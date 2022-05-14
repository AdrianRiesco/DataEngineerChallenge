# Import libraries
from flask import Flask, redirect, url_for, render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from datetime import timedelta
from forms import LoginForm, RegisterForm, UploadForm
import mysql.connector
import json
import os

app = Flask(__name__)

app.secret_key = "eroijfeoUhouILFE8YOhr21NDfJHKDBCDFsds" # The secret key could be stored in a .env file and avoid loading it to a public repository
#app.permanent_session_lifetime = timedelta(days=1) # Maximum time a session can keep opened is 1 day

# Get connection with the MySQL database
def getMysqlCon():
	return mysql.connector.connect(user='root', host='database', port='3306', password='root', database='mainDB')

bcrypt = Bcrypt(app)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Home page
@app.route("/")
def home():
	return render_template("index.html")

# Login page
@app.route("/login", methods=["POST", "GET"])
def login():
	login_form = LoginForm()
	upload_form = UploadForm()
	print("*** LOGIN METHOD ***")
	if login_form.validate_on_submit():
		#session.permanent = True

		username = login_form.username.data
		password = login_form.password.data

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
			
			existing_username = response[0]
			existing_name = response[1]
			existing_password = response[3]

			print(password)
			print(existing_password)
			print(bcrypt.generate_password_hash(password))
			if (username == existing_username) and (bcrypt.check_password_hash(existing_password, password)):

				session["name"] = existing_name
				session["username"] = username

				flash(f"You have been sucesfully logged in, {existing_name}! :)", category="success")
				return redirect(url_for("myfiles", user = existing_name, form = upload_form))

		flash(f"Error! User or password invalid", category="error")
		return render_template("login.html", form = login_form)

	if "name" in session:
		flash("Already logged in :)")
		name = session["name"]
		return redirect(url_for("myfiles", user = name, form = upload_form))

	return render_template("login.html", form = login_form)

# Signin page
@app.route("/signin", methods=["POST", "GET"])
def signin():
	print("*** SIGNIN METHOD ***")
	register_form = RegisterForm()
	upload_form = UploadForm()
	if register_form.validate_on_submit():
		#session.permanent = True
		name = register_form.name.data
		username = register_form.username.data
		email = register_form.email.data
		password = register_form.password.data

		hashed_password = bcrypt.generate_password_hash(password)

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
			flash(f"There is already an user registered with the same username! :)", category="info")
			return redirect(url_for("signin", form = register_form))
		else:
			session["name"] = name
			session["username"] = username

			# Add user to the database
			sql = """insert into users (username, name, email, password) values (%s, %s, %s, %s)"""
			my_cursor.execute(sql, (username, name, email, hashed_password))
			db.commit()
			my_cursor.close()
			db.close()

			flash(f"You have been sucesfully registered, {name}! :)", category="success")
			return redirect(url_for("myfiles", user = name, form = upload_form))

	return render_template("signin.html", form = register_form)

# Main page
@app.route("/myfiles", methods=["POST", "GET"])
def myfiles():
	print("*** MYFILES METHOD ***")
	login_form = LoginForm()
	upload_form = UploadForm()

	# Check if the user is logged
	if "name" in session:
		name = session["name"]
		username = session["username"]

		# Check if the form was valid
		if upload_form.validate_on_submit():
			# Get image data
			filename = secure_filename(upload_form.file.data.filename)
			visibility = upload_form.visibility.data

			# Check if the file is already stored
			db = getMysqlCon()

			my_cursor = db.cursor()
			sql = """select * from files where username=%s and filename=%s"""
			my_cursor.execute(sql, (username, filename))

			response = my_cursor.fetchone()
			print(response)

			# Check if the file is already stored
			if response is not None:
				# Close the cursor and the connection
				my_cursor.close()
				db.close()

				# Render the page again
				flash(f"Sorry, you cannot upload the same image twice", category="error")
				return render_template("myfiles.html", user = name, form = upload_form)
			else:
				# Save the image
				upload_form.file.data.save(os.path.join(UPLOAD_FOLDER, filename))
				print("Imagen guardada")
				print(UPLOAD_FOLDER)
				print(visibility)
				print("*")

				# Insert the data in the database
				sql = """insert into files (username, filename, visibility) values (%s, %s, %s)"""
				my_cursor.execute(sql, (username, filename, visibility))
				db.commit()
				my_cursor.close()
				db.close()

				# Render the page again
				flash(f"File uploaded!", category="success")
				return render_template("myfiles.html", user = name, form = upload_form)

		# Render the page again
		print(upload_form.errors)
		return render_template("myfiles.html", user = name, form = upload_form)

	return redirect(url_for("login", form = login_form))

@app.route("/logout")
def logout():
	print("*** LOGOUT METHOD ***")
	login_form = LoginForm()
	if "name" in session:
		name = session["name"]
		flash(f"You have been sucesfully logged out, {name}! :)", category="info")
	session.pop("name", None)
	session.pop("username", None)
	return redirect(url_for("login", form = login_form))

if __name__ == "__main__":
	app.run(debug = True)