import pickle


with open('tags.pkl', 'rb') as f:
    data = pickle.load(f)

f = open("categories.txt","w+")
f.write(str(data))
f.close()