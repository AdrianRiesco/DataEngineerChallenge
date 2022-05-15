# Import libraries
from flask import Flask, redirect, url_for, render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, UploadForm, DeleteForm
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from datetime import timedelta
from minio import Minio
import mysql.connector
import json
import os, io

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = "eroijfeoUhouILFE8YOhr21NDfJHKDBCDFsds" # The secret key could be stored in a .env file and avoid loading it to a public repository
app.config['SESSION_PERMANENT'] = False
#app.permanent_session_lifetime = timedelta(days=1) # Maximum time a session can keep opened is 1 day
app.config['MINIO'] = os.getenv("MINIO","localhost:9000")
app.config['PREFIX'] = os.getenv("MINIO_PREFIX","http://localhost:9000/")

# Minio client configuration
client = Minio(app.config['MINIO'],
      secure=False,
      access_key=os.getenv("MINIO_ROOT_USER","minio"),
      secret_key=os.getenv("MINIO_ROOT_PASSWORD","minio123"))

bcrypt = Bcrypt(app)

# Get connection with the MySQL database
def getMysqlCon():
	""" This function returns the connection to the MySQL database

	Returns:
		MySQLConnection

	"""
	return mysql.connector.connect(user='root', host='database', port='3306', password='root', database='mainDB')

# Execute a search query
def executeQuery(sql, par, option):
	""" This function execute a query with the sql and parameters sent and option selected

	Args:
		sql (string): SQL statement for the query
		par (tuple): arguments to include in the SQL query
		option (string): type of query to send

	Returns:
		response (list of tuples) : response from the query (empty if commiting changes to the database)

	"""
	# Create connection and cursor
	db = getMysqlCon()
	my_cursor = db.cursor()

	# Execute query
	my_cursor.execute(sql, par)

	# Get the response or commit the changes
	if option == "get_all":
		response = my_cursor.fetchall()
	elif option == "get_one":
		response = my_cursor.fetchone()
	elif option == "modify":
		response = []
		db.commit()

	# Close cursor and connection
	my_cursor.close()
	db.close()

	return response

# Get MinIO bucket public policy
def get_minioPublicPolicy(bname):
	""" This function returns the read-write MinIO bucket policy for the bucket_name selected

	Args:
		bname (string): bucket name

	Returns:
		minio_publicPolicy (json) : public policy for the bucket

	"""
	minio_publicPolicy = {
	    "Version": "2012-10-17",
	    "Statement": [
	        {
	            "Effect": "Allow",
	            "Principal": {"AWS": "*"},
	            "Action": [
	                "s3:GetBucketLocation",
	                "s3:ListBucket",
	                "s3:ListBucketMultipartUploads",
	            ],
	            "Resource": "arn:aws:s3:::" + bname,
	        },
	        {
	            "Effect": "Allow",
	            "Principal": {"AWS": "*"},
	            "Action": [
	                "s3:GetObject",
	                "s3:PutObject",
	                "s3:DeleteObject",
	                "s3:ListMultipartUploadParts",
	                "s3:AbortMultipartUpload",
	            ],
	            "Resource": "arn:aws:s3:::" + bname + "/*",
	        },
	    ],
	}

	return minio_publicPolicy

# Home page
@app.route("/")
def home():
	return render_template("index.html")

