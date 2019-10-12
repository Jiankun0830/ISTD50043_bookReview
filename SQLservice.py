import mysql.connector as db


DATABASE="kindle_reviews"

class SQL_db:
    def __init__(self):
        self.conn=db.connect(host="localhost",user="root",password="",db=DATABASE)
    
    def describe(self):
        cursor=self.conn.cursor()
        cursor.execute("desc reviews")
        res=cursor.fetchall()
        return res

    '''
    input field:
    Any asin number of a book in kinde_reviews.reviews

    output field :  
    idx,asin,helpful, overall, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime,
    '''
    def get_review(self,asinID):
        cursor = self.conn.cursor()
        cursor.execute("select reviewerName,summary,overall,reviewTime from reviews where asin = %(asin)s;", {'asin':asinID})
        res=cursor.fetchall()
        return res


test = SQL_db()
test.describe()

print(test.get_review('B00LE4Q95G'))


