# My personal touch is letting the user change the passowrd
import os

import cs50
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
db = cs50.SQL("sqlite:///users.db")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, post TEXT NOT NULL, 'time' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")


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
    posts = db.execute("SELECT * FROM posts ORDER BY time DESC")
    return render_template("index.html", posts=posts)


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST":
        id = session["user_id"]
        post = request.form.get("post")
        db.execute("INSERT INTO posts (user_id, post) VALUES (?, ?)", id, post)
        return redirect("/")
    else:
        return render_template("post.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']
    return render_template("profile.html", username=username)

@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    return render_template("feedback.html")


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


@app.route("/change_username", methods=["GET", "POST"])
@login_required
def change_username():
    if request.method == "POST":
        new_username = request.form.get("new_username")
        confirmation = request.form.get("confirmation")
        if not new_username or not confirmation:
            return apology("must type in a username!")
        if new_username != confirmation:
            apology("usernames don't match")
        current_username = db.execute("SELECT username FROM users")
        if new_username == current_username:
            apology("Your new username is the same as your old ")
        existing_users = db.execute("SELECT username FROM users")

        if new_username in [user["username"] for user in existing_users]:
            return apology("this username already exists")
        db.execute("UPDATE users SET username = ? WHERE id = ?", new_username, session["user_id"])
        return redirect("/")

    if request.method == "GET":
        return render_template("change_username.html")
