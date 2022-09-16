from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json
import os

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
users = db["Users"]

def userExists(username):
    if users.count_documents({"Username":username}) == 0:
        return False
    else:
        return True

def passwordVerified(username, password):
    if not userExists(username):
        return False

    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if userExists(username):
            retJson = {
                "status": 301,
                "msg" : "Invalid username"
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "Successfully signed up to the API!"
        }

        return jsonify(retJson)

def verifyPassword(username, password):
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def generateReturnDictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }

def verifyCredentials(username, password):
    if not userExists:
        return generateReturnDictionary(301, "Username does not exist"), True

    correct_pw = verifyPassword(username, password)
    if not correct_pw:
        return generateReturnDictionary(302, "Password is incorrect for the username"), True

    return None, False

class Classify(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        tokens = users.find({
            "Username":username
        })[0]["Tokens"]
        if tokens == 0:
            return jsonify(generateReturnDictionary(303, "Not enough tokens!"))

        # Download an image from the url and write into a file called temp.jpg
        r = requests.get(url)
        retJson = {}
        with open('temp.jpg', 'wb') as f:
            f.write(r.content)
            proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait()
            with open("text.txt") as f:
                retJson = json.load(f)

        users.update_one({
            "Username": username
        },{
            "$set":{
                "Tokens": tokens-1
            }
        })

        return retJson

class Refill(Resource):
    def post(self):
        # Obtain the data from the post
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        user_to_update = postedData["user_to_update"]
        num_tokens = postedData["num_tokens"]

        if username == "admin":
            retJson, error = verifyCredentials(username, password)
            if error:
                return jsonify(retJson)

            if userExists(user_to_update):
                users.update_one({
                    "Username": user_to_update
                },{
                    "$set":{
                        "Tokens": num_tokens
                    }
                })

            return jsonify(generateReturnDictionary(200, "User tokens have been updated"))
        else:
            return jsonify(generateReturnDictionary(304, "User does not have the correct access rights to perform this operation"))

api.add_resource(Refill, '/refillTokens')
api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
