from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get add_pet_log Handle Request")
    
    

    cur = g.db.cursor();
    logger.debug(request.form['petLogName'])
    logger.debug(request.form['logType'])
    logger.debug(request.form['comments'])

    
    try:

        cur.execute("INSERT INTO logs (name, type, comment) values('" + request.form['petLogName'] + "','" + request.form['logType'] + "', '" + request.form['comments'] + "');")
        cur.close()
        g.db.commit();
        
        logger.debug("Added pet Log")
        return json_response(token = create_token( g.jwt_data), data =("success"))

    except:
        return json_response(data={"message": "Error occured while reading from database."}, status=500)
