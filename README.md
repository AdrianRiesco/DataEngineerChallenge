# Shopify Data Engineer Intern Challenge
This **Image Repository** is made for the Shopify Data Engineer Intern challenge. The web application has been stored on Google Cloud (Compute Engine) to make it publicly available. You can download and execute the project locally or access via [Data Engineer Challenge](http://adrianriesco.com:8000/). In case you need, the folder example_images contains some beautiful images to upload to the Image Repository.
> ℹ️ The web published is already populated with a few images in the public folder.

> ⚠️ If you face any kind of problem or the web is working slow, I encourage you to run the project in your local environment.

## Description
This project is an image repository that allows the user to perform the following actions:
 - Create a user by entering name, username, email and password.
 - Login with username and password.
 - Upload images with public visibility (all users can see them) or private (only the user who uploaded them can see them).
 - Delete images from the user folder (private) or from the public folder.

This image repository has been built using **Docker** and **Docker Compose** to run containers with services from **Flask** (web application framework), **MySQL** (relational database), and **MinIO** (S3-compatible object-oriented storage). While Flask supports the web application, MySQL stores user and image information, and MinIO stores images in its buckets.

When a user is created, the data (name, username, email, and encrypted password) is sent to MySQL and a bucket for that user is created in MinIO. When creating users, the only field that must be different is the username (that is, the email field can match).

On the other hand, when an image is added or modified, its data (filename, username, and visibility) is added to MySQL and the file uploaded to the MinIO public or user bucket, depending on the selected visibility. A user can only have one image with each name within their personal repository (images with the same name cannot be uploaded). Regarding the public repository, as it is shared by all users, it cannot contain images with the same name even if they are uploaded by different users. That is, a user cannot upload an image with the name "image.png" if an image with the same name already exists in the public repository.

## Prerequisites
 - Git
 - Docker
 - Docker-compose

## Usage
Clone the project and execute docker-compose in the command console.
```
$ git clone https://github.com/AdrianRiesco/DataEngineerChallenge.git
...
$ cd DataEngineerChallenge/docker
$ docker-compose up
```
The url to access the web application is "http://localhost:8000/". If this URL does not work, please check the command console output to identify the URL corresponding to the "web" service.

In case there is a need to reset the project after the upload (e.g., want to reset the users stored), run the following commands within the docker folder to ensure that all the services are built again:
```
$ sudo docker-compose down -v
$ sudo docker-compose up --build
```

If you reset the project, you may need to clear your browser cookies or click "Logout" once in the webapp, as the previous user session may still be present and that may trigger errors (for example, trying to to access the bucket of the user with the active session when this has been deleted by the previous command).

## Additional features
Due to the fact that this project has been developed using containers, it allows to extend the functionality of the application by adding other services and simplifies the scaling of the existing ones.

If our goal is to modify existing services, the database can be easily altered via the initial build script, the MinIO configuration can be modified in docker-compose, and the web folder organization allows for new changes such as adding views or forms.

Regarding the possible improvements and functionalities to be added, the following have emerged during its development:
 - Check password strength level and restrict weak passwords.
 - Limit the maximum weight of the images.
 - Hide the parameters shown in the URL for the redirects.
 - Separate the elements of the flask application file into different configuration and model files, and create User and File classes.
 - Add more tests, since the existing ones are only a sample and could be more numerous and cover more aspects of each service container.
 - Prevent the creation of an user account with the same name of the public bucket (filtering the name or prepopulating the database with that user).
 - Create an admin account and provide the ability to delete users or reset the project. Currently, users are removed via command line.
 - Add the ability to upload and delete images in bulk.
 - Expand the range to other types of files, taking advantage of the object-oriented storage service used.
 - Add the possibility that users can comment or give feedback to public images.

 > Hope you like the project. Adrian.
