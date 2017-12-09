from flask import Flask, render_template, request, session
from database import Database

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
    return render_template("restuarants.html")

@app.route('/reviews')
def reviews():
    return render_template("reviews.html")

@app.route('/orders')
def orders():
    return render_template("orders.html")

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
        return render_template("home.html")
    else:
        #return to login
        return render_template("login.html")

    return render_template("home.html")

if __name__ == '__main__':
    app.run()
