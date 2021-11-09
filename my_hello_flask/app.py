from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json, jsonify

import jwt
import datetime
import bcrypt
import db_con
import json

from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }
global_db_con = get_db()
CUR_ENV = "PRD"

global JWT
SECRET = "why is connecting to a database so annoying"


@app.route('/buy') #endpoint
def buy():
    return 'Buy'


#-------assignment3------#

#------------------Login shiz----------------------#
@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print("made it to auth!")

        print(request.form.get("username"))

        cur=global_db_con.cursor()
        cur.execute("select * from users where username = '" + str(request.form["log_name"]) + "';")
        dbcredz = cur.fetchone()
        cur.close()
        print(dbcredz)
        #check if credentials is in the database
        if dbcredz[0] is None:
            print("No User!")
            return json_response( data={"message": "Invalid user name: " + str(request.form["log_name"])}, status = 404)
        else:
            print("in else statement!")
            if bcrypt.checkpw(bytes(request.form["log_pass"], "utf-8"), bytes(dbcredz[2], "utf-8")) == True:
                print("Successful Login, : " + str(request.form["log_name"]))
            
                JWT = jwt.encode( {"username": dbcredz[1],"password":dbcredz[2]}, SECRET, algorithm="HS256")
                print(JWT)
                return json_response( data={"jwt": JWT})
            else:
                print("Thats not the password, creeper!!")

                return json_response( data={"message": "Incorrect Password"}, status = 404)


#-----------------SignUp----------------------------#
@app.route('/signup',  methods=['POST']) #endpoint
def signup():

    """Creates an account from input creds. checks the DB to ensure no doubles. if the new account is valid,
    a JWT will be created to store the new users username and password."""

    fusername =request.form.get('uname')
    password = request.form.get('pass')

    """check the DB for existing creds"""
    cur = global_db_con.cursor()
    cur.execute("SELECT username FROM users WHERE username = '"+fusername+"';")
    dbuname = cur.fetchone()
    print(dbuname)

    if dbuname != None:
        print('username already exists! pick another dork')
        return json_response(data={"message": fusername + "Already Exists"})
    else:

        """hash and salt the password"""
        salted = bcrypt.hashpw( bytes(password, 'utf-8'), bcrypt.gensalt(10))
        print(salted)
        print(fusername)
        """insert into DB"""
        #cur.global_db_con.cursor()
        unsalted=salted.decode('utf-8')
        print(unsalted)
        cur.execute("INSERT INTO users(username, password) VALUES ('"+fusername+"', '"+unsalted+"');")
        cur.close()
        global_db_con.commit()

        """create the JWT"""
        #enc_JWT = jwt.encode({'username': fusername, 'password': unsalted}, SECRET, algorithm="HS256")


    return json_response(data={"message":fusername + "created successfully"})

#---------------------Bookstore----------------------#

@app.route('/bookstore', methods=['GET']) #endpoint
def bookstore():
    print("in bookstore")
    incoming=request.args.get("jwt")
    print(incoming)

    cur = global_db_con.cursor()
    try:
        cur.execute("select * from books;")
        booklist=cur.fetchall()
        cur.close()
    except:
        print("cannot read from database")
        return json_response(data={"message": "Error occured while reading from database."}, status=500)
    
    count=0
    message = '{"books":['
    for b in booklist:
        if b[0] < len(booklist) :
            message += '{"title":"'+str(b[1]) + '","price":"' + str(b[2]) + '"},'
        else:
            message += '{"title":"'+str(b[1]) + '","price":"' + str(b[2]) + '"}'
    message += "]}"
    print(message)
    print("sending silly token")
    return json_response(data=json.loads(message))


#-----------------Cart--------------------------#
@app.route('/showCart', methods=['GET']) #endpoint
def showCart():
    incoming=request.args.get("jwt")
    cur = global_db_con.cursor()
    try:
        cur.execute("select * from purchases;")
        purchases=cur.fetchall()
        cur.close()
    except:
        print("cannot read from database")
        return json_response(data={"message": "Error occured while reading from database."}, status=500)

    count=1
    message = '{"purchases":['
    for b in purchases:
       
        if count < len(purchases) :
            message += '{"title":"'+str(b[1]) + '","price":"' + str(b[2]) +'"},'
            count=count+1
        else:
            message += '{"title":"'+str(b[1]) +'","price":"' + str(b[2]) +'"}'
    message += "]}"
    print(message)
    print("sending silly token")
    return json_response(data=json.loads(message))


#--------------purchase--------------------#
@app.route('/purchase', methods=['POST']) #endpoint
def purchase():
    title = request.form["title"]
    print(title)
    cur = global_db_con.cursor()
    cur.execute("INSERT INTO purchases (title, price) SELECT title, price FROM books WHERE title = '" + title + "';")
    cur.close()
    global_db_con.commit()

    print("Added book to cart.")
    return json_response(data={"message":str(title) +" successfully added."})

app.run(host='0.0.0.0', port=80)

