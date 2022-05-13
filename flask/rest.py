# Import libraries
import pymysql
from app import app
from db import mysql
from flask import jsonify

@app.route('/')
def users():
    conn = mysql.connect()

    my_cursor = conn.cursor(pymysql.cursors.DictCursor)
    my_cursor.execute("SELECT * FROM user")

    rows = my_cursor.fetchall()

    resp = jsonify(rows)
    resp.status_code = 200

    return resp

@app.route('/')
def users():
    conn = mysql.connect()

    my_cursor = conn.cursor(pymysql.cursors.DictCursor)
    my_cursor.execute("SELECT * FROM user")

    rows = my_cursor.fetchall()

    resp = jsonify(rows)
    resp.status_code = 200

    return resp

if __name__ == "__main__":
    app.run(debug=True)