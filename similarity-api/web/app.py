from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

# Import the Flask constructor
app = Flask(__name__)
# Initialise that this app is going to be an API
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.DocumentsDatabase
users = db["Users"]

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens

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
        username = postedData["username"] # NOTE: using single quotes instead of double as per instructions
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

class Detect(Resource):
    def post(self):
        # Obtain the data from the post
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        doc_1 = postedData["document_1"]
        doc_2 = postedData["document_2"]

        if not userExists(username):
            retJson = {
                "status": 301,
                "msg" : "Invalid username"
            }
            return jsonify(retJson)

        if not passwordVerified(username, password):
            retJson = {
                "status": 302,
                "msg" : "Invalid password"
            }
            return jsonify(retJson)

        if countTokens(username) == 0:
            retJson = {
                "status": 303,
                "msg" : "You have ran out of tokens!"
            }
            return jsonify(retJson)

        # Checks are now done so we can count detect similarities with spacy
        nlp = spacy.load("en_core_web_sm")
        doc_1 = nlp(doc_1)
        doc_2 = nlp(doc_2)

        ratio = doc_1.similarity(doc_2)

        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Successfully calculated similarity of documents"
        }

        current_tokens = countTokens(username)

        users.update_one({
            "Username": username
        },{
            "$set":{
                "Tokens": current_tokens-1
            }
        })

        return jsonify(retJson)

class Refill(Resource):
    def post(self):
        # Obtain the data from the post
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        user_to_update = postedData["user_to_update"]
        num_tokens = postedData["num_tokens"]

        if username == "admin":
            if passwordVerified(username, password):
                retJson = {
                    "status": 302,
                    "msg" : "Invalid password"
                }
                return jsonify(retJson)
            if userExists(user_to_update):
                users.update_one({
                    "Username": user_to_update
                },{
                    "$set":{
                        "Tokens": num_tokens
                    }
                })

            retJson = {
                "status": 200,
                "msg" : "User tokens have been updated"
            }
            return jsonify(retJson)
        else:
            retJson = {
                "status": 304,
                "msg" : "User does not have the correct access rights to perform this operation"
            }
            return jsonify(retJson)



api.add_resource(Refill, '/refillTokens')
api.add_resource(Register, '/register')
api.add_resource(Detect, '/detection')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
