from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import json
from tools.logging import logger

def handle_request():
    logger.debug("Get Pet Report Handle Request")


    cur = g.db.cursor()
    try:
        cur.execute("select * from logs;")
        logs=cur.fetchall()
        cur.close()
    except:
        print("cannot read from database")
        return json_response(data={"message": "Error occured while reading from database."}, status=500)

    count=1
    message = '{"logs":['
    for i in logs:

        if count < len(logs) :
            message += '{"PetName":"'+str(i[0]) + '","type":"' + str(i[1]) +'","comment":"' + str(i[3]) +'"},'
            count=count+1
        else:
            message += '{"PetName":"'+str(i[0]) +'","type":"' + str(i[1]) +'","comment":"' + str(i[3]) +'"}'
    message += "]}"
    print(message)
    #print("sending silly token")

    
    return json_response( token = create_token(  g.jwt_data ) , data = json.loads(message))
