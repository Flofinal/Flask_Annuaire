import json
from os import system
from flask import Blueprint, request, make_response
from user import mysql
import hashlib
import logging

auth = Blueprint('auth', __name__)

@auth.route('/signup_auth', methods=['POST'])
def signup_post():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM user WHERE email = %s"
        val = (d["email"],)
        mycursor.execute(sql,val)
        columns = mycursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in mycursor.fetchall()]
        if result:  # if a user is found, we want to redirect back to signup page so user can try again
            return make_response(
                {"result": "try"},
                200
            )
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        encoded_pwd = d["password"].encode()
        hashed_pwd = hashlib.sha256(encoded_pwd).hexdigest()
        sql="INSERT INTO user (email,name,numero,password) VALUES (%s, %s,%s, %s)"
        val=(d["email"],d["name"],d["numero"],hashed_pwd)
        mycursor.execute(sql,val)
        mysql.connection.commit()
        logging.info('%s signed up in the directory', d["email"])
        
        return make_response(
            {"result": "ok"},
            200
        )
    except:
        logging.error('%s could not sign up - SQL Error', d["email"])
        
        return make_response(
            {"result": "error"},
            400
        )

@auth.route('/login_auth', methods=['POST'])
def login_post():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM user WHERE email = %s"
        val = (d["email"],)
        mycursor.execute(sql, val)
        columns = mycursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in mycursor.fetchall()]
        encoded_pwd = d["password"].encode()
        hashed_pwd = hashlib.sha256(encoded_pwd).hexdigest()
        if not result or not result[0]["password"] == hashed_pwd:
            logging.warning('%s tried to log but wrong password', d["email"])
            
            return make_response(
                {"result": "wrong"},
                200
            )
        # if the above check passes, then we know the user has the right credentials
        payload = json.dumps(dict(email=result[0]["email"], password=result[0]["password"], id=result[0]["id"], name=result[0]["name"],numero=result[0]["numero"], role=result[0]["role"] ))
        logging.info('%s logged in', d["email"])
        
        return make_response(
            {"result": payload},
            200
        )
    except:
        logging.error('%s could not log in - SQL Error', d["email"])
        
        return make_response(
            {"result": "error"},
            400
        )


@auth.route('/profile_auth', methods=['POST'])
def profile_pwd():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()
        sql = "UPDATE user SET password = %s WHERE email = %s"
        encoded_pwd = d["password"].encode()
        hashed_pwd = hashlib.sha256(encoded_pwd).hexdigest()
        val = (hashed_pwd, d["email"])
        mycursor.execute(sql, val)
        mysql.connection.commit()

        logging.info('%s changed his password', d["email"])
        return make_response(
            {"result": "ok"},
            200
        )
    except:
        logging.error('%s could not change his password - SQL Error', d["email"])
        return make_response(
            {"result": "error"},
            400
        )


@auth.route('/load_user2', methods=['POST'])
def load_user2():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM user WHERE id = %s"
        val = (d["id_user"],)
        mycursor.execute(sql, val)
        columns = mycursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in mycursor.fetchall()]
        if result:
            payload = json.dumps(dict(email=result[0]["email"], password=result[0]["password"], id=result[0]["id"],
                                      name=result[0]["name"], numero=result[0]["numero"], role=result[0]["role"]))
            return make_response(
                {"result": payload},
                200
            )
        return make_response({
            "result": "nf"},
            200
        )
    except:
        return make_response(
            {"result": "error"},
            400
        )

@auth.route('/getuser', methods=['POST'])
def getuser():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()

        mycursor.execute("SELECT * FROM user")
        columns = mycursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in mycursor.fetchall()]
        if result:
            a = []
            for i in result:
                a += [dict(email=i["email"], name=i["name"], numero=i["numero"], role=i["role"])]
            payload = json.dumps(a)
            return make_response(
                {"result": payload},
                200
            )
        return make_response({
            "result": "nf"},
            200
        )
    except:
        return make_response(
            {"result": "error"},
            400
        )

@auth.route('/getname', methods=['POST'])
def getname():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM user WHERE name REGEXP %s"
        val = ("^"+d["name"],)
        mycursor.execute(sql, val)
        columns = mycursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)} for value in mycursor.fetchall()]
        if result:
            a = []
            for i in result:
                a += [dict(email=i["email"], name=i["name"], numero=i["numero"], role=i["role"])]
            payload = json.dumps(a)
            return make_response(
                {"result": payload},
                200
            )
        return make_response({
            "result": "nf"},
            200
        )
    except:
        return make_response(
            {"result": "error"},
            400
        )

@auth.route('/deleteUser', methods=['POST'])
def deleteUser():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()

        sql = "DELETE FROM user WHERE email = %s"
        adr = (d["email"],)
        mycursor.execute(sql, adr)
        mysql.connection.commit()
        logging.info('%s deleted his account', d["email"])
        return make_response({
            "result": "ok"},
            200
        )
    except:
        logging.error('%s could not delete his account - SQL Error', d["email"])
        return make_response(
            {"result": "error"},
            400
        )

@auth.route('/promouvoir', methods=['POST'])
def promouvoir():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()
        sql = "UPDATE user SET role = %s WHERE email = %s"
        val = ("admin",d["email"])
        mycursor.execute(sql, val)
        mysql.connection.commit()

        logging.info('%s got promoted to admin', d["email"])
        return make_response(
            {"result": "ok"},
            200
        )
    except:
        logging.error('%s could not be promoted to admin - SQL Error', d["email"])
        return make_response(
            {"result": "error"},
            400
        )

@auth.route('/retrograder', methods=['POST'])
def retrograder():
    try:
        d = request.json
        mycursor = mysql.connection.cursor()
        sql = "UPDATE user SET role = %s WHERE email = %s"
        val = ("member",d["email"])
        mycursor.execute(sql, val)
        mysql.connection.commit()
        logging.info('%s got downgraded to member', d["email"])
        return make_response(
            {"result": "ok"},
            200
        )
    except:
        logging.error('%s could not be downgraded to member - SQL Error', d["email"])
        return make_response(
            {"result": "error"},
            400
        )

    