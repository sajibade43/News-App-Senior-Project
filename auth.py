from flask_httpauth import HTTPTokenAuth
from flaskext.mysql import MySQL

from user import User
from __init__ import app

mysql = MySQL(app)

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    return User.check_token(token, mysql) if token else None
