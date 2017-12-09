from flask import Flask, render_template, request, session, redirect
from database import Database
import json

db = Database()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", user="Brian")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/restaurants')
def restaurants():
    restaurants = db.getRestaurants()
    restArray = []
    for rest in restaurants:
        restArray.append({
                'name': str(rest[1]),
                'phone': str(rest[2]),
                'email': str(rest[3]),
                'hours': str(rest[4]),
                'diningType': str(rest[5]),
                'streetNo': str(rest[6]),
                'city': str(rest[7]),
                'zip': str(rest[8]),
                'pricerange': str(rest[9]),
                'deliveryFlag': str(rest[10]),
                'outdoorsFlag': str(rest[11])
        })
    return render_template("restaurants.html", restaurantData=restArray, user=session['user'])

@app.route('/review-list')
def reviews():
    restList = db.getRestaurantNames()
    return render_template("reviews.html", restList=restList)

@app.route('/review', methods=['GET'])
def rest_review():
    return render_template("rest_review.html")

@app.route('/order-list')
def orders():
    orderList = db.getRestaurantNames()
    return render_template("orders.html", orderList=orderList)

@app.route('/order', methods=['GET'])
def rest_order():
    return render_template("rest_order.html")

@app.route('/logout')
def logout():
    return render_template("logout.html")

@app.route('/submit_login', methods=['POST'])
def submit_login():
    username = str(request.form.get("uname"))
    password = str(request.form.get("pswd"))
    print(username,password)

    res = db.authenticateUser(username,password)
    if res:
        #log user in
        user = db.getUserName(username)
        session['user'] = user
        print(user)
        return home()
    else:
        #return to login
        return render_template("login.html")

    return render_template("home.html")

@app.route('/search', methods=['GET'])
def search():
    return search_result()

@app.route('/search-result')
def search_result():
    return render_template("search.html")

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
