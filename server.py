import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from functools import wraps
import users


# Allows environment variables to be accessed
load_dotenv()


# An instance of the Flask class is created
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
Session(app)
port = 8080


# Check if user is logged in for pages requiring a logged-in account
def check_session():
    def decorator(function):
        @wraps(function)
        def wrapper():
            if not session.get('student_number'):
                return redirect(url_for('login_page'))
            return function()
        return wrapper
    return decorator


@app.route("/reset")
def reset_session():
    session.clear()
    return redirect(url_for('login_page'))


# Splash page for the website w/ basic info
@app.route("/")
def splash_page():
    return render_template("base.html")


# Account dashboard for logged-in users
@app.route("/dashboard", methods=["GET", "POST"])
@check_session()
def dashboard_page():
    return render_template("dashboard.html", student_number=session['student_number'])


# Login and Sign-Up page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if session.get('student_number'):
        return redirect(url_for('dashboard_page'))

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        new_user_info = {}
        for element_name, value in request.form.items():
            new_user_info[element_name] = value
        print(new_user_info)
        users.add_user(new_user_info)
        session['student_number'] = request.form.get('student_number')
        return redirect(url_for('dashboard_page'))


# Flask app is run, allowing access of the webpage at localhost:8080 in a web browser
app.run(host="localhost", port=port)
