# Shopify Data Engineer Challenge
This Image Repository is made for the Shopify Data Engineer Internship challenge.

## Description
This project is an image repository that allows the user to perform the following actions:
 - Create a user by entering name, username, email and password.
 - Login with username and password.
 - Upload images with public visibility (all users can see them) or private (only the user who uploaded them can see them).
 - Delete images from your user folder (private) or from the public folder.

This image repository has been built using **Docker** and **Docker Compose** to run containers with services from **Flask** (web application framework), **MySQL** (relational database), and **MinIO** (S3-compatible object-oriented storage).
While Flask supports the web application, MySQL stores user and image information, and MinIO stores the images themselves in its buckets.

When a user is created, the data (name, username, email, and encrypted password) is sent to MySQL and a bucket for that user is created in MinIO. When creating users, the only field that must be different is the username (that is, the email field can match).
On the other hand, when an image is added or modified, its data (filename, username, and visibility) is added to MySQL and the file uploaded to the MinIO public or user bucket, depending on the selected visibility. A user can only have one image with each name within their private repository (images with the same name cannot be uploaded). Regarding the public repository, as it is shared by all users, it cannot contain images with the same name even if they are uploaded by different users. That is, a user cannot upload an image with the name "image.png" if an image with that name already exists in the public repository.

## Prerequisites
 - Git
 - Docker
 - Docker-compose

## Usage
Clone the project and execute docker-compose.
```
$ git clone git@github.com:AdrianRiesco/DataEngineerChallenge.git
...
$ cd docker
$ docker-compose up
```

## Additional features
Because this project has been developed using containers, it makes it easy to extend the functionality of the application by adding other services.

If our goal is to modify existing services, the database can be easily altered via the initial build script, the MinIO configuration can be modified in docker-compose, and the web folder organization allows for new changes such as adding views or forms.

Regarding the possible functionalities and improvements to be added, the following have emerged during its development:
 - Check password strength level and restrict weak passwords.
 - Limit the maximum weight of the images.
 - Add the ability to upload and delete images in bulk.
 - Expand the range to other types of files, taking advantage of the object-oriented storage service used.
 - Add the possibility that users can comment or give feedback to public images.

 >Hope you like the project. Adrian.