# Login page
@app.route("/login", methods=["POST", "GET"])
def login():
	print("*** LOGIN METHOD ***")

	# Create forms
	login_form = LoginForm()
	upload_form = UploadForm()
	delete_form = DeleteForm()

	# Get all public images (including those of the current user)
	public_images = client.list_objects("publicimagesbucket")

	# Check if user already loged (session information is still present)
	if "name" in session:
		name = session["name"]
		username = session["username"]

		# Get user's private images
		private_images = client.list_objects(username.lower())

		flash("Already loged in :)")
		return redirect(url_for("myfiles", user = name, username = username, form_upload = upload_form, form_delete = delete_form, prefix_public = (app.config['PREFIX'] + "publicimagesbucket"),
			prefix_private = (app.config['PREFIX'] + username.lower()), public_files = public_images, private_files = private_images))

	# Check if user trying to log in
	if login_form.validate_on_submit():
		#session.permanent = True

		username = login_form.username.data
		password = login_form.password.data

		# Check if this username exists (use lower to avoid the creation of similar usernames)
		sql = """select * from users where lower(username)=%s"""
		par = (username.lower(),)
		response = executeQuery(sql, par, "get_one")

		if response is not None:
			# Get the user information
			existing_username, existing_name, existing_mail, existing_password = response

			# Check if username and hashed password match
			if (username == existing_username) and (bcrypt.check_password_hash(existing_password, password)):

				# Add user info to the session
				session["name"] = existing_name
				session["username"] = username

				# Get user's private images
				private_images = client.list_objects(username.lower())

				flash(f"You have been sucesfully logged in, {existing_name}! :)", category="success")
				return render_template("myfiles.html", user = existing_name, username = username, form_upload = upload_form, form_delete = delete_form, prefix_public = (app.config['PREFIX'] + "publicimagesbucket"),
					prefix_private = (app.config['PREFIX'] + username.lower()), public_files = public_images, private_files = private_images)

		flash(f"Error! User or password invalid", category="error")
		return render_template("login.html", form = login_form)

	return render_template("login.html", form = login_form)

# Signin page
@app.route("/signin", methods=["POST", "GET"])
def signin():
	print("*** SIGNIN METHOD ***")
	register_form = RegisterForm()
	upload_form = UploadForm()
	delete_form = DeleteForm()

	if register_form.validate_on_submit():
		#session.permanent = True
		name = register_form.name.data
		username = register_form.username.data
		email = register_form.email.data
		password = register_form.password.data

		hashed_password = bcrypt.generate_password_hash(password)

		# Check if user exists
		sql = """select * from users where username=%s"""
		par = (username,)
		response = executeQuery(sql, par, "get_one")

		if response is not None:
			flash(f"There is already an user registered with the same username! :)", category="info")
			return redirect(url_for("signin", form = register_form))
		else:
			# Save session data
			session["name"] = name
			session["username"] = username

			# Add user to the database
			sql = """insert into users (username, name, email, password) values (%s, %s, %s, %s)"""
			par = (username, name, email, hashed_password)
			response = executeQuery(sql, par, "modify")

			# Get all public images
			public_images = client.list_objects("publicimagesbucket")

			print(client.get_bucket_policy("publicimagesbucket"))
			# Create the user bucket
			if not client.bucket_exists(username.lower()):
				print(username.lower())
				client.make_bucket(username.lower())
				client.set_bucket_policy(username.lower(), json.dumps(get_minioPublicPolicy(username.lower())))
			private_images = []

			flash(f"You have been sucesfully registered, {name}! :)", category="success")
			return redirect(url_for("myfiles", user = name, username = username, form_upload = upload_form, form_delete = delete_form, prefix_public = (app.config['PREFIX'] + "publicimagesbucket"),
					prefix_private = (app.config['PREFIX'] + username.lower()), public_files = public_images, private_files = private_images))

	return render_template("signin.html", form = register_form)

