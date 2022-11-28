# My personal touch is letting the user change the passowrd
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTO INCREMENT NOT NULL, user_id INTEGER NOT NULL, post TEXT NOT NULL, 'time' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():   
    posts = db.execute("SELECT * FROM posts SORT BY time")
    return render_template("index.html", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        # lookup symbol and return quoet
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if quote is not None:
            return render_template("quoted.html", quote=quote)
        else:
            return apology("symbol doesn't exist")
    if request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username is blank or existing
        username = request.form.get("username")
        existing_users = db.execute("SELECT username FROM users")
        if not username:
            return apology("must type in a username!")
        elif username in [user["username"] for user in existing_users]:
            return apology("this username already exists")

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check if passwords are blank and are matching
        if not password or not confirmation:
            return apology("must type in password")
        elif password != confirmation:
            return apology("passwords must match")

        # hash the password and insert username and password into database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        return redirect("/login")

    if request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        # check that shares and stock chosen are valid
        stock = request.form.get("symbol")
        shares = request.form.get("shares")
        if not stock:
            return apology("pick a stock")
        if not shares:
            return apology("pick how many shares")
        shares = int(shares)

        # get the number of shares user owns and compare with how many they're selling
        shares_owned = db.execute("SELECT shares FROM portfolio WHERE id = ? AND symbol = ?",
                                  session["user_id"], stock)[0]["shares"]
        print(shares_owned)
        if shares > shares_owned:
            return apology("you don't own that many shares")

        # insert transaction into history
        price = lookup(stock)["price"]
        now = datetime.now()
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        db.execute("INSERT INTO history (id, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], stock, -shares, price, dt_string)

        # update portfolio and delete row if number of shares < 1
        db.execute("UPDATE portfolio SET shares = ? WHERE id = ? AND symbol = ?",
                   shares_owned-shares, session["user_id"], stock)
        db.execute("DELETE FROM portfolio WHERE shares < 1")

        # update user's balance
        gain = price * shares
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance+gain, session["user_id"])

        return redirect("/")

    if request.method == "GET":
        # display form of stocks that can be sold
        stocks = db.execute("SELECT symbol FROM portfolio WHERE id = ?", session["user_id"])
        stocks = [stock["symbol"] for stock in stocks]
        return render_template("sell.html", stocks=stocks)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        # check if passwords are blank and are matching
        if not new_password or not confirmation:
            return apology("must type in password")
        elif new_password != confirmation:
            return apology("passwords must match")

        # hash the password and insert username and password into database
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, session["user_id"])
        return redirect("/login")

    if request.method == "GET":
        return render_template("change_password.html")