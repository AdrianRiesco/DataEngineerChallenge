# Import libraries
from flask import Flask
from app import app, getMysqlCon, executeQuery, get_minioPublicPolicy, home, login, signin, myfiles, delete_file, logout
import pytest
import os

@pytest.fixture()
def create_app():
	fixture
	flask_app.config['SECRET_KEY'] = "eroijfeoUhouILFE8YOhr21NDfJHKDBCDFsds" # The secret key could be stored in a .env file and avoid loading it to a public repository
	flask_app.config['SESSION_PERMANENT'] = False
	flask_app.config['MINIO'] = os.getenv("MINIO","localhost:9000")
	flask_app.config['PREFIX'] = os.getenv("MINIO_PREFIX","http://localhost:9000/")

	return flask_app

def test_home_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/' page is requested (GET)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/')
		assert response.status_code == 200
		assert b'Image Repository Shopify Challenge' in response.data

def test_home_page_post():
	'''
	GIVEN a configured flask application
	WHEN the '/' page is posted to (POST)
	THEN check that the response returns a 405 status code
	'''

	with app.test_client() as test_client:
		response = test_client.post('/')
		assert response.status_code == 405
		assert b'Image Repository Shopify Challenge' not in response.data

def test_login_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/login' page is requested (GET)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/login')
		assert response.status_code == 200
		assert b'User Login' in response.data

def test_login_page_post():
	'''
	GIVEN a configured flask application
	WHEN the '/login' page is posted to (POST)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/login')
		assert response.status_code == 200
		assert b'User Login' in response.data

def test_signin_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/signin' page is requested (GET)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/signin')
		assert response.status_code == 200
		assert b'User Register' in response.data

def test_signin_page_post():
	'''
	GIVEN a configured flask application
	WHEN the '/signin' page is posted to (POST)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/signin')
		assert response.status_code == 200
		assert b'User Register' in response.data

def test_myfiles_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/myfiles' page is requested (GET)
	THEN check that the response is valid  (redirect)
	'''

	with app.test_client() as test_client:
		response = test_client.get('/myfiles')
		assert response.status_code == 302

def test_myfiles_page_post():
	'''
	GIVEN a configured flask application
	WHEN the '/myfiles' page is posted to (POST)
	THEN check that the response is valid (redirect)
	'''

	with app.test_client() as test_client:
		response = test_client.get('/myfiles')
		assert response.status_code == 302

def test_delete_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/delete' page is requested (GET)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/delete')
		assert response.status_code == 405

def test_delete_page_post():
	'''
	GIVEN a configured flask application
	WHEN the '/delete' page is posted to (POST)
	THEN check that the response is valid (redirect)
	'''

	with app.test_client() as test_client:
		response = test_client.get('/delete')
		assert response.status_code == 405

def test_logout_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/logout' page is requested (GET)
	THEN check that the response is valid (redirect)
	'''

	with app.test_client() as test_client:
		response = test_client.get('/logout')
		assert response.status_code == 302

def test_logout_page_post():
	'''
	GIVEN a configured flask application
	WHEN the '/logout' page is posted to (POST)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/logout')
		assert response.status_code == 302