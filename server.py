import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_session import Session

# Allows environment variables to be accessed
load_dotenv()


# An instance of the Flask class is created
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
Session(app)
port = 8080


@app.route("/")
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard_page():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        data = request.form.items()
        for element_name, value in request.form.items():
            print(element_name, value)
        return redirect(url_for("dashboard_page"))


# Flask app is run, allowing access of the webpage
app.run(host="localhost", port=port)
