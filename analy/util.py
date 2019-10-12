from pymongo import MongoClient
class Mg:
    def __init__(self):
        self.con=MongoClient("mongodb://localhost:27017/")["book_metadata"]["metadata"]
mg=Mg().con
def get_all_info():
    a=mg.find({"asin":"B000FA5M3K"})
    for i in a:
        print(str(i))
def get_total():
    a=mg.find().count()
    print(str(a))
def get_all():
    a=mg.distinct("asin")
    for i in a:
        print(str(i))
#get_all_keys()
#get_all_info()
#get_total()
get_all()
