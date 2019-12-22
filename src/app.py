from flask import send_from_directory, url_for, redirect, Flask, render_template, request, session
from flask_session import Session
import SQLservice
import SQLservice_User
import mongoService
import mongoService_visualize
from utils import *
import numpy as np
import pandas as pd
import string
import hashlib
import json

app = Flask(__name__)
app.config['DEBUG'] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mg = mongoService.Mg()
mg_visualize = mongoService_visualize.Mg()

with open('categories.json') as f:
    data = json.load(f)

@app.route('/data/<path:path>')
def send_data(path):
    return send_from_directory('data', path)

@app.route("/plot")
def plot():
    #mg.plot_test()
    mg_visualize.plot_trend()
    mg_visualize.plot_heat(choice=0)
    mg_visualize.plot_heat(choice=1)

    if 'user' in session: 
        is_admin = session['isadmin']
        if is_admin: 
            cat_book_list = mg.get_highest_viewed_books()
        else:
            cat_book_list = mg.get_highest_viewed_books_by_user(userid=session['userid'])

    if 'user' in session: is_admin = session['isadmin']
    return render_template("heat_plot.html", cat_book_list=cat_book_list, isadmin=is_admin,
                           in_session=('user' in session))

@app.route("/home_page")
def home_page():
    cats = ["Mystery, Thriller & Suspense", "Science Fiction & Fantasy", "Action & Adventure", "Love & Romance",
            "Business & Money", "Health, Fitness & Dieting", "Professional & Technical", "Administration & Policy",
            "Dictionaries & Thesauruses", "Biographies & Memoirs"]

    book_list = mongoService.Mg().get_bestsellers()

    cat_book_list = []
    for cat in cats:
        top_in_cat = mongoService.Mg().get_highest_rank_books(cat)
        cat_book_list.append(top_in_cat)
    is_admin = False
    login = False
    if 'user' in session: 
        is_admin = session['isadmin']
        login = True 
    return render_template("home_page.html", results=book_list[:-3], catbook_list=cat_book_list, isadmin=is_admin, login=login,
                           in_session=('user' in session))


@app.route("/")
def home():
    # return render_template("dashboard.html")
    return redirect(url_for('home_page'))


@app.route("/bookinfo")
def book_list():
    # if 'user' not in session:
    #     return redirect(url_for('login'))
    return str(mg.get_all())


@app.route("/bookinfo/<page_num>/<category>")
def book_list_page(page_num, category):
    # if 'user' not in session:
    #    return redirect(url_for('login'))
    page_num = int(page_num)
    book_list = mongoService.Mg().get_all_books(page_num, category)
    # TODO: what is this for?
    page_numbers = list(range(1, 4000))
    if 'user' in session:
        add_log(request.method, request.url, "all_book_returned", session['userid'], session['isadmin'], mg)
    return render_template("booklist.html", results=book_list, page_numbers=page_numbers, categories=data)


@app.route("/searchpage", methods=["POST"])
def searchpage():
    # if 'user' not in session:
    #     return redirect(url_for('login'))
    keyword = request.form.get("searchpage")
    keyword = ''.join([o for o in keyword if o not in string.punctuation])

    return redirect(url_for("book_list_page", page_num=int(keyword), category="all"))

    # book_list = mongoService.Mg().get_all_books(int(keyword), "all")
    # page_numbers = list(range(1, 4000))
    # add_log(request.method, request.url, "all_book_returned", session['userid'], session['isadmin'], mg)
    # return render_template("booklist.html", results=book_list, page_numbers=page_numbers, categories=data)


