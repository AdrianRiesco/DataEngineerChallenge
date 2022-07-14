# Import libraries
from flask import Flask
from app import app, getMysqlCon, executeQuery, get_minioPublicPolicy, home, login, signin, myfiles, delete_file, logout
from forms import LoginForm, RegisterForm, UploadForm
import pytest
import os

def test_home_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/' page is requested (GET)
	THEN check that the response is valid
	'''

	with app.test_client() as test_client:
		response = test_client.get('/')
		assert response.status_code == 200
		assert b'Image Repository' in response.data

def test_home_page_post():
	'''
	GIVEN a configured flask application
	WHEN the '/' page is posted to (POST)
	THEN check that the response returns a 405 status code
	'''

	with app.test_client() as test_client:
		response = test_client.post('/')
		assert response.status_code == 405
		assert b'Image Repository' not in response.data

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
		response = test_client.post('/login')
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
		response = test_client.post('/signin')
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
		response = test_client.post('/myfiles')
		assert response.status_code == 302

def test_delete_page_get():
	'''
	GIVEN a configured flask application
	WHEN the '/delete' page is requested (GET)
	THEN check that the response is valid (method not allowed)
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
		response = test_client.post('/delete')
		assert response.status_code == 302

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
	THEN check that the response is valid (method not allowed)
	'''

	with app.test_client() as test_client:
		response = test_client.post('/logout')
		assert response.status_code == 405