import jwt
import datetime
from flask import g
from tools.logging import logger

#create's a JWT token that expires after 30 minuites. return's token
def create_token(token_data):
    token_data['exp'] = datetime.datetime.utcnow() + datetime.timedelts(days=0,minutes=30)
    token_data['iat'] = datetime.datetime.utcnow()

    return jwt.encode( token_data , g.secrets['JWT'], algorithm="HS256")
