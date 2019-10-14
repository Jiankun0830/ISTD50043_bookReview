import mysql.connector as db
import copy

# TODO 1: Add database name as env var



DATABASE="kindle_reviews"

class SQL_db:
    def __init__(self):
        self.conn=db.connect(host="localhost",user="root",password="",db=DATABASE)
        self.get_num_entires()

    
    def describe(self):
        cursor=self.conn.cursor()
        cursor.execute("desc reviews")
        res=cursor.fetchall()
        return res


    def get_num_entires(self):
        cursor=self.conn.cursor()
        cursor.execute("select count(*) from reviews;")
        res=cursor.fetchall()[0][0]
        self.count = res

        return res


    '''
    input field:
    Any asin number of a book in kinde_reviews.reviews
    output field :  
    idx,asin,helpful, overall, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime,
    '''
    def get_review(self,asin='B00LE4Q95G'):
        cursor = self.conn.cursor()
        cursor.execute("""select reviewerName,overall,reviewText,reviewTime from reviews where asin = %(asin)s;""",{"asin":asin})
        
        res=cursor.fetchall()
        return res

    

    #TODO 2: There should be constraints on insertion once we decided primary key
    def add_review(self,asin,overall,reviewText,idx=None,helpful=None,reviewTime=None,reviewerID=None,reviewerName=None,summary=None, unixReviewTime=None):
        cursor = self.conn.cursor()
        idx = self.count +1
        inputs = {'idx':idx,'asin':asin,'helpful':helpful, 'overall':overall, 'reviewText':reviewText, 'reviewTime':reviewTime, 'reviewID':reviewerID, 'reviewerName':reviewerName, 'summary':summary, 'unixReviewTime':unixReviewTime}
        new_inputs = inputs.copy()
        for i in inputs:
            if inputs[i] == None:
                del new_inputs[i]
        
        clm_name = ''
        clm_value = ''

        for j in new_inputs:
            clm_name = clm_name + ','+j
            if j == 'idx' or j == 'overall':
                clm_value = clm_value + ',' + str(inputs[j])
            else:
                clm_value = clm_value + ',' +"'"+str(inputs[j])+"'"

        clm_name = clm_name[1:]
        clm_value =clm_value[1:]


        # cursor.execute("""
        #     insert into reviews(%(column_names)s)
        #     values(%(column_values)s);
        #     """,{"column_names":clm_name,"column_values":clm_value})

        print(cursor.execute("""
            insert into reviews({})
            values({});
            """.format(clm_name,clm_value)))

        
        cursor.execute("""insert into reviews (idx,asin,reviewText) values(27501,'ltltltltlt','test4');""")
        self.conn.commit()
        cursor.execute("""select * from reviews where asin = %(asin)s;""",{"asin":asin})
        res=cursor.fetchall()
        return res


    def get_review(self,asinID):
        cursor = self.conn.cursor()
        cursor.execute("select reviewerName,summary,overall,reviewTime from reviews where asin = %(asin)s;", {'asin':asinID})
        res=cursor.fetchall()
        return res


test = SQL_db()
test.describe()

print(test.get_review('B00LE4Q95G'))


# Example for using this class: 

# test = SQL_db()

# print(test.add_review(idx=26356,asin='tfdt11re89',overall=4,reviewText='test lalala',summary='this is a summary'))

# print(test.get_review(asin='tfdt11re89'))
