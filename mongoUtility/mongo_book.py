from pymongo import MongoClient
import json

class MyMongo:
    def __init__(self):
        self.client = MongoClient()
    def createNewDb(self, dbName, collecName, dbFile):
        # dbName: string
        # collecName: string, name of the new collection
        # dbFile: string, name of the json file
        db = self.client[dbName]
        collection = db[collecName]
        with open(dbFile) as f:
            file_data = json.load(f)
        collection.insert_one(file_data)
    def addBook(self, dbName, collecName, asin, title=None, price=None, imUrl=None, also_bought=[], also_viewed=[], buy_after_viewing=[], bought_together=[]):
        # dbName: string
        # collecName: string
        # jsonList: a list of json records to be inserted in to the collection
        db = self.client[dbName]
        collection = db[collecName]
        cursor = collection.find({'asin':asin})
        if cursor.count() > 0:
            raise Exception('Book with given asin already exists!')
        else:
            toInsert = {'asin':asin,
                'title': title,
                'price': price,
                'imUrl': imUrl,
                'related':{'also_bought': also_bought,
                    'also_viewed':also_viewed,
                    'buy_after_viewing': buy_also_viewing,
                    'bought_together': bought_together}}
            jsonString = json.dumps(toInsert)
            x = collection.insert_one(jsonString)
    def getBook(self, dbName, collecName, asin):
        # asin: string
        db = self.client[dbName]
        collection = db[collecName]
        query = { "asin": asin}
        doc = collection.find(query)
        book = []
        for i in doc:
            book.append(dict(i))
        if len(book)>1:
            raise Exception('Found more than one book with the given asin!')
        elif len(book)==0:
            raise Exception('The book with given asin is not found!')
        else:
            return book[0]
    
