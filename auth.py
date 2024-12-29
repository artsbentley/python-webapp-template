from fastapi import Request
import jwt
from dotenv import load_dotenv
import os

class RequiresLoginException(Exception):
    pass

load_dotenv()

KEY = os.getenv('KEY')

def to_token(username):
    return jwt.encode({'username' : username}, KEY, algorithm="HS256")

def from_token(token):
    return jwt.decode(token, KEY, algorithms=["HS256"])['username']

def get_user(request: Request):
    token = request.cookies.get("username")
    if token is None:
        raise RequiresLoginException
    try:
        user = from_token(token)
        return user
    except Exception:
        raise RequiresLoginException
