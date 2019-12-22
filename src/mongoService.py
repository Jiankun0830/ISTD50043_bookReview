from pymongo import MongoClient
import time
import pandas as pd
import matplotlib.pyplot as plt # to plot analytics
import datetime as DT
import csv
import os
import matplotlib.dates as mdates # for date plot
import numpy as np
from collections import Counter

MONGO_IP = os.environ['LC_MONGO_IP']

class Mg:
    def __init__(self):
        mongo_addr = "mongodb://db_grp7_test:1234567@"+MONGO_IP+"/book_log"
        self.con = MongoClient(mongo_addr)["book_metadata"]["metadata"]
        self.log = MongoClient(mongo_addr)["book_log"]["log"]

        # self.con = MongoClient("mongodb://db_grp7_test:1234567@3.234.153.108/book_log")["book_metadata"]["metadata"]
        # self.log = MongoClient("mongodb://db_grp7_test:1234567@3.234.153.108/book_log")["book_log"]["log"]
        # self.con = MongoClient("mongodb://localhost:27017/")["book_metadata"]["metadata"]
        # self.log = MongoClient("mongodb://localhost:27017/")["book_log"]["log"]
    
    def mongo_to_df(self,query={}):
        a=self.log.find(query)
        df=pd.DataFrame(list(a))
        #print(df.columns)
        df=df.drop(['userid', 'query_type', 'query', 'response','user_type'],axis=1)
        df["date"]=df.apply(lambda row:time.strftime('%Y-%m-%d',
            time.localtime(row.time_stamp)),axis=1)
        re=pd.DataFrame({"cnt":df.groupby(['date']).size()}).reset_index().to_numpy()
        return re[:,0],re[:,1]    
    
    def get_highest_viewed_books(self, k=5):
        # For admin
        all_query = list(self.log.find({}, {'query':1}))
        asins = [d['query'].split('/')[-1] for d in all_query if d['query'].split('/')[-1].startswith('B')]
        most_common_asins = [item for item, c in Counter(asins).most_common(k)]
        books = [next(self.con.find({"asin": o})) for o in most_common_asins]
        return books
   
    def get_highest_viewed_books_by_user(self, userid, k=5):
        # For user
        all_query = list(self.log.find({'user_id':userid}, {'query':1}))
        asins = [d['query'].split('/')[-1] for d in all_query if d['query'].split('/')[-1].startswith('B')]
        most_common_asins = [item for item, c in Counter(asins).most_common(k)]
        books = [next(self.con.find({"asin": o})) for o in most_common_asins]
        return books

    def get_bestsellers(self):
        a=self.con.find({"salesRank":{'$exists': 1}})
        #,{"asin":1,"salesRank":1}
        ls=[]
        for i in a:
            ls.append(i)
        return ls

    def get_all_info(self, param):
        a = self.con.find({"asin": param})
        ls = [i for i in a]
        return ls

    def search_book(self, keyword):
        query = {'$or':[{'title':{"$regex":keyword,"$options":"i"}},{'author':{"$regex":keyword,"$options":"i"}},
                        {'brand':{"$regex":keyword, "$options":"i"}},{'asin':{"$regex":keyword, "$options":"i"}},
                        {'categories': {'$elemMatch': {'$elemMatch': {"$regex":keyword, "$options":"i"}}}}]}
        cursor = self.con.find(query)
        results = [book for book in cursor]
        return results

    def add_book(self, asin, title=None, price=None, imUrl=None, category=[], salesRank={}, brand=None, also_bought=[],
                 also_viewed=[], buy_after_viewing=[], bought_together=[]):
        # asin, title, brand, imUrl: string
        # salesRank={category: integer}
        # category: list of list
        cursor = self.con.find({'asin': asin})
        if cursor.count() > 0:
            raise Exception('Book with given asin already exists.')
        else:
            toInsert = {'asin': asin,
                        'title': title,
                        'price': price,
                        'imUrl': imUrl,
                        'related': {'also_bought': also_bought,
                                    'also_viewed': also_viewed,
                                    'buy_after_viewing': buy_after_viewing,
                                    'bought_together': bought_together},
                        'categories': category,
                        'salesRank': salesRank,
                        'brand': brand}
            x = self.con.insert_one(toInsert)

    def get_all_books(self, skip, category):
        if (category == "all"):
            param = {}
        else:
            param = {'categories': {'$elemMatch': {'$elemMatch': {'$in': [category]}}}}
        a = self.con.find(param).limit(100).skip(100 * (skip - 1))
        ls = [i for i in a]
        return ls

    def get_all(self):
        a = self.con.distinct("asin")
        ls = [i for i in a]
        return ls

    def get_category(self, param):
        p = {'categories': {'$elemMatch': {'$elemMatch': {'$in': [param]}}}}
        a = self.con.find(p)
        ls = [i for i in a]
        return ls

    def insert_query(self, query):
        self.log.insert_one(query)
    
    def get_related_books(self, asin, feature):
        a = self.con.find({"asin": asin})
        try:
            ls = [i["related"][feature] for i in a]
        except KeyError:
            ls = []
            return ls
        
        z = self.con.find({ 'asin' : {'$in' : ls[0] } })
        l = [i for i in z]
        
        return l

    def get_book_log(self):
        self.log.find({})

    def get_highest_rank_books(self, category):
        categories = ["Mystery, Thriller & Suspense",
                      "Science Fiction & Fantasy",
                      "Action & Adventure",
                      "Love & Romance",
                      "Business & Money",
                      "Health, Fitness & Dieting",
                      "Professional & Technical",
                      "Administration & Policy",
                      "Dictionaries & Thesauruses",
                      "Biographies & Memoirs"
                      ]
        if category not in categories:
            raise Exception("No such category")
        else:
            temp = 'salesRank.'+category
            a = self.con.find( {temp:{'$exists': True }} ).limit(10)
            ls = [i for i in a]
            ls.insert(0, category)
            return ls
    

if __name__ == "__main__":
    pass
