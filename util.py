import bcrypt
import re
import jwt
import lepl.apps.rfc3696
import hashlib
from sql import *

PRIVATE_KEY = "MyVeryStr0ngKey@@"
TOKEN_ALGORITHM = "HS256"

SUCCESS = 0
USER_EXISTS = 1
USER_NOT_FOUND = 2
WRONG_PASSWORD = 3
INVALID_EMAIL = 4
INVALID_PASSWORD = 5
TOKEN_NOT_FOUND = 6
WRONG_PARAM = 7

def getPasswordHash(password, salt):
    return hashlib.sha512(str(password + salt).encode()).hexdigest()

def isValidEmail(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def isValidPassword(password):
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if re.search("\s", password):
        return False
    return True

def getTokenByEmail(email):
    jwtToken = jwt.encode({"email": email}, PRIVATE_KEY, TOKEN_ALGORITHM)
    return jwtToken.decode()
        
def getEmailByToken(token):
    return jwt.decode(str.encode(token), PRIVATE_KEY, TOKEN_ALGORITHM)["email"]

def getUserByToken(token):
    email = getEmailByToken(token)
    user = findUserByEmail(email)
    if not user:
        return None
    return user