# Main page where the images are displayed
@app.route("/myfiles", methods=["POST", "GET"])
def myfiles():
	print("*** MYFILES METHOD ***")
	login_form = LoginForm()
	upload_form = UploadForm()
	delete_form = DeleteForm()

	# Check if the user is logged
	if "name" in session:
		name = session["name"]
		username = session["username"]
		print("1. User in session")
		# Get all public images (including those of the current user)
		public_images = client.list_objects("publicimagesbucket")

		# Check if the form was valid
		if upload_form.validate_on_submit():
			# Get image data
			print("2. Upload image form")
			filename = secure_filename(upload_form.file.data.filename)
			visibility = upload_form.visibility.data

			# Check if the file is already stored by the user
			sql = """select * from files where username=%s and filename=%s"""
			par = (username, filename)
			response1 = executeQuery(sql, par, "get_one")

			# If user wants to store a public file, check if there is a file with the same name in the public bucket
			if visibility == "public":
				sql = """select * from files where filename=%s and visibility=%s"""
				par = (filename, "public")
				response2 = executeQuery(sql, par, "get_one")
			else:
				response2 = None

			# Check if the file is already stored
			if response1 is not None or response2 is not None:
				print("* Imagen NO guardada")
				
				# Get user's private images
				private_images = client.list_objects(username.lower())

				flash(f"Sorry, you cannot upload the same image twice", category="error")
				
			else:
				print("* Imagen guardada")

				# Save image to minIO public or user bucket
				if visibility == "public":
					result = client.put_object(
				        bucket_name="publicimagesbucket",
				        object_name=filename,
				        data=upload_form.file.data,
				        length=-1,
				        part_size=10*1024*1024,
				        content_type='image')
				else:
					result = client.put_object(
				        bucket_name=username.lower(),
				        object_name=filename,
				        data=upload_form.file.data,
				        length=-1,
				        part_size=10*1024*1024,
				        content_type='image')

				# Add image data to MySQL database
				sql = """insert into files (username, filename, visibility) values (%s, %s, %s)"""
				par = (username, filename, visibility)
				response = executeQuery(sql, par, "modify")

				# Get user's private images
				private_images = client.list_objects(username.lower())

				flash(f"File uploaded!", category="success")
		else:
			# Get user's private images
			private_images = client.list_objects(username.lower())

			# Check if the user wants to delete an image
			if delete_form.validate_on_submit():
				print("3. Delete image form")
				# Get form data
				filename = secure_filename(delete_form.filename.data)
				visibility = secure_filename(delete_form.visibility.data)

				print(filename)
				print(visibility)

				# Remove image from database and minIO (considering if public or private)
				if visibility == "public":
					sql = """delete from files where filename=%s and visibility=%s"""
					par = (filename, visibility)
					response = executeQuery(sql, par, "modify")

					client.remove_object("publicimagesbucket", filename)
				else:
					sql = """delete from files where username=%s and filename=%s"""
					par = (username, filename)
					response = executeQuery(sql, par, "modify")

					client.remove_object(username.lower(), filename)

		print("4. Redirect")
		# Render the page again
		return render_template("myfiles.html", user = name, username = username, form_upload = upload_form, form_delete = delete_form, prefix_public = (app.config['PREFIX'] + "publicimagesbucket"),
			prefix_private = (app.config['PREFIX'] + username.lower()), public_files = public_images, private_files = private_images)

	# Redirect to login
	return redirect(url_for("login", form = login_form))

@app.route("/delete", methods = ["POST"])
def delete_file():
	print("*** DELETE_FILE METHOD ***")
	# Create the forms
	login_form = LoginForm()
	upload_form = UploadForm()
	delete_form = DeleteForm()

	if "name" in session:
		name = session["name"]
		username = session["username"]
		print("1. User logged")
		# Get all public images (including those of the current user)
		public_images = client.list_objects("publicimagesbucket")

		# Get user's private images
		private_images = client.list_objects(username.lower())

		# Get filename and visibility
		filename = secure_filename(request.form["filename"])
		visibility = request.form["visibility"]
		print(filename)
		print(visibility)
		# Remove image from database and minIO (considering if public or private)
		if visibility == "public":
			sql = """delete from files where filename=%s and visibility=%s"""
			par = (filename, visibility)
			response = executeQuery(sql, par, "modify")

			client.remove_object("publicimagesbucket", filename)
		else:
			sql = """delete from files where username=%s and filename=%s"""
			par = (username, filename)
			response = executeQuery(sql, par, "modify")

			client.remove_object(username.lower(), filename)

		return redirect(url_for("myfiles", user = name, username = username, form_upload = upload_form, form_delete = delete_form, prefix_public = (app.config['PREFIX'] + "publicimagesbucket"),
			prefix_private = (app.config['PREFIX'] + username.lower()), public_files = public_images, private_files = private_images))

	return redirect(url_for("login", form = login_form))

@app.route("/logout")
def logout():
	# Create the form
	login_form = LoginForm()

	if "name" in session:
		name = session["name"]
		flash(f"You have been sucesfully logged out, {name}! :)", category="info")

	# Remove session data
	session.pop("name", None)
	session.pop("username", None)
	return redirect(url_for("login", form = login_form))

if __name__ == "__main__":
	app.run(debug = True)