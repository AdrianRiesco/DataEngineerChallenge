# Import libraries
from flask import Flask, redirect, url_for, render_template, request, flash, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "eroijfeoUhouILFE8YOhr21NDfJHKDBCDFsds" # The secret key could be stored in a .env file and avoid loading it to a public repository
app.permanent_session_lifetime = timedelta(days=1) # Maximum time a session can keep opened is 1 day

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		username = request.form["login_username"]
		password = request.form["login_password"]
		session["username"] = username
		session["password"] = password
		flash(f"You have been sucesfully logged in, {username}! :)", "info")
		return redirect(url_for("myfiles", user = username))
	else:
		if "username" in session:
			flash("Already logged in :)")
			username = session["username"]
			return redirect(url_for("myfiles", user = username))
		return render_template("login.html")

@app.route("/myfiles")
def myfiles():
	if "username" in session:
		username = session["username"]
		return render_template("myfiles.html", user = username)
	else:
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	if "username" in session:
		username = session["username"]
		flash(f"You have been sucesfully logged out, {username}! :)", "info")
	session.pop("username", None)
	session.pop("password", None)
	return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug = True)