@app.route("/book/<asin>", methods=["GET", "POST"])
def info(asin):
    # if request.method == "GET":
    #     if 'user' not in session:
    #         return redirect(url_for('login'))

    if request.method == "POST":
        if 'user' not in session:
            add_log(request.method, request.url, None, None, None, mg)
            return redirect(url_for('login'))
        title = request.form.get("title")
        comment = request.form.get("comment")
        my_rating = request.form.get("rating")
        add_log(request.method, request.url, {"user_comment": comment, "rating": my_rating}, session['userid'],
                session['isadmin'], mg)
        SQLservice.SQL_db().add_review(asin=asin, overall=my_rating, reviewerName=session['user'],
                                       reviewerID=session['userid'], summary=title, reviewText=comment)

    also_bought = mongoService.Mg().get_related_books(asin, "also_bought")
    also_viewed = mongoService.Mg().get_related_books(asin, "also_viewed")
    buy_after_viewing = mongoService.Mg().get_related_books(asin, "buy_after_viewing")
    book_info = mongoService.Mg().get_all_info(asin)[0]
    results = SQLservice.SQL_db().get_review(asin)
    rating = round(np.mean([review[2] for review in results]), 2)
    if 'user' in session:
        add_log(request.method, request.url, {"bookNumber": asin, "number_of_reviews": len(results), "rating": rating},
                session['userid'], session['isadmin'], mg)

    return render_template("info.html", book_info=book_info, reviews=results, rating=rating, also_bought = also_bought, also_viewed=also_viewed, buy_after_viewing=buy_after_viewing)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        add_log(request.method, request.url, None, session['userid'], session['isadmin'], mg)
        return redirect(url_for('home_page'))

    message = None

    if request.method == "POST":
        usern = request.form.get("username")
        passw = request.form.get("password")
        passw_hash = hashlib.md5(passw.encode('utf-8')).hexdigest()
        user_id, verify_passw_hash, isadmin = SQLservice_User.SQL_User_db().get_usr_info(usern)
        if passw_hash == verify_passw_hash:
            session['user'] = usern
            session['userid'] = user_id
            session['isadmin'] = True if isadmin else False
            add_log(request.method, request.url, {"usern": usern, "passw_hash": passw_hash, "login_sucessful": True},
                    None, None, mg)
            return redirect(url_for('home_page'))
        else:
            message = "Username or password is incorrect."
            add_log(request.method, request.url, {"usern": usern, "passw_hash": passw_hash, "login_sucessful": False},
                    None, None, mg)
    return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('userid', None)
    session.pop('isadmin', None)
    add_log(request.method, request.url, {"logout_sucessful": True}, None, None, mg)
    return redirect(url_for('home_page'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if 'user' in session:
        add_log(request.method, request.url, None, session['userid'], session['isadmin'], mg)
        return redirect(url_for('home_page'))

    message = None

    if request.method == "POST":
        usern = request.form.get("username")
        passw = request.form.get("password")
        passw_hash = hashlib.md5(passw.encode('utf-8')).hexdigest()
        result = SQLservice_User.SQL_User_db().add_user(usern, passw_hash)
        user_id = SQLservice_User.SQL_User_db().get_usr_info(usern)[0]
        if result:
            session['user'] = usern
            session['userid'] = user_id
            session['isadmin'] = False
            add_log(request.method, request.url, {"usern": usern, "passw_hash": passw_hash, "register_sucessful": True},
                    None, None, mg)
            return redirect(url_for('home_page'))
        else:
            message = "Username already exists."
            add_log(request.method, request.url,
                    {"usern": usern, "passw_hash": passw_hash, "register_sucessful": False}, None, None, mg)

    return render_template("registration.html", message=message)


@app.route("/search", methods=["POST"])
def search():
    # if 'user' not in session:
    #     return redirect(url_for('login'))
    keyword = request.form.get("searchbox")
    keyword = ''.join([o for o in keyword if o not in string.punctuation])
    results = mg.search_book(keyword)
    session['isadmin'] = 1  # delete this
    if 'user' in session:
        add_log(request.method, request.url, {"search_keyword": keyword, "results_length": len(results)},
                session['userid'], session['isadmin'], mg)
    return render_template("search.html", results=results)


@app.route("/addbook", methods=['POST', 'GET'])
def addBook():
    is_admin = False
    if 'user' in session: is_admin = session['isadmin']
    if not is_admin:
        add_log(request.method, request.url, None, None, None, mg)
        return redirect(url_for('login'))

    if request.method == 'POST':
        if request.form['submit_button'] == 'Submit':
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
            add_log(request.method, request.url,
                    {"book_information": {"title": title, "price": price, "category": category}}, session['userid'],
                    session['isadmin'], mg)
            return render_template("addsuccess.html")
    else:
        return render_template("addbook.html")


@app.route("/addsuccess", methods=['POST', 'GET'])
def addsuccess():
    return render_template("addsuccess.html")


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
