import os
from util import *
from sql import *
# from nlp import *
from flask import Flask, request, jsonify
from flask_cors import CORS

HOST = '0.0.0.0'
PORT = '8090'
app = Flask(__name__)
api_v1_cors_config = {
  "origins": ["*"]
}
CORS(app)

os.system("clear")

@app.route("/")
def hello():
    return "Success"

@app.route("/sign_up" , methods = ["POST"])
def sign_up():
    data = request.json
    email = data["email"]
    password = data["password"]
    company = data["company"]
    name = data["name"]
    if not isValidEmail(email):
        return jsonify({"status": INVALID_EMAIL})
    if not isValidPassword(password):
        return jsonify({"status": INVALID_PASSWORD})
    if findUserByEmail(email):
        return jsonify({"status": USER_EXISTS})
    salt = bcrypt.gensalt().decode()
    hashed = getPasswordHash(salt, password)
    addUser(email, name, company, salt, hashed)
    return jsonify({"status": SUCCESS, "token": getTokenByEmail(email)})

@app.route("/login", methods = ["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    if not isValidEmail(email):
        return jsonify({"status": INVALID_EMAIL})
    if not isValidPassword(password):
        return jsonify({"status": INVALID_PASSWORD})
    user = findUserByEmail(email)
    if not user:
        return jsonify({"status": USER_NOT_FOUND})
    hashed = getPasswordHash(user[3], password)
    if hashed != user[4]:
        return jsonify({"status": WRONG_PASSWORD})
    return jsonify({"status": SUCCESS, "token": getTokenByEmail(email)})

@app.route("/get_all_user", methods=['GET'])
def get_all_users():
    token = request.headers.get('Authorization')
    user = getUserByToken(token)
    if not user:
        return jsonify({"status": TOKEN_NOT_FOUND})
    users = getAllUsers()
    ans = [{"email": user[0], "name": user[1], "company": user[2]} for user in users]
    return jsonify({"status": SUCCESS, "data": ans})

@app.route("/get_user_info", methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization')
    user = getUserByToken(token)
    if not user:
        return jsonify({"status": TOKEN_NOT_FOUND})
    email = getEmailByToken(token)
    print (email)
    user = findUserByEmail(email)
    print (user)
    ans = ans = {"email": user[0], "name": user[1], "company": user[2]}
    return jsonify({"status": SUCCESS, "user": ans})


@app.route("/delete_user", methods=['POST'])
def delete_user():
    token = request.headers.get('Authorization')
    user = getUserByToken(token)
    if not user:
        return jsonify({"status": TOKEN_NOT_FOUND})
    email = request.json["email"]
    user = findUserByEmail(email)
    if not user:
        return jsonify({"status": USER_NOT_FOUND})
    deleteUser(email)
    return jsonify({"status": SUCCESS})

@app.route("/change_user_info", methods=['POST'])
def change_user_info():
    token = request.headers.get('Authorization')
    user = getUserByToken(token)
    if not user:
        return jsonify({"status": TOKEN_NOT_FOUND})
    email = str(user[0])
    data = request.json
    if ("current_password" and "new_password") in data.keys():
        current_password = data["current_password"]
        hashed = getPasswordHash(user[3], current_password)
        if hashed != user[4]:
            return jsonify({"status": WRONG_PASSWORD})
        if not isValidPassword(data["new_password"]):
            return jsonify({"status": INVALID_PASSWORD})
        changeUserInfo(email, "password", data["new_password"])
        return jsonify({"status": SUCCESS})
    if "name" in data.keys():
        changeUserInfo(email, "name", data["name"])
    if "company" in data.keys():
        changeUserInfo(email, "company", data["company"])
    return jsonify({"status": SUCCESS})

@app.route("/check_token", methods=['POST'])
def check_token():
    token = request.headers.get('Authorization')
    print("token" + token)
    user = getUserByToken(token)
    if not user:
        return jsonify({"status": TOKEN_NOT_FOUND})
    return jsonify({"status": SUCCESS})

@app.route("/generate_text", methods=['POST'])
def generate_text():
    token = request.headers.get('Authorization')
    print("token" + token)
    user = getUserByToken(token)
    if not user:
        return jsonify({"status": TOKEN_NOT_FOUND})
    data = request.json
    keyword = data["keyword"]
    length = data["length"]
    ans = generateText(keyword, length)
    return jsonify({"status": SUCCESS, "data": ans})

if __name__ == "__main__":
    print("deploy on {}:{}".format(HOST, PORT))
    app.run(host=HOST, port = PORT, debug = True)
