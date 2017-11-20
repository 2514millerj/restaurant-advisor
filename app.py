from flask import Flask, render_template, request
from database import Database

db = Database

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/submit_login', methods=['POST'])
def submit_login():
    username = request.form.get("uname")
    password = request.form.get("pwd")
    return render_template("home.html")

if __name__ == '__main__':
    app.run()
