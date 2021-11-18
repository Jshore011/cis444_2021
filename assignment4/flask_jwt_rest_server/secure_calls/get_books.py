from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")


    cur = g.db.cursor();
    try:
        cur.execute("select * from books;")
        booklist=cur.fetchall()
        cur.close()
    except:
        logger.debug("cannot read from database")
        return json_response(data={"message": "Error occured while reading from database."}, status=500)

    count=0
    books = '{"books":['
    for b in booklist:
        if b[0] < len(booklist) :
            books += '{"title":"'+str(b[1]) + '","price":"' + str(b[2]) + '"},'
        else:
            books += '{"title":"'+str(b[1]) + '","price":"' + str(b[2]) + '"}'
    books += "]}"
    #print(message)
    print("sending silly token")
    
    return json_response( token = create_token(  g.jwt_data ) , books = {})

