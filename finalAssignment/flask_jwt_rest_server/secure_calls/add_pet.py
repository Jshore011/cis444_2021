from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get add_pet Handle Request")
    

    cur = g.db.cursor();
    logger.debug(request.form['petname'])
    logger.debug(request.form['age'])
    logger.debug(request.form['breed'])

    
    try:

        cur.execute("INSERT INTO pets (name, age, breed) values('" + request.form['petname'] + "','" + request.form['age'] + "', '" + request.form['breed'] + "');")
        cur.close()
        g.db.commit();
        
        logger.debug("Added pet")
        return json_response(token = create_token( g.jwt_data), data =("success"))

    except:
        return json_response(data={"message": "Error occured while reading from database."}, status=500)
