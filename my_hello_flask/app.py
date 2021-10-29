from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json, jsonify

import jwt
import datetime
import bcrypt

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

JWT_TOKEN= None
SECRET = "why is connecting to a database so annoying"


@app.route('/buy') #endpoint
def buy():
    return 'Buy'


#-------assignment3------#
@app.route('/auth',  methods=['POST']) #endpoint
def auth():

    """authenticates a user using entered creds.
    takes the entered credentials and checks the database to see if creds are valid.
    if the account information is valid return a json response """
    
    '''get username from form'''
    username  = request.form.get('username')

    """use the username to query db for password"""
    cur = global_db_con.cursor()
    cur.execute("SELECT password FROM users WHERE username = users.username;")
    dbpass = cur.fetchone()
    cur.close();

    """check if the username exists"""
    if dbpass == None:
        print('invalid password!')
        return jsonify(logon = False)

    """check if the form password matches the password from the db"""
    if not bcrypt.checkpw(  bytes(request.form.get('pass'),  'utf-8' )  , str.encode(dbpass[0])):
        print('invalid password')
        return jsonify( logon = False)

    """create a JWT with the username and password"""
    encode_JWT =jwt.encode({'username': username, 'password': dbpass[0]}, SECRET, algorithm="HS256")
    return jsonify(jwt=encode_JWT, logon = True)

@app.route('/signup',  methods=['POST']) #endpoint
def signup():

    """Creates an account from input creds. checks the DB to ensure no doubles. if the new account is valid,
    a JWT will be created to store the new users username and password."""

    fusername =request.form.get('uname')
    password = request.form.get('pass')

    """check the DB for existing creds"""
    cur = global_db_con.cursor()
    cur.execute("SELECT username FROM users WHERE username = users.username;")
    dbuname = cur.fetchone()

    if dbuname == fusername:
        print('username already exists! pick another dork')
        return jsonify(logon =False)

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
    enc_JWT = jwt.encode({'username': fusername, 'password': unsalted}, SECRET, algorithm="HS256")


    return jsonify(jwt=enc_JWT, logon = True)


app.run(host='0.0.0.0', port=80)

