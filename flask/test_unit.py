# Import libraries
from flask import Flask
from app import app, executeQuery, get_minioPublicPolicy
from minio import Minio
import mysql.connector
import pytest
import json
import os, io

@pytest.fixture(scope='module')
def new_minio_client():
	minio_client = Minio(app.config['MINIO'],
      secure=False,
      access_key=os.getenv("MINIO_ROOT_USER","minio"),
      secret_key=os.getenv("MINIO_ROOT_PASSWORD","minio123"))

	return minio_client

def test_minio_make_remove_bucket(new_minio_client):
	'''
	GIVEN a minio client
	WHEN we create a bucket and then removed
	THEN check that the bucket exists and then not
	'''
	if not new_minio_client.bucket_exists("testbucket"):
		new_minio_client.make_bucket("testbucket")
	assert new_minio_client.bucket_exists("testbucket")

	new_minio_client.remove_bucket("testbucket")
	assert not new_minio_client.bucket_exists("testbucket")


def test_minio_add_remove_object(new_minio_client):
	'''
	GIVEN a minio client
	WHEN we add an object to a bucket and then remove it
	THEN check that the object exists in the bucket and then not
	'''

	value = "Random text to upload to MinIO"
	value_bytes = value.encode('utf-8')
	value_stream = io.BytesIO(value_bytes)

	if not new_minio_client.bucket_exists("testbucket"):
		new_minio_client.make_bucket("testbucket")

	new_minio_client.put_object("testbucket", "dummyObject", value_stream , length=len(value_bytes))
	assert any("dummyObject" in obj.object_name for obj in new_minio_client.list_objects("testbucket"))


	new_minio_client.remove_object("testbucket", "dummyObject")
	assert "dummyObject" not in new_minio_client.list_objects("testbucket")

	new_minio_client.remove_bucket("testbucket")