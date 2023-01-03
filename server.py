from flask import Flask, render_template, request

# An instance of the Flask class is created
app = Flask(__name__)
port = 8080


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Flask app is run, allowing access of the webpage
app.run(host="localhost", port=port)
