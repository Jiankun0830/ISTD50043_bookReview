from pymongo import MongoClient
import time
import pandas as pd
import matplotlib.pyplot as plt
#to plot analytics
import datetime as DT
import csv
import os
class Mg:
    def __init__(self):
        self.con = MongoClient("mongodb://db_grp7_test:1234567@3.234.153.108/book_log")["book_metadata"]["metadata"]
        self.log = MongoClient("mongodb://db_grp7_test:1234567@3.234.153.108/book_log")["book_log"]["log"]
        # self.con = MongoClient("mongodb://localhost:27017/")["book_metadata"]["metadata"]
        # self.log = MongoClient("mongodb://localhost:27017/")["book_log"]["log"]
    
    ########data visualization######## 
    def plot_test(self):
        s = pd.Series([1, 2, 3])
        fig, ax = plt.subplots()
        s.plot.bar()
        fig.savefig('img/my_plot.png')

    def plot_heat(self,choice=1):
        #for last 7 days:
        if choice==0:
            week_ago=(DT.date.today() - DT.timedelta(8)).strftime("%s")
            a=self.log.find({"time_stamp" : {"$gte": float(week_ago)}})
            file_name='data/week.tsv'            
        #for all previous history
        else:
            a=self.log.find({})
            file_name='data/all.tsv'
        #append result to ls
        ls=[]
        for i in a:
            ls.append(i)
        week_dic={"Monday":1,
                  "Tuesday":2,
                  "Wednesday":3,
                  "Thursday":4,
                  "Friday":5,
                  "Saturday":6,
                  "Sunday":7
                }
        #write to tsv file for quick parsing
        try:
            #if file exits,overwrite
            with open(file_name, 'w') as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(["day","hour","value"])
                for i in ls:
                    t=i["time_stamp"]
                    t1=time.strftime('%A %H', time.localtime(t)).split(" ")
                    tsv_writer.writerow([week_dic[t1[0]],t1[1],1])
        except:
            #if not, create file
            with open(file_name, 'a') as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow(["day","hour","value"])
                for i in ls:
                    t=i["time_stamp"]
                    print(t)
                    t1=time.strftime('%A %H', time.localtime(t)).split(" ")
                    tsv_writer.writerow([week_dic[t1[0]],t1[1],1])

    #################################

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
    #print(Mg().get_highest_rank_books("Dictionaries & Thesauruses"))
    Mg().plot_heat(1)
    Mg().plot_heat(0)
