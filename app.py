from flask import Flask, render_template, request, session, redirect
from database import Database
import json
import datetime

db = Database()

app = Flask(__name__)

@app.route('/')
def home():
    if session.get('user', None) is None:
        return login()

    return render_template("home.html", user=session['user'])

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/restaurants')
def restaurants():
    if session.get('user', None) is None:
        return login()

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
    if session.get('user', None) is None:
        return login()

    restList = db.getRestRating()

    return render_template("reviews.html", restList=restList)

@app.route('/write-review', methods=['GET'])
def write_review():
    if session.get('user', None) is None:
        return login()

    rid = request.args.get("rid")
    rname = db.getRestaurantNameFromId(rid)[0][0]
    reviewList = db.getRestaurantReviews(rid)

    return render_template("write_review.html", rid=rid, reviewList=reviewList, rname=rname)

@app.route('/review', methods=['POST', 'GET'])
def rest_review():
    if session.get('user', None) is None:
        return login()

    rid = request.args.get("rid")
    rating = request.args.get("rating")
    comment = request.args.get("comment")
    email = session['email']

    if int(rating) > 5 or int(rating) < 1:
        return render_template("error.html", message="Please submit vaild rating from 1-5")

    db.writeReview(rid, rating, comment, email)

    return render_template("success.html", message="Review submitted successfully")

@app.route('/order-list')
def orders():
    if session.get('user', None) is None:
        return login()

    restList = db.getRestaurantNames()
    return render_template("order-list.html", restList=restList)

@app.route('/rest-order')
def rest_order():
    if session.get('user', None) is None:
        return login()

    rid = request.args.get("rid")
    itemList = db.getRestaurantMenu(rid)

    return render_template("orders.html", menu=itemList, rid=rid)

@app.route('/order-submit')
def order_submit():
    if session.get('user', None) is None:
        return login()

    rid = request.args.get("rid")

    if request.args.get('Delivery') == 'Y':
        delivery = 'Y'
        pickup = 'N'
    else:
        delivery = 'N'
        pickup = 'Y'

    #create restaurant order
    orderid = db.createRestaurantOrder(session['email'], delivery, pickup)[0][0]
    print(orderid)
    if orderid == None:
        return render_template("error.html")

    itemList = db.getRestaurantMenu(rid)
    for item in itemList:
        itemCount = request.args.get(item[1])
        foodName = item[1]
        if int(itemCount) > 0:
            ret = db.createRestaurantODetails(orderid, rid, foodName, itemCount)
            if not ret:
                print("Error, returning")
                return render_template("error.html")

    message = "Order placed successfully. Your order number is " + str(orderid)

    return render_template("success.html", message=message)

@app.route('/logout')
def logout():
    session['user'] = None
    session['email'] = None
    return render_template("login.html")

@app.route('/submit_login', methods=['POST'])
def submit_login():
    username = str(request.form.get("uname"))
    password = str(request.form.get("pswd"))

    res = db.authenticateUser(username,password)
    if res:
        #log user in
        user = db.getUserName(username)
        session['email'] = username
        session['user'] = user
        return home()
    else:
        #return to login
        return login()

    return home()

@app.route('/search', methods=['GET'])
def search():
    if session.get('user', None) is None:
        return login()

    rname = request.args.get("search")
    restaurant = {}
    restaurant['name'] = None

    restaurants = db.getRestaurants()
    for rest in restaurants:
        if rname == str(rest[1]):
            restaurant = {
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
            }
            break

    return render_template("search.html", restaurant=restaurant)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/submit-register', methods=['POST'])
def submit_register():
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    street_no = request.form.get("st_no")
    street_name = request.form.get("st_name")
    city = request.form.get("city")
    state = request.form.get("state")
    zip = request.form.get("zip")
    password = request.form.get("password1")

    ret = db.addNewUser(fname, lname, email, street_no, street_name, city, state, zip, password)

    if ret:
        # log user in
        user = db.getUserName(email)
        session['email'] = email
        session['user'] = user
        return home()
    else:
        # return to login
        return login()

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
