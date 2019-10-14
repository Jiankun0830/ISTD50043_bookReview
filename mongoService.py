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
    
    def get_total(self):
        a=self.con.find().count()
        print(a)
    
    def get_all_books(self, skip):
        a=self.con.find().limit(100).skip(100*skip)
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
