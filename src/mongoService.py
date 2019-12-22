from pymongo import MongoClient
import time

import os
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

    def get_sorted_title(self):
        pass

    def insert_query(self, query):
        self.log.insert_one(query)
    
    def get_related_books(self, asin, feature):
        a = self.con.find({"asin": asin})
        try:
            ls = [i["related"][feature] for i in a]
        except KeyError:
            ls = []
            return ls
        
        # print(len(ls[0]))

        z = self.con.find({ 'asin' : {'$in' : ls[0] } })
        l = [i for i in z]
        
        return l

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
    # print(Mg().get_highest_rank_books("Dictionaries & Thesauruses"))
    print(Mg().get_related_books("B000FA5S98", 'also_bought'))
