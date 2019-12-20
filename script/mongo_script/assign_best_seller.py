from pymongo import MongoClient

col = MongoClient("mongodb://localhost:27017/")["book_metadata"]["metadata"]
print(col.find().count())
categories = ["Mystery, Thriller & Suspense"
,"Science Fiction & Fantasy"
,"Action & Adventure"
,"Love & Romance"
,"Business & Money"
,"Health, Fitness & Dieting"
,"Professional & Technical"
,"Administration & Policy"
,"Dictionaries & Thesauruses"
,"Biographies & Memoirs"
]

def assign_rank(category):
    p = {'categories': {'$elemMatch': {'$elemMatch': {'$in': [category]}}}}
    documents = col.find(p).limit(10)
    ids = [i['asin'] for i in documents]
    ranks = list(range(1,11))
    for i,rank in enumerate(ranks):
        col.update_one({'asin':ids[i]},{"$set":{"salesRank":{category:rank}}})
    print("Updated category "+category)

for i in categories:
    assign_rank(i)
