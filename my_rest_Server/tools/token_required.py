import jwt
from functools import wraps
from flask import request, redirect, g
from flask_json import FlaskJSON, JsonReeor, json_response, as_json

from tools.logging import logger
from tools.get_aws_secrets import get_secrets

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        secrets = get_secrets()
        auth_headers = request.headers.get('Authorization', '').split(':')

        invalid_msg = {
                'message': 'Invalid token. Registration and/or authentication required',
                'authenticated': False
                }
        expired_msg = {
                'message': 'Expired token. Reauthentication required.',
                'authenticated' : False
                }

        if len(auth_handlers) != 2:
            return json_response(status_=401, message = invalid_msg)

        try:
            token = auth_headers[1]
            logger.debug("Got token")
            data = jwt.decode(token, secrets['JWT'], algorithms = ['HS256'])
            #set global jwt_data
            g.jwt_data = data
            return f( *args, **kwargs)
        except jwt.ExpiredSignatureError:
            #401 is unauthorized HTTP status code
            return json_response(status_=401, message=expired_msg)
        except (jwt.InvalidTokenError, Exception) as e:
            logger.debug(e)
            return json_response(status_=401, message-expired_msg)

        return _verify