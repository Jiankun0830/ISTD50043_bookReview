from flask import url_for,redirect,Flask,render_template,request
import SQLservice
import mongoService
import numpy as np
import pandas as pd



app=Flask(__name__)



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
    book_list=mongoService.Mg().get_all_books()
    total=len(book_list)//20
    if page_num==total:
        temp_book_list = book_list[page_num*20:]
    elif page_num>total:
        return("no more books!")
    else:
        temp_book_list = book_list[page_num*20:(page_num+1)*20]
    return render_template("search.html", results=temp_book_list)

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

@app.route("/addbook", methods=['POST', 'GET'])
def addBook():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Apply':
            asin = request.form['field1']
            title = request.form['field2']
            brand = request.form['field3']
            price = float(request.form['field4'])
            url = request.form['field5']
            alsoBought = request.form['field6'].strip().split(" ")
            alsoViewed = request.form['field7'].strip().split(" ")
            buyAfterViewing = request.form['field8'].strip().split(" ")
            boughtTogether = request.form['field9'].strip().split(" ")
            category = [request.form['field10'].strip().split(" ")]
            mg = mongoService.Mg()
            mg.add_book(asin, title=title, price=price, imUrl=url, category=category, brand=brand, also_bought=alsoBought, also_viewed=alsoViewed, buy_after_viewing=buyAfterViewing, bought_together=boughtTogether)
            return(render_template("addbook.html"))
    else:
        return(render_template("addbook.html"))



if __name__=="__main__":
    app.run(debug=True)

