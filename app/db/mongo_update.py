import csv
import boto3
from pymongo import MongoClient

'''
SCHEMA:
Dataset:
{
    _id = dataset_name
    _subjects = [list of subject document ids]
}

Subject:
{
    _id = subject id
    metadata = {
        session: {
            {key: value},
            {key: value},
        }
        ...
    }
    datatype = {
        derivative: [
            {link : neuroglancer link},
            {link : neuroglancer link},
            ...
        ]
    }
}

'''

scan_count = 0

#################
# Database Functions

def init_database():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        # specify database
        db = client.m2gdatabase
        # specify collection
        lims = db.lims
        return lims
    except:
        raise Exception("MongoDB not running.")

def build_database(dataset, bucket_name):
    # Initialize
    lims = init_database()
    build_dataset(lims, dataset)

    # TODO: Use Docker creds
    # Read creds
    rows = []
    with open('/home/nitin/.aws/s3_creds') as credsfile:
        cred_reads = csv.reader(credsfile)
        for row in cred_reads:
            rows.append(row)
    creds = dict(zip(rows[0], rows[1]))

    # Read listing of files
    s3 = boto3.resource('s3', aws_access_key_id=creds['access_key'], aws_secret_access_key=creds['secret_key'],
                        region_name='us-east-1')
    bucket = s3.Bucket('lemur-simple')
    subs = dict()
    for elem in bucket.objects.all():
        file_structs = elem.key.split('/')
        if len(file_structs) < 4:
            continue
        subs[file_structs[1]] = subs.get(file_structs[0], {})
        subs[file_structs[1]][file_structs[0]] = subs[file_structs[1]].get(file_structs[0], {})
        subs[file_structs[1]][file_structs[0]][file_structs[2]] = subs[file_structs[1]][file_structs[0]].get(
            file_structs[2], [])
        subs[file_structs[1]][file_structs[0]][file_structs[2]].append([file_structs[3], file_structs[3]])

    print(subs)

    # Insert into db
    for sub, datatypes in subs.items():
        for datatype, derivs in datatypes.items():
            for deriv, links in derivs.items():
                build_derivative(lims, dataset, datatype, deriv, links)

    # build_metadata(lims)

def build_dataset(lims, dataset):
    lims.update_one(
        filter = {"_id": dataset},
        update = {"$setOnInsert": { "subjects": [] }},
        upsert = True
    )

def update_dataset(lims, dataset, subject):
    lims.update_one(
        filter = {"_id": dataset},
        update = {"$addToSet": { "subjects": subject }}
    )

#################

def parse_csv(filename):
    metadata_list = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        keys = next(reader)
        # remaining lines are subject metadata
        for row in reader:
            metadata = {}
            for i in range(len(row)):
                ## get corresponding key
                if row[i] == "#":
                    continue
                metadata[keys[i]] = row[i]
            metadata_list.append(metadata)

    return metadata_list

def build_derivative(lims, dataset, datatype, derivative, links):

    global scan_count
    for link_list in links:
        scan_count += 1
        link_header = link_list[0]
        ## invalid parse
        ## TODO: get better fix
        if (link_header.find("sub") < 0 or link_header.find("_") < 0):
            continue
        # url = encode_url(link_list[1])
        url = link_list[1]

        subject = get_subject(link_header)
        update_dataset(lims, dataset, subject)
        # insert  and subject dataype if needed

        write_result = lims.update_one(
            filter = {"_id": subject},
            update = {"$setOnInsert": { datatype + "." + derivative: [{url: ""}]}},
            upsert = True
        )

        if (write_result.upserted_id is not None):
            continue

        lims.update_one(
            filter = {"_id": subject, datatype + "." + derivative: {"$exists": False}},
            update = { "$set": { datatype + "." + derivative: [] }},
        )
        #insert url to derivative list
        #NOTE: no upsert option exists
        lims.update_one(
            filter = {"_id": subject}, #query
            update = {
                "$push": { datatype + "." + derivative: {url: ""} }
            }
        )
    print("Updated Scan Count: " + str(scan_count))

def build_metadata(lims, filename):
    metadata_list = parse_csv(filename)

    for metadata in metadata_list:

        # Try to get subject ID, no other way besides brute force right now
        subid = metadata.pop("SUBID", -1)
        if (subid == -1):
            subid = metadata.pop("URSI", -1)
        if (subid == -1):
            subid = metadata.pop("ursi", -1)
        if (subid == -1):
            subid = metadata.pop("SubjectID", -1)
        if (subid == -1):
            continue

        try:
            session = metadata.pop("SESSION")
        except:
            session = "Session-1"

        for key, value in metadata.items():
            try:
                result = lims.update_one(
                    filter = {"_id": "sub-" + subid},
                    update = {"$set": {"metadata." + session + "." + key: value}}
                )

                ##Update did not occur
                if (result.matched_count < 1):
                    lims.update_one(
                        filter = {"_id": "sub-00" + subid},
                        update = {"$set": {"metadata." + session + "." + key: value}}
                    )
            except:
                raise Exception("Error adding metadata")

    print("Added Metadata")


###########################

def get_subject(link_header):
    return link_header.split("_")[0]


if __name__ == "__main__":
    build_database('test_new_BIDS')
