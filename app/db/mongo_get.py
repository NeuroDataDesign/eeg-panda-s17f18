from pymongo import MongoClient

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

def get_from_database(dataset, ids, modality):
    # Initialize
    lims = init_database()
    cursor = lims.find({ '_id' : { '$in' : ids } }, { dataset : 1, dataset + '.' + modality : 1, dataset + '.metadata' : 1})
    subjs, datatypes, tasks = [], [], []
    for doc in cursor:
        subjs.append({'_id' : doc['_id'], 'metadata' : doc[dataset].get('metadata', {})})
        datatypes.append(list(doc[dataset][modality].keys()))
        tasks.append([list(doc[dataset][modality][datatype].keys()) for datatype in datatypes[-1]])
    return subjs, datatypes, tasks

def get_from_dataset(dataset):
    # Initialize
    lims = init_database()
    cursor = lims.find({ '_id' : dataset })
    subjs = []
    for doc in cursor:
        subjs = doc['subjects']
        break
    return subjs

def get_datatype_task(dataset, modality):
    # Initialize
    lims = init_database()
    subjs = get_from_dataset(dataset)

    datatypes, tasks = set(), set()

    cursor = lims.find({ '_id' : { '$in' : subjs } }, { dataset + '.' + modality : 1})
    for doc in cursor:
        curr_datatypes = list(doc[dataset][modality].keys())
        datatypes.update(curr_datatypes)
        for datatype in curr_datatypes:
            tasks.update(doc[dataset][modality][datatype].keys())

    return list(datatypes), list(tasks)


