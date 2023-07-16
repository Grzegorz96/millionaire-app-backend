from Database_connection import database_connect
import mysql.connector
from flask import Flask, jsonify, request, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv
from Activation_number_sender import sending_activation_number
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("API_SECRET_KEY")


def create_tokens(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow(),
        'sub': user_id
    }

    access_token = jwt.encode(payload,
                              app.config["SECRET_KEY"],
                              algorithm="HS256")

    payload = {
        'exp': datetime.utcnow() + timedelta(hours=10),
        'iat': datetime.utcnow(),
        'sub': user_id
    }

    refresh_token = jwt.encode(payload,
                               app.config["SECRET_KEY"],
                               algorithm="HS256")

    return [access_token, refresh_token]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = request.headers.get("access-token")
        refresh_token = request.headers.get("refresh-token")

        if not access_token:
            return jsonify(result="access_token is missing"), 401

        try:
            jwt.decode(access_token, app.config["SECRET_KEY"], algorithms=['HS256'])

        except jwt.exceptions.ExpiredSignatureError:
            result = refreshing_access_token(refresh_token)
            if isinstance(result, str):
                resp = make_response(jsonify(result="new access token created"), 201)
                resp.headers["access-token"] = result
                return resp

            else:
                return result

        except jwt.exceptions.InvalidSignatureError as m:
            return jsonify({"InvalidSignatureError": m.args[0]}), 401

        except jwt.exceptions.InvalidTokenError as m:
            return jsonify({"InvalidTokenError": m.args[0]}), 401

        except Exception:
            return jsonify({"Error": "Other problem with access token"}), 500

        else:
            return f(*args, **kwargs)

    return decorated


def refreshing_access_token(refresh_token):
    if not refresh_token:
        return jsonify(result="refresh_token is missing"), 401

    try:
        decoded_refresh_token = jwt.decode(refresh_token, app.config["SECRET_KEY"], algorithms=['HS256'])

    except jwt.exceptions.ExpiredSignatureError:
        return jsonify({"Your session has expired": "login again"}), 401

    except jwt.exceptions.InvalidSignatureError as m:
        return jsonify({"InvalidSignatureError": m.args[0]}), 401

    except jwt.exceptions.InvalidTokenError as m:
        return jsonify({"InvalidTokenError": m.args[0]}), 401

    except Exception:
        return jsonify({"Error": "Other problem with refresh token"}), 500

    else:
        user_id = decoded_refresh_token["sub"]
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'iat': datetime.utcnow(),
            'sub': user_id
        }

        new_access_token = jwt.encode(payload,
                                      app.config["SECRET_KEY"],
                                      algorithm="HS256")

        return new_access_token


# Function for getting questions.
@app.route("/questions", methods=["GET"])
def get_questions():
    # Making connection and cursor as dictionary.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    # Execute SELECT query.
    try:
        query = """SELECT content, A, B, C, D, right_answer, difficulty FROM questions"""
        cur.execute(query)
    # Return details of error with 400 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500
    # Return list of questions as json with 200 status code.
    else:
        return jsonify(result=cur.fetchall()), 200
    # Closing connection with database and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/users/register/check-data", methods=["GET"])
def check_data_for_registration():
    # Making connection and cursor as dictionary.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    request_data = request.get_json()
    # Execute SELECT query.
    try:
        query = """SELECT user_id FROM users
                   WHERE login=%(login)s OR email=%(email)s"""

        cur.execute(query, request_data)
    # Return details of error with 400 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500
    # Return list of questions as json with 200 status code.
    else:
        user_id = cur.fetchall()
        if not user_id:
            return jsonify(result="login and e-mail are available"), 200
        else:
            return jsonify(result="login or e-mail are not available"), 226

    # Closing connection with database and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/users/send-activation-number", methods=["POST"])
def send_activation_number():
    request_body = request.get_json()
    sending_result = sending_activation_number(request_body["email_receiver"])
    if isinstance(sending_result, dict):
        return jsonify(result=sending_result), 200
    else:
        return jsonify(result=sending_result), 500


