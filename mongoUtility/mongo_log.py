from pymongo import MongoClient
import json

class MyMongoLog:
    def __init__(self):
        self.client = MongoClient()
    def createNewDb(self, dbName, collecName,dbFile):
        db = self.client[dbName]
        collection = db[collecName]
        with open(dbFile) as f:
            file_data = json.load(f)
        collection.insert_one(file_data)
    def addLog(self, dbName, collecName, timeStamp, requestType, response):
        # timeStamp: string
        # requestType: string
        # response: json object
        db = self.client[dbName]
        collection = db[collecName]
        response = json.loads(response)
        toInsert = {'timeStamp':timeStamp, 'requestType':requestType, 'response':response}
        x = collection.insert_one(toInsert)
    def delLog(self, dbName, collecName, timeStamp):
        # timeStamp: string
        collection = self.client[dbName][collecName]
        toDelete = {"timeStamp":timeStamp}
        collection.delete_one(toDelete)
