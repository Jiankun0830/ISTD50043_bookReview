from pymongo import MongoClient
class Mg:
    def __init__(self):
        self.con=MongoClient("mongodb://localhost:27017/")["book_metadata"]["metadata"]
  
    def get_all_info(self,param):
        a=self.con.find({"asin":param})
        ls=[]
        for i in a:
            ls.append(i)
        return ls
    
    def add_book(self, asin, title=None, price=None, imUrl=None, category=[], salesRank={}, brand=None, also_bought=[], also_viewed=[], buy_after_viewing=[], bought_together=[]):
        # asin, title, brand, imUrl: string
        # salesRank={category: integer}
        # category: list of list
        cursor = self.con.find({'asin':asin})
        if cursor.count() > 0:
            raise Exception('Book with given asin already exists.')
        else:
            toInsert = {'asin':asin,
                    'title': title,
                    'price': price,
                    'imUrl': imUrl,
                    'related':{'also_bought':also_bought,
                        'also_viewed':also_viewed,
                        'buy_after_viewing':buy_after_viewing,
                        'bought_together':bought_together},
                    'categories':category,
                    'salesRank':salesRank,
                    'brand':brand}
            x = self.con.insert_one(toInsert)
    def get_total(self):
        a=self.con.find().count()
        print(a)
    
    def get_all_books(self):
        a=self.con.find()
        ls=[]
        for i in a:
            ls.append(i)
        return ls

    def get_all(self):
        a=self.con.distinct("asin")
        ls=[]
        for i in a:
            ls.append(i)
        return ls
    
    def get_category(self,param):
        a=self.con.find({"category":param})
        ls=[]
        for i in a:
            ls.append(i)
        return ls
    
    def get_sorted_title(self):
        pass
