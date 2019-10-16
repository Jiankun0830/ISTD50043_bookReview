from flask import url_for, redirect, Flask, render_template
from flask import request
from flask import url_for, redirect, Flask, render_template, request
import SQLservice
import mongoService
import numpy as np
import pandas as pd
import json

app = Flask(__name__)
app.config['DEBUG'] = True

mg = mongoService.Mg()

with open('categories.json') as f:
    data = json.load(f)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/bookinfo")
def book_list():
    return str(mg.get_all())


@app.route("/bookinfo/<page_num>/<category>")
def book_list_page(page_num, category):
    page_num = int(page_num)
    book_list = mongoService.Mg().get_all_books(page_num, category)
    page_numbers = list(range(1, 4000))
    categories = ['Books', 'Behavioral Sciences', 'Relationships']
    mg.insert_query({'results': book_list, 'page_numbers': page_numbers, 'categories': data})
    return render_template("booklist.html", results=book_list, page_numbers=page_numbers, categories=data)


@app.route("/book/<asin>", methods=["GET", "POST"])
def info(asin):
    if request.method == "POST":
        comment = request.form.get("comment")
        my_rating = request.form.get("rating")
        SQLservice.SQL_db().add_review(asin=asin, overall=my_rating, summary=comment)

    book_info = mongoService.Mg().get_all_info(asin)[0]
    results = SQLservice.SQL_db().get_review(asin)
    rating = np.mean([review[2] for review in results])
    mg.insert_query({'book_info': book_info, 'reviews': results, 'rating': rating})
    return render_template("info.html", book_info=book_info, reviews=results, rating=rating)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")


@app.route("/search")
def search():
    return render_template("booklist.html")


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
            mg.add_book(asin, title=title, price=price, imUrl=url, category=category, brand=brand,
                        also_bought=alsoBought, also_viewed=alsoViewed, buy_after_viewing=buyAfterViewing,
                        bought_together=boughtTogether)
            return render_template("addbook.html")
    else:
        return render_template("addbook.html")


if __name__ == "__main__":
    app.run()
