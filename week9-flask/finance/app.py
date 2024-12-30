import os
import logging
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    transactions_db = db.execute(
        "SELECT symbol,SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]
    return render_template("index.html", database=transactions_db, cash=cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")
        if not symbol:
            return apology("Must provide symbol", 400)
        stock = lookup(symbol.upper())
        if stock is None:
            return apology("Invalid symbol", 400)
        try:
            shares = int(shares_input)
            if shares <= 0:
                return apology("Shares must be a positive integer", 400)
        except ValueError:
            return apology("Shares must be a positive integer", 400)
        transaction_value = shares * stock["price"]
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        if user_cash < transaction_value:
            return apology("Not enough cash", 400)
        updated_cash = user_cash - transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
        date = datetime.datetime.now()
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
            user_id, stock["symbol"], shares, stock["price"], date
        )
        flash(f"Bought {shares} shares of {symbol.upper()} for {usd(transaction_value)}")
        return redirect("/")

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions = db.execute("""
        SELECT symbol, shares, price, date
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
    """, user_id)
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        stock = lookup(symbol)
        print("Lookup result:", stock)
        if stock == None:
            return apology("test symbol", 400)
        return render_template("quoted.html", stock=stock)
    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        if not username:
            return apology("Username is required")
        elif not password:
            return apology("Password is required")
        elif not confirmation:
            return apology("Password confirmation is required")
        if password != confirmation:
            return apology('Passwords do not match')
        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect('/')
        except:
            return apology("Username has already been registered!")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols_user])
    else:
        symbol = request.form.get("symbol")
        shares_input = request.form.get("shares")
        if not symbol:
            return apology("Must provide a Stock Symbol")
        stock = lookup(symbol.upper())
        if stock is None:
            return apology("Please Provide Valid Stock Symbol")
        try:
            shares = int(shares_input)
            if shares <= 0:
                return apology("Please enter a positive number of shares you would like to sell")
        except ValueError:
            return apology("Please enter a valid integer for shares")
        user_id = session["user_id"]
        user_shares = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        if not user_shares or user_shares[0]["total_shares"] < shares:
            return apology("You don't have this amount of shares")
        transaction_value = shares * stock["price"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        uptd_cash = user_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], -shares, stock["price"], date)
        flash(f"Stock Sold! || Cash: ${uptd_cash:.2f}")
        return redirect("/")

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "GET":
        return render_template("addcash.html")
    else:
        new_cash = int(request.form.get("new_cash"))
        if not new_cash:
            return apology("Please enter a cash amount")
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        uptd_cash = user_cash + new_cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)
        flash(f"${new_cash} added to account")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
