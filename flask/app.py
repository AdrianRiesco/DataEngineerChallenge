# Import libraries
from flask import Flask, redirect, url_for, render_template, request, flash, session
from datetime import timedelta
import mysql.connector
import json

app = Flask(__name__)

app.secret_key = "eroijfeoUhouILFE8YOhr21NDfJHKDBCDFsds" # The secret key could be stored in a .env file and avoid loading it to a public repository
app.permanent_session_lifetime = timedelta(days=1) # Maximum time a session can keep opened is 1 day

# Get connection with the MySQL database
def getMysqlCon():
	return mysql.connector.connect(user='root', host='database', port='3306', password='root', database='mainDB')

# Home page
@app.route("/")
def home():
	return render_template("index.html")

# Login page
@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		username = request.form["login_username"]
		password = request.form["login_password"]
		session["username"] = username
		session["password"] = password

		# Check if user exists
		db = getMysqlCon()

		my_cursor = db.cursor()
		sql = """select * from users where username=%s"""

		my_cursor.execute(sql, (username,))
		response = my_cursor.fetchone()
		print(response)
		my_cursor.close()
		db.close()
		
		if response is not None:
			existing_username = response[2]
			existing_password = response[4]

			if (username == existing_username) and (password == existing_password):
				flash(f"You have been sucesfully logged in, {username}! :)", "info")
				return redirect(url_for("myfiles", user = username))

		flash(f"Error! User or password invalid")
		return render_template("login.html")
	else:
		if "username" in session:
			flash("Already logged in :)")
			username = session["username"]
			return redirect(url_for("myfiles", user = username))
		return render_template("login.html")

# Signin page
@app.route("/signin", methods=["POST", "GET"])
def signin():
	if request.method == "POST":
		session.permanent = True
		name = request.form["signin_name"]
		username = request.form["signin_username"]
		email = request.form["signin_email"]
		password = request.form["signin_password"]
		session["username"] = username
		session["password"] = password

		# Check if user exists
		db = getMysqlCon()

		my_cursor = db.cursor()
		sql = """select * from users where username=%s"""

		my_cursor.execute(sql, (username,))
		response = my_cursor.fetchone()
		print(response)

		if response is not None:
			my_cursor.close()
			db.close()
			flash(f"There is already an user registered with the same username! :)", "info")
			return redirect(url_for("signin.html"))
		else:
			# Add user to the database
			sql = """insert into users (name, username, email, password) values (%s, %s, %s, %s)"""
			my_cursor.execute(sql, (name, username, email, password))
			db.commit()
			my_cursor.close()
			db.close()
			flash(f"You have been sucesfully registered, {name}! :)", "info")
			return redirect(url_for("myfiles", user = name))
	else:
		return render_template("signin.html")

# Main page
@app.route("/myfiles", methods=["POST", "GET"])
def myfiles():
	email = None
	if "username" in session:
		username = session["username"]

		if request.method == "POST":
			email = request.form["email"]
		else:
			if "email" in session:
				email = session["email"]
		return render_template("myfiles.html", user = username, email = email)
	else:
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	if "username" in session:
		username = session["username"]
		flash(f"You have been sucesfully logged out, {username}! :)")
	session.pop("username", None)
	session.pop("password", None)
	session.pop("email", None)
	return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug = True)