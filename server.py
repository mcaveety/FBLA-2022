from flask import Flask, render_template, request, redirect, url_for

# An instance of the Flask class is created
app = Flask(__name__)
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
        return redirect(url_for("dashboard_page"))

# Flask app is run, allowing access of the webpage
app.run(host="localhost", port=port)
