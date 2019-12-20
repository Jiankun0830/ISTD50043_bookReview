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
        df=df.drop(['_id', 'query_type', 'query', 'response','user_type'],axis=1)
        df["date"]=df.apply(lambda row:time.strftime('%Y-%m-%d',
            time.localtime(row.time_stamp)),axis=1)
        re=pd.DataFrame({"cnt":df.groupby(['date']).size()}).reset_index().to_numpy()
        return re[:,0],re[:,1]    
    
    def plot_test(self):
        s = pd.Series([1, 2, 3])
        fig, ax = plt.subplots()
        s.plot.bar()
        fig.savefig('img/my_plot.png')

    def plot_trend(self):
        #get df from mongoDB
        a=self.log.find({})
        df=pd.DataFrame(list(a))
        df=df.drop(['_id', 'query_type', 'query', 'response','user_type'],axis=1)
        df["date"]=df.apply(lambda row:time.strftime('%Y-%m-%d',
            time.localtime(row.time_stamp)),axis=1)

        re=pd.DataFrame({"cnt":df.groupby(['date']).size()}).reset_index().to_numpy()
        #data to plot        
        dates=re[:,0].astype("datetime64[D]")
        y=re[:,1]
        #plot fig
        fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(6, 4))
        start=np.datetime64('2019-11-01')
        end=np.datetime64('2019-11-30')
        lims=(start,end)
        #add zero
        
        all_dates = np.arange(start,end, DT.timedelta(days=1)).astype("datetime64[D]")
        y_0=np.zeros(len(all_dates))

        for i,o in enumerate(dates):
            result=np.where(all_dates==o)
            y_0[result]=y[i]
        
        # Plot
        ax.plot(all_dates, y_0)
        ax.set_xlim(lims)
        # rotate_labels...
        for label in ax.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')
        ax.set_title('Default Date Formatter')
        fig.savefig('img/plot_trend.png')
    
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

    def get_highest_viewed_books(self, k=5):
        all_query = list(self.log.find({}, {'query':1}))
        asins = [d['query'].split('/')[-1] for d in all_query if d['query'].split('/')[-1].startswith('B')]
        print([item for item, c in Counter(asins).most_common(k)])
        print('a')
        return  [item for item, c in Counter(asins).most_common(k)]
   
    def get_highest_view_books_by_user(self, userid, k=5):
        all_query = list(self.log.find({'userid':userid}, {'query':1}))
        asins = [d['query'].split('/')[-1] for d in all_query if d['query'].split('/')[-1].startswith('B')]
        return [item for item, c in Counter(asins).most_common(k)]


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
    print(Mg().get_highest_rank_books("Dictionaries & Thesauruses"))
    print("hi")
    #get two tsv file pre-loaded
    #Mg().plot_heat(1)
    #Mg().plot_heat(0)
    #print(Mg().mongo_to_df())
