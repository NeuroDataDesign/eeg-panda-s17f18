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
        print(db)
        # specify collection
        lims = db.lims
        return lims
    except:
        raise Exception("MongoDB not running.")


def build_database(dataset, modality, bids_parser, task_list):
    # Initialize
    lims = init_database()
    build_dataset(lims, dataset)

    print(bids_parser)
    # Insert into db
    for sub, datatypes in bids_parser.dataset.items():
        for datatype, tasks in datatypes.items():
            if datatype not in task_list:
                continue
            for task, links in tasks.items():
                build_derivative(lims, dataset, modality, sub, datatype, task, links)

def build_dataset(lims, dataset):
    lims.update_one(
        filter = {"_id": dataset},
        update = {"$setOnInsert": { "subjects": [] }},
        upsert = True
    )

def update_dataset(lims, dataset, subject):
    print(subject)
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


def build_derivative(lims, dataset, modality, subject, datatype, task, links):

    update_dataset(lims, dataset, subject)

    global scan_count
    scan_count += len(links)
    links = list(filter(lambda link: link.find('sub') >= 0 and link.find('_') >= 0, links))

    lims.update_one(
        filter = {'_id': subject},
        update = {'$set': { dataset + '.' + modality + '.' + datatype + '.' + task : links}},
        upsert = True
    )

    print("Updated Scan Count: " + str(scan_count))

def build_metadata(filename, dataset):
    lims = init_database()
    metadata_list = parse_csv(filename)

    for metadata in metadata_list:

        # Try to get subject ID, no other way besides brute force right now
        subid = metadata.pop("\ufeffEID", -1)
        if (subid == -1):
            subid = metadata.pop("URSI", -1)
        if (subid == -1):
            subid = metadata.pop("ursi", -1)
        if (subid == -1):
            subid = metadata.pop("SubjectID", -1)
        if (subid == -1):
            continue

        # try:
        #     session = metadata.pop("SESSION")
        # except:
        #     session = "Session-1"

        for key, value in metadata.items():
            try:
                result = lims.update_one(
                    filter = {"_id": "sub-" + subid},
                    update = {"$set": {dataset + ".metadata." + key: value}}
                )

                ##Update did not occur
                if (result.matched_count < 1):
                    lims.update_one(
                        filter = {"_id": "sub-00" + subid},
                        update = {"$set": {dataset + ".metadata."  + key: value}}
                    )
            except:
                raise Exception("Error adding metadata")

    print("Added Metadata")


###########################

def get_subject(link_header):
    return link_header.split("_")[0]

#########################################

def delete_dataset(dataset):
    # Initialize
    lims = init_database()
    cursor = lims.find({ '_id' : dataset })
    subjs = []
    for doc in cursor:
        subjs = doc['subjects']
        break
    for s in subjs:
        lims.update_one({'_id': s}, {'$unset': {dataset: ''}})
    lims.remove({ '_id' : dataset })

if __name__ == '__main__':
    lims = init_database()
    build_dataset(lims, 'lord_forgive_me')
