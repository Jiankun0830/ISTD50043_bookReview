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
        self.log = MongoClient(mongo_addr)["book_log"]["log"]

        # self.con = MongoClient("mongodb://db_grp7_test:1234567@3.234.153.108/book_log")["book_metadata"]["metadata"]
        # self.log = MongoClient("mongodb://db_grp7_test:1234567@3.234.153.108/book_log")["book_log"]["log"]
        # self.con = MongoClient("mongodb://localhost:27017/")["book_metadata"]["metadata"]
        # self.log = MongoClient("mongodb://localhost:27017/")["book_log"]["log"]
    
    def mongo_to_df(self,query={}):
        a=self.log.find(query)
        df=pd.DataFrame(list(a))
        df=df.drop(['user_id', 'query_type', 'query', 'response','user_type'],axis=1)
        df["date"]=df.apply(lambda row:time.strftime('%Y-%m-%d',
            time.localtime(row.time_stamp)),axis=1)
        re=pd.DataFrame({"cnt":df.groupby(['date']).size()}).reset_index().to_numpy()
        return re[:,0],re[:,1]    
    
    # def plot_test(self):
    #     s = pd.Series([1, 2, 3])
    #     fig, ax = plt.subplots()
    #     s.plot.bar()
    #     fig.savefig('img/my_plot.png')

    def plot_trend(self):
        #get df from mongoDB
        a=self.log.find({})
        df=pd.DataFrame(list(a))
        df=df.drop(['user_id', 'query_type', 'query', 'response','user_type'],axis=1)
        df["date"]=df.apply(lambda row:time.strftime('%Y-%m-%d',
            time.localtime(row.time_stamp)),axis=1)

        re=pd.DataFrame({"cnt":df.groupby(['date']).size()}).reset_index().to_numpy()
        #data to plot        
        dates=re[:,0].astype("datetime64[D]")
        y=re[:,1]
        #plot fig
        fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(6, 4))
        start=np.datetime64('2019-12-01')
        end=np.datetime64('2019-12-30')
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
            file_name='data/last_week_history.tsv'            
        #for all previous history
        else:
            a=self.log.find({})
            file_name='data/all_history.tsv'
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
                    t1=time.strftime('%A %H', time.localtime(t)).split(" ")
                    tsv_writer.writerow([week_dic[t1[0]],t1[1],1])

if __name__ == "__main__":
    pass
