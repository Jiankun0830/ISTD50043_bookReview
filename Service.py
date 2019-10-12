import mysql.connector as db
from pymongo import MongoClient

DATABASE="yunyi_test"
class Sql_db:
    def __init__(self):
        self.conn=db.connect(host="localhost",user="root",password="",db=DATABASE)
    
    def describe(self):
        cursor=self.conn.cursor()
        cursor.execute("describe review")
        res=cursor.fetchall()
        return res
    def find(self,params):
        cursor=self.conn.cursor()

    
