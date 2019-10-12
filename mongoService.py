from pymongo import MongoClient
class Mg:
    def __init__(self):
        self.con=MongoClient("mongodb://localhost:27017/")["book_metadata"]["metadata"]
  
    #mg=Mg().con
    def get_all_info(self,param):
        a=self.con.find({"asin":param})
        ls=[]
        for i in a:
            ls.append(str(i))
        return ls
    
    def get_total(self):
        a=self.con.find().count()
        print(str(a))
    
    def get_all(self):
        a=self.con.distinct("asin")
        ls=[]
        for i in a:
            ls.append(str(i))
        return ls
#get_all_keys()
#get_all_info()
#get_total()


############## test ###########################
'''
    def show(self):
        a=self.con.find({})
        ls=[]
        for i in a:
            ls.append(str(i))
        return ls
    def get(self,param):
        a=self.con.find({""})
'''
