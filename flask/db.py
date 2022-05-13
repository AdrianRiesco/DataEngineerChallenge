# Import libraries
from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config["MYSQL_DB_USER"] = "root"
app.config["MYSQL_DB_PASSWORD"] = "root"
app.config["MYSQL_DB_DB"] = "mainDB"
app.config["MYSQL_DB_HOST"] = "db"

mysql.init_app(app)