from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Purchases Handle Request")
    

    cur = g.db.cursor();
    logger.debug(request.args.get('title'))
    
    try:
        title = request.form["title"]
        print(title)
        cur.execute("INSERT INTO purchases (title, price) SELECT title, price FROM books WHERE title = '" + title + "';")
        cur.commit()
        cur.close()

        logger.debug("Added book to cart.")
        return json_response(data={"message" : "Succesfully added book to purchases."}, status = 200)

    except:
        return json_response(data={"message": "Error occured while reading from database."}, status=500)



