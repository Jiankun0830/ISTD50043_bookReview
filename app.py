from flask import url_for,redirect,Flask,render_template
import SQLservice
import mongoService
import numpy as np
import pandas as pd



app=Flask(__name__)
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/bookdemo")
def bookdemo():
    return url_for('about')

@app.route("/sql")
def des_sql():
    return (str(SQLservice.Sql_db().describe()))

@app.route("/bookinfo")
def book_list():
    return(str(mongoService.Mg().get_all()))

@app.route("/bookinfo/<page_num>")
def book_list_page(page_num):
    page_num=int(page_num)
    book_list=mongoService.Mg().get_all_books(page_num)
    total=4000
    page_numbers = range(1, total)
    categories = ['Books', 'Behavioral Sciences', 'Relationships']
    # if page_num==total:
    #     temp_book_list = book_list[page_num*100:]
    # elif page_num>total:
    #     return("no more books!")
    # else:
    #     temp_book_list = book_list[page_num*100:(page_num+1)*100]
    return render_template("search.html", results=book_list, page_numbers=page_numbers, categories=categories)

@app.route("/book/<asin>")
def info(asin):
    book_info=mongoService.Mg().get_all_info(asin)[0]
    results = SQLservice.SQL_db().get_review(asin)
    rating = np.mean([review[2] for review in results])
    return render_template("info.html", book_info=book_info, reviews=results, rating=rating)

@app.route("/dashboard")
def dashboard():
    return(render_template("dashboard.html"))

@app.route("/login")
def login():
    return(render_template("login.html"))

@app.route("/registration")
def registration():
    return(render_template("registration.html"))

@app.route("/search")
def search():
    return(render_template("search.html"))



if __name__=="__main__":
    app.run(debug=True)

    