# Function adding user
@app.route("/users/register", methods=["POST"])
def register_user():
    # Making connection and cursor.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    try:
        # Assignment request body into request data variable.
        request_data = request.get_json()
        query = """INSERT INTO users(first_name, last_name, login, password, email)
                   VALUES(%(first_name)s, %(last_name)s, %(login)s,  %(password)s, %(email)s) """
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()

    except mysql.connector.Error as message:
        # If is error in sql syntax, user declared bad name of key.
        if "You have an error in your SQL syntax" in message.msg:
            return jsonify(key_error="Required keys: first_name, last_name, login, password, email."), 400
        elif "login_UNIQUE" in message.msg:
            return jsonify(login_error="The user with the given login is already registered"), 400
        elif "email_UNIQUE" in message.msg:
            return jsonify(email_error="The user with the given e-mail address is already registered"), 400
        else:
            return jsonify(result=message.msg), 500
    # If it succeeds, return json of info about created user with 201 status code.
    else:
        return jsonify(result="User successfully created."), 201
    # Closing connection and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/scores", methods=["GET"])
def get_scores():
    # Making connection and cursor.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    try:
        limit = request.args.get("limit")
        if limit:
            query = f"""SELECT DISTINCT users.first_name, users.last_name, top_scores.points FROM users
                        JOIN top_scores ON users.user_id=top_scores.user_id
                        ORDER BY points DESC
                        LIMIT {limit}"""

        else:
            query = f"""SELECT DISTINCT users.first_name, users.last_name, top_scores.points FROM users
                        JOIN top_scores ON users.user_id=top_scores.user_id
                        ORDER BY points DESC"""

        cur.execute(query)

    except mysql.connector.Error as message:
        if "Undeclared variable" in message.msg:
            return jsonify(result="Wrong value in limit parameter."), 400
        else:
            return jsonify(result=message.msg), 500
    else:
        return jsonify(result=cur.fetchall()), 200
    # Closing connection and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/scores", methods=["POST"])
@token_required
def add_score():
    # Making connection and cursor.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    try:
        # Assignment request body into request data variable.
        request_data = request.get_json()
        query = """INSERT INTO top_scores(user_id, points)
                   VALUES(%(user_id)s, %(points)s)"""
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()

    except mysql.connector.Error as message:
        # If is error in sql syntax, user declared bad name of key.
        if "You have an error in your SQL syntax" in message.msg:
            return jsonify(result="Required keys: user_id, points."), 400
        else:
            return jsonify(result=message.msg), 500
    # If it succeeds, return json of info about created user with 201 status code.
    else:
        return jsonify(result="Score added successfully"), 201
    # Closing connection and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/questions", methods=["POST"])
@token_required
def add_questions():
    connection = database_connect()
    cur = connection.cursor()
    try:
        request_body = request.get_json()
        query = """INSERT INTO questions(content, A, B, C, D, right_answer, difficulty)
                   VALUES"""
        if isinstance(request_body, list):
            for dictionary in request_body:
                content = dictionary["tresc"]
                a = dictionary["odp"][0]
                b = dictionary["odp"][1]
                c = dictionary["odp"][2]
                d = dictionary["odp"][3]
                right_answer = dictionary["odp_poprawna"]
                difficulty = dictionary['trudnosc']

                if request_body.index(dictionary) < (len(request_body) - 1):
                    query += fr""" ("{content}", "{a}", "{b}", "{c}", "{d}", "{right_answer}", {difficulty}),"""

                else:
                    query += fr""" ("{content}", "{a}", "{b}", "{c}", "{d}", "{right_answer}", {difficulty})"""

        elif isinstance(request_body, dict):
            content = request_body["tresc"]
            a = request_body["odp"][0]
            b = request_body["odp"][1]
            c = request_body["odp"][2]
            d = request_body["odp"][3]
            right_answer = request_body["odp_poprawna"]
            difficulty = request_body['trudnosc']
            query += fr""" ("{content}", "{a}", "{b}", "{c}", "{d}", "{right_answer}", {difficulty})"""

        else:
            raise ValueError

        cur.execute(query)
        connection.commit()
    except KeyError:
        return jsonify(result="Required keys: tresc, odp, odp_poprawna, trudnosc."), 400

    except (IndexError, ValueError):
        return jsonify(result="The question was worded incorrectly. Wording required: "
                              "[{tresc:nowe pytanie, odp:[odpowiedz1, odpowiedz2, odpowiedz3, odpowiedz4], "
                              "odp_poprawna:C, trudnosc:0}] or {tresc:nowe pytanie, odp:[odpowiedz1, odpowiedz2,"
                              " odpowiedz3, odpowiedz4], odp_poprawna:C, trudnosc:0}."), 400

    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    else:
        return jsonify(result="question added successfully"), 201

    finally:
        connection.close()
        cur.close()


