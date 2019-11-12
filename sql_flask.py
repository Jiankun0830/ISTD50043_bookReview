from flask import Flask,request
import mysql.connector as db
import SQLservice

app = Flask(__name__)


@app.route('/get_description')

def get_description():
    return (str(SQLservice.SQL_db().describe()))

@app.route('/get_review/<asin>')

def get_review(asin):
    return (str(SQLservice.SQL_db().get_review(asin)))


if __name__ == '__main__':
    app.run(debug=True)

