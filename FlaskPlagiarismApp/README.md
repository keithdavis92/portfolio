# Plagiarism API
This is a similarity API to check for similarity between different documents based on Udemy lecture from "Python REST APIs with Flask, Docker, MongoDB, and AWS DevOps"

There are some minor refactors, primarily within the Refill method. 

## Tools Used
* Docker
* Docker Compose
* MongoDB
* PyMongo
* Flask 
* BCrypt
* SpaCy 

## Initial Setup and Pre-requisites
You will need to have Docker, Docker-Compose, and MongoDB installed on your machine.
```sh
# Clone the repository
git clone git@github.com:keithdavis92/portfolio.git

cd portfolio/FlaskPlagiarimApp
```

## Getting Started
At the top level of the project, you can run the following commands in order to get 
the project up and running: 
```sh
cd portfolio/FlaskPlagiarimApp
sudo docker-compose build
sudo docker-compose up
```
The project should now be up and running, so you can open up Postman. In Postman, you can run a POST 
request to register a user. You will need to point to:```localhost:5000/register```
You can paste in the following JSON string with to send the request:
```json
{
    "username": "test",
    "password": "secure"
}
```

Once the user is registered, you can send another post request detect similarities. Each user, when registered, 
is given 6 tokens to run detections with:

In Postman, enter the following:
```http request
POST localhost:5000/detection
```
```json
{
    "username": "test",
    "password": "secure",
    "document1": <string-to-compare>,
    "document2": <string-to-compare>
}
```