@app.route("/users/login", methods=["GET"])
def login_user():
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    request_data = request.get_json()
    # Execute SELECT query.
    try:
        query = """SELECT user_id FROM users
                   WHERE login=%(login)s AND password=%(password)s AND active_flag=1"""

        cur.execute(query, request_data)
    # Return details of error with 500 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500
    # Return list of questions as json with 200 status code.
    else:
        user_id = cur.fetchall()
        if user_id:
            tokens = create_tokens(user_id[0]["user_id"])
            resp = make_response(jsonify(result=user_id[0]["user_id"]), 200)
            resp.headers["access-token"] = tokens[0]
            resp.headers["refresh-token"] = tokens[1]
            return resp
        else:
            return jsonify(result="Bad login, password or your account has not been activated"), 401

    # Closing connection with database and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/users/<user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    # Making connection and cursor as dictionary.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    request_data = {}
    # Execute SELECT query.
    try:
        query = """SELECT user_id, first_name, last_name, login, password, email, active_flag FROM users
                   WHERE user_id=%(user_id)s AND active_flag=1"""
        request_data["user_id"] = user_id
        cur.execute(query, request_data)
    # Return details of error with 500 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500
    # Return list of questions as json with 200 status code.
    else:
        return jsonify(result=cur.fetchall()), 200
    # Closing connection with database and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/users/<user_id>", methods=["PATCH"])
@token_required
def update_user(user_id):
    # Making connection and cursor.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)

    try:
        query = """UPDATE users"""
        request_data = request.get_json()
        request_data["user_id"] = user_id
        if "first_name" in request_data.keys():
            query += """ SET first_name=%(first_name)s"""
        elif "last_name" in request_data.keys():
            query += """ SET last_name=%(last_name)s"""
        elif "password" in request_data.keys():
            query += """ SET password=%(password)s"""
        else:
            raise KeyError
        query += """ WHERE user_id=%(user_id)s AND active_flag=1"""
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()
        is_it_done = cur.rowcount
        if not is_it_done:
            raise ReferenceError

    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    except KeyError:
        return jsonify(result="Required keys: first_name ,last_name or password."), 400

    except ReferenceError:
        return jsonify(result="User with given id does not exist or "
                              "you are trying to update a resource with the same data."), 409
    # If it succeeds, return json of info about created user with 201 status code.
    else:
        return jsonify(result="Update successful."), 200
    # Closing connection and cursor.
    finally:
        connection.close()
        cur.close()


@app.route("/users/<user_id>", methods=["DELETE"])
@token_required
def delete_user(user_id):
    # Making connection and cursor.
    connection = database_connect()
    cur = connection.cursor(dictionary=True)
    request_data = {}
    try:
        request_data["user_id"] = user_id
        query = """UPDATE users
                   SET active_flag=False 
                   WHERE user_id=%(user_id)s AND active_flag=1"""
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()
        is_it_done = cur.rowcount
        if not is_it_done:
            raise ReferenceError

    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    except ReferenceError:
        return jsonify(result="User with given id does not exist or has already been deleted."), 409
    else:
        return jsonify(result="Deletion completed successfully."), 200
    # Closing connection and cursor.
    finally:
        connection.close()
        cur.close()


if __name__ == "__main__":
    # Running app on server.
    app.run(debug=True, port=3000)
