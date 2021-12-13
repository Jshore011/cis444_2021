from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger
import json

def handle_request():
    logger.debug("Get dash Handle Request")


    cur = g.db.cursor();
    try:
        cur.execute("select * from users;")
        user=cur.fetchall()
        cur.close()
    except:
        logger.debug("cannot read from database")
        return json_response(data={"message": "Error occured while reading from database."}, status=500)

    count=0
    message = '{"user":['
    for i in user:
        if i[0] < len(user) :
            message += '{"name":"'+str(i[3]) + '","city":"' + str(i[4]) + '","state":"' + str(i[5]) + '"},'
        else:
            message += '{"name":"'+str(i[3]) + '","city":"' + str(i[4]) + '","state":"' + str(i[5]) + '"}'
    message += "]}"
    print(message)
    #print("sending silly token")
    
    return json_response( token = create_token(  g.jwt_data ) , data = json.loads(message))
