# Image Classification API
This is an image classification API that utilizes Inception v3 to determine what is in an image from an image URL provided.
User details are registered to a MongoDB, where each user has a select amount of credits to run classification of images. Once
the credits run out, the user will have to pay for further credits (outside this projects scope). The admin has permissions
to refill their tokens through the API.

## Tools Used
* Flask
* Docker
* Docker-Compose
* PyMongo
* BCrypt
* Postman
* AWS EC2

## Initial Setup and Pre-requisites
You will need to have Docker, Docker-Compose, and MongoDB installed on your machine.
```sh
# Clone the repository
git clone git@github.com:keithdavis92/portfolio.git

cd portfolio/FlaskImageRecognitionApp
```

## Getting Started
At the top level of the project, you can run the following commands in order to get 
the project up and running: 
```sh
cd portfolio/FlaskImageRecognitionApp
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

Once the user is registered, you can send another post request to classify an image. Each user, when registered, 
is given 6 tokens to classify with. You can find an JPEG image URL through Google. Paste this into the request and the
classification will be done. I will add a link for convenience:


In Postman, enter the following:
```http request
POST localhost:5000/classify
```
```json
{
    "username": "test",
    "password": "secure",
    "url": "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg"
}
```