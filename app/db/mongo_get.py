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

def get_from_database(dataset, ids):
    # Initialize
    lims = init_database()
    print(ids)
    cursor = lims.find({ '_id' : { '$in' : ids } }, { dataset : 1, dataset + '.metadata' : 1})
    subjs = []
    print(cursor)
    for doc in cursor:
        doc = {'_id' : doc['_id'], 'metadata' : doc[dataset].get('metadata', {})}
        subjs.append(doc)
    return subjs

def get_from_dataset(dataset):
    # Initialize
    lims = init_database()
    cursor = lims.find({ '_id' : dataset })
    subjs = []
    for doc in cursor:
        subjs = doc['subjects']
        break
    return subjs

