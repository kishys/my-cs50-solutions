"""
https://cs50.harvard.edu/x/2023/labs/9/
"""

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        db.execute("INSERT INTO birthdays (first_name, last_name, day, month, year) VALUES (?, ?, ?, ?, ?)", first_name, last_name, day, month, year)

        return redirect("/")

    else:
        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=birthdays)
