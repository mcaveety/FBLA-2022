import os
import random
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

import archive
import events
import prizes
import users

# Allows environment variables to be accessed
load_dotenv()


# An instance of the Flask class is created
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
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


# (Temp) resets login info for testing
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
    user_data = users.lookup_user(session['student_number'])
    return render_template("dashboard.html", user_data=user_data)


# Loads event(s) for selecting
@app.route("/events", methods=["GET", "POST"])
@check_session()
def events_page():
    events_data = events.load_events()

    if request.method == "GET":
        confirm_error = request.args.get('confirm_error', "")

        # If an event is selected
        if request.args.get('num', None):
            if events_data[int(request.args['num'])]:
                return render_template(
                    "event_info.html",
                    event=events_data[int(request.args['num'])],
                    confirm_error=confirm_error
                )

        return render_template("events.html", events_data=events_data)

    # Checks if attendance was confirmed
    if request.method == "POST":
        if request.form.get('confirm_attend', None):
            users.add_attended(session.get('student_number', None), int(request.args['num']), )
            return redirect(url_for('events_page'))

        # Displays error not confirmed
        else:
            return redirect(url_for(
                'events_page',
                num=int(request.args['num']),
                confirm_error="Please confirm your attendance before submission."
            ))


# Leaderboard page
@app.route("/leaderboard", methods=["GET", "POST"])
@check_session()
def leaderboard_page():
    file_path = users.users_path

    if request.method == "POST":
        if request.form['btn'] == "Archive Current Quarter":
            user_info = archive.archive_file(session)

            for key in user_info:
                session[key] = user_info[key]

        elif request.form['btn'] == "Select":
            file_path = users.resource_path(request.form.get('select_qy'))

    users_data = users.sort_leaderboard(file_path=file_path)
    qy_list = list(archive.collect_paths())

    return render_template("leaderboard.html", users_data=users_data, qy_list=qy_list)


# Login and Sign-Up page
@app.route("/login", methods=["GET", "POST"])
def login_page():

    # Logged-in users are redirected
    if session.get('student_number'):
        return redirect(url_for('dashboard_page'))

    # Displays login & signup options (and errors, if any)
    if request.method == "GET":
        error_sign_up = request.args.get('error_sign_up', "")
        error_login = request.args.get('error_login', "")
        return render_template(
            "login.html",
            error_sign_up=error_sign_up,
            error_login=error_login
        )

    # On form submission
    if request.method == "POST":

        # User tries to login
        if request.form['btn'] == "Login":

            # If account exists, login
            if users.check_user(request.form.get('student_number')):
                session['student_number'] = request.form.get('student_number')
                user_info = users.lookup_user(session['student_number'])

                for key in user_info:
                    session[key] = user_info[key]

                return redirect(url_for('dashboard_page'))

            # If account doesn't exist, display error
            else:
                return redirect(url_for(
                    'login_page',
                    error_login=f"Student Number {request.form.get('student_number')} does not exist."
                ))

        # User tries to sign up
        elif request.form['btn'] == "Sign Up":
            new_user_info = {}

            for element_name, value in request.form.items():
                new_user_info[element_name] = value

            # Removes unneeded key
            new_user_info.pop('btn')

            # If student number is new, sign up
            if users.add_user(new_user_info):
                session['student_number'] = request.form.get('student_number')
                return redirect(url_for('dashboard_page'))

            # If student number is in use, display error
            else:
                return redirect(url_for(
                    'login_page',
                    error_sign_up=f"Student Number {request.form.get('student_number')} is in use."
                ))


@app.route("/prizes", methods=["GET", "POST"])
@check_session()
def prizes_page():
    prizes_list = users.open_file(prizes.prizes_path)

    if request.method == "GET":
        error = request.args.get('error', "")
        message = request.args.get('message', "")
        return render_template("prizes.html", prizes=prizes_list, error=error, message=message)

    if request.method == "POST":
        try:
            credits_cost = int(request.form.get('prize_select'))
        except TypeError:
            return redirect(url_for('prizes_page', error="Please select a prize."))

        if credits_cost > session['credits']:
            return redirect(url_for(
                'prizes_page',
                error=f"Insufficient point balance. You need {credits_cost - session['credits']} more points.")
            )
        else:
            # Updates user's credit total
            session['credits'] -= credits_cost
            user = users.lookup_user(session['student_number'])
            user['credits'] = session['credits']
            users.update_user(session['student_number'], user)

            # random 6 digit code generator from https://stackoverflow.com/a/47504953
            redeem_code = f'Present redemption code #{random.randrange(1, 10**6):06} to a school administrator to receive your prize!'

            return redirect(url_for('prizes_page', message=redeem_code))


# Error Handler code from
# https://flask.palletsprojects.com/en/1.0.x/patterns/errorpages/
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('splash_page'))


# Flask app is run, allowing access of the webpage at localhost:8080 in a web browser

app.run(host="localhost", port=port)
