import mysql.connector as db
import copy
from datetime import datetime
import os

# TODO 1: Add database name as env var


DATABASE = "kindle_reviews"
MYSQL_IP = os.environ['LC_MYSQL_IP']

class SQL_db:
    def __init__(self):
        # self.conn = db.connect(host="54.244.217.119", user="root", password="", db=DATABASE)
        # self.conn = db.connect(host="localhost", user="root", password="", db=DATABASE)
        self.conn = db.connect(host=MYSQL_IP, user="root", password="", db=DATABASE)
        self.get_num_entires()

    def describe(self):
        cursor = self.conn.cursor()
        cursor.execute("desc reviews")
        res = cursor.fetchall()
        return res

    def get_num_entires(self):
        cursor = self.conn.cursor()
        cursor.execute("select count(*) from reviews;")
        res = cursor.fetchall()[0][0]
        self.count = res

        return res

    '''
    input field:
    Any asin number of a book in kinde_reviews.reviews
    output field :  
    idx,asin,helpful, overall, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime,
    '''

    # TODO 2: There should be constraints on insertion once we decided primary key
    def add_review(self, asin, overall, reviewText=None, helpful=None, reviewerID=None, reviewerName="Guest",
                   summary=None, unixReviewTime=None):
        cursor = self.conn.cursor()
        idx = self.count + 1
        reviewTime = datetime.today().strftime('%m %d, %Y')
        inputs = {'idx': idx, 'asin': asin, 'helpful': helpful, 'overall': overall, 'reviewText': reviewText,
                  'reviewTime': reviewTime, 'reviewerID': reviewerID, 'reviewerName': reviewerName, 'summary': summary,
                  'unixReviewTime': unixReviewTime}
        new_inputs = inputs.copy()
        for i in inputs:
            if inputs[i] == None:
                del new_inputs[i]

        clm_name = ''
        clm_value = ''

        for j in new_inputs:
            clm_name = clm_name + ',' + j
            if j == 'idx' or j == 'overall':
                clm_value = clm_value + ',' + str(inputs[j])
            else:
                clm_value = clm_value + ',' + "'" + str(inputs[j]) + "'"

        clm_name = clm_name[1:]
        clm_value = clm_value[1:]

        print(cursor.execute("""
            insert into reviews({})
            values({});
            """.format(clm_name, clm_value)))

        cursor.execute("""insert into reviews (idx,asin,reviewText) values(27501,'ltltltltlt','test4');""")
        self.conn.commit()
        cursor.execute("""select * from reviews where asin = %(asin)s;""", {"asin": asin})
        res = cursor.fetchall()
        return res

    def get_review(self, asinID):
        cursor = self.conn.cursor()
        cursor.execute("select reviewerName,summary,overall,reviewTime,reviewText from reviews where asin = %(asin)s;",
                       {'asin': asinID})
        res = cursor.fetchall()
        return res

    def get_most_rated_books(self):
        cursor = self.conn.cursor()
        cursor.execute("""select * from mostRated;""")
        res = cursor.fetchall()
        return res
    
    def get_highest_rated_books(self):
        cursor = self.conn.cursor()
        cursor.execute("""select * from highestAvgScore;""")
        res = cursor.fetchall()
        return res
    
    def generate_additional_tables(self):
        # cursor = self.conn.cursor()
        # cursor.execute('source database/sql/create_additional_tables.sql;')
        # self.conn.commit()
        # # res = cursor.fetchall()
        # # return res

        os.system("mysql -u root < database/sql/create_additional_tables.sql")

if __name__ == "__main__":
    pass
    # print(SQL_db().describe())
    # print(SQL_db().generate_additional_tables())
    # print(SQL_db().get_most_rated_books())
    # print(SQL_db().get_highest_rated_books())
