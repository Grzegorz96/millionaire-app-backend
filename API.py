# Modules import.
from Database_connection import database_connect
import mysql.connector
from flask import Flask, jsonify, request, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv
# Module with sending_activation_number function for sending email to user.
from Activation_number_sender import sending_activation_number
# Module for returning Access-Control-Allow-Origin header with web domains.
from flask_cors import CORS
# Import of the validating module.
from re import match

# Loading environment variables.
load_dotenv()
# Creating app.
app = Flask(__name__)
# Assigning SECRET_KEY for access and refresh key from API_SECRET_KEY environment variable.
app.config["SECRET_KEY"] = os.getenv("API_SECRET_KEY")
# Permission for requesting by origins for every endpoint in application and exposing headers.
CORS(app, resources={"*": {"origins": ["http://127.0.0.1:5500", "https://millionaire-web-app.netlify.app"]}},
     expose_headers=["access-token", "refresh-token"])


def create_tokens(user_id):
    """The function responsible for creating JWT tokens with user_id parameter and returning them."""
    # Creating payload for access_token with subject, expiration time and issued at. Exp informs about time when token
    # will be expired.
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    # Creating access token with encoded payload, Key for decoding and algorithm HS256.
    access_token = jwt.encode(payload,
                              app.config["SECRET_KEY"],
                              algorithm="HS256")
    # Creating payload for refresh token with subject, expiration time and issued at. In this case exp time is longer
    # than exp time in access token, when exp time for refresh token expired, user cant use protected endpoints and
    # needs to log in again.
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=10),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    # Creating refresh token with encoded payload, Key for decoding and algorithm HS256.
    refresh_token = jwt.encode(payload,
                               app.config["SECRET_KEY"],
                               algorithm="HS256")

    # Returning list of tokens.
    return [access_token, refresh_token]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """The function responsible for reading access and refresh tokens from headers and validating them. If the
        access token expires, the function will try to refresh it using a refresh token."""
        # Assigning access and refresh tokens from request headers.
        access_token = request.headers.get("access-token")
        refresh_token = request.headers.get("refresh-token")

        # If user didn't send his access_token then return status 401 and user cant go further.
        if not access_token:
            return jsonify(result="access_token is missing"), 401

        # If refresh token is not existing, then return 401 status
        if not refresh_token:
            return jsonify(result="refresh_token is missing"), 401

        # If access_token exist, trying to decode it with KEY and algorithm.
        try:
            jwt.decode(access_token, app.config["SECRET_KEY"], algorithms=['HS256'])

        # If access_token is expired then program will try to refresh this token.
        except jwt.exceptions.ExpiredSignatureError:
            # Calling refreshing access token function with refresh token.
            result = refreshing_access_token(refresh_token)
            # If result from function is string for example: result="ey3j23jio3huosjcoi3i2i2isdad", then new access key
            # was successfully created and start creating response object with status 201, response body and new
            # access token in header.
            if isinstance(result, str):
                resp = make_response(jsonify(result="new access token created"), 201)
                resp.headers["access-token"] = result
                # Return response object to frontend.
                return resp

            # If result is tuple, then new access token wasn't created and an error occurred 401 or 500 and this error
            # will be returned to user.
            else:
                return result

        # If signature error was occurred then return 401 status with error arg in response body.
        except jwt.exceptions.InvalidSignatureError as m:
            return jsonify({"InvalidSignatureError": m.args[0]}), 401

        # If token error was occurred then return 401 status with error arg in response body.
        except jwt.exceptions.InvalidTokenError as m:
            return jsonify({"InvalidTokenError": m.args[0]}), 401

        # If other error was except, return 500 status
        except Exception:
            return jsonify({"Error": "Other problem with access token"}), 500

        # If everything is ok and token is not expired and was successfully decrypted then user can go to target
        # endpoint.
        else:
            return f(*args, **kwargs)

    return decorated


def refreshing_access_token(refresh_token):
    """The function responsible for refreshing expired access tokens with refresh tokens."""
    # Trying to decode refresh token with KEY and algorithm.
    try:
        decoded_refresh_token = jwt.decode(refresh_token, app.config["SECRET_KEY"], algorithms=['HS256'])

    # If refresh token is expired, then return 401 status with "Your session has expired" key in response body.
    except jwt.exceptions.ExpiredSignatureError:
        return jsonify({"Your session has expired": "login again"}), 401

    # If signature error was occurred then return 401 status with error arg in response body.
    except jwt.exceptions.InvalidSignatureError as m:
        return jsonify({"InvalidSignatureError": m.args[0]}), 401

    # If token error was occurred then return 401 status with error arg in response body.
    except jwt.exceptions.InvalidTokenError as m:
        return jsonify({"InvalidTokenError": m.args[0]}), 401

    # If other error was except, return 500 status.
    except Exception:
        return jsonify({"Error": "Other problem with refresh token"}), 500

    # If decoding refresh token was successfully then start making new access token.
    else:
        # Creating payload with exp/iat time and subject with user_id getting form decoded payload from refresh token.
        user_id = decoded_refresh_token["sub"]
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        # Creating new access token with payload, KEY and algorithm.
        new_access_token = jwt.encode(payload,
                                      app.config["SECRET_KEY"],
                                      algorithm="HS256")

        # Returning new access token.
        return new_access_token


def validate_user_id(user_id, access_token):
    """The function responsible for user ID validation."""
    try:
        # Assigning user id from token JWT.
        access_token_user_id = jwt.decode(access_token, options={"verify_signature": False})["sub"]
    except Exception:
        pass
    else:
        # If the entered user id is equal to the user id from the token, I return true, in any other case return false.
        if user_id == access_token_user_id:
            return True


@app.route("/questions", methods=["GET"])
def get_questions():
    """The function responsible for getting questions from the database. Allowed methods: GET."""
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None
    # Trying to perform a database operation.
    try:
        # Making connection and cursor as dictionary.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Making query.
        query = """SELECT content, A, B, C, D, right_answer, difficulty FROM questions"""
        # Execute SELECT query.
        cur.execute(query)

    # Return details of error with 500 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    # Return 200 status code.
    else:
        return jsonify(result=cur.fetchall()), 200

    # Closing connection with database and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/users/register/check-data", methods=["POST"])
def check_data_for_registration():
    """The function responsible for determining whether the data entered by the user is no longer in the database.
    Allowed methods: POST."""
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Creating request data from request body.
        request_data = request.get_json()
        # Validation of entered data.
        if not (match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń0-9]{5,45}$", request_data["login"]) and
                match("^([A-Za-z0-9]+|[A-Za-z0-9][A-Za-z0-9._-]+[A-Za-z0-9])@([A-Za-z0-9]+|[A-Za-z0-9._-]+[A-Za-z0-9])\.[A-Za-z0-9]+$",
                      request_data["email"])):
            raise ValueError
        # Making connection and cursor as dictionary.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Making query.
        query = """SELECT user_id FROM users
                   WHERE login=%(login)s OR email=%(email)s"""
        # Execute SELECT query.
        cur.execute(query, request_data)

    # Return details of error with 500 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    # If the user does not provide valid keys and their values in json, it will return a status of 400.
    except (ValueError, TypeError, KeyError, IndexError):
        return jsonify(result="The entered data does not meet the requirements. "
                              "Required data: {login:'string', email:'string'}."), 400

    # If everything ok, checking if is something retrieved from cursor. When there will be user id it means that
    # in database is already registered user with those currently provided data and user can't create account with
    # these data. In case there is nothing there, user can create account with this data.
    else:
        user_id = cur.fetchall()
        # Returning information with 200 status.
        if not user_id:
            return jsonify(result="login and e-mail are available."), 200
        # Returning information with 226 status.
        else:
            return jsonify(result="login or e-mail are not available."), 226

    # Closing connection with database and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/users/send-activation-number", methods=["POST"])
def send_activation_number():
    """The function responsible for sending activation numbers to new users. Allowed methods: POST."""
    try:
        # Creating request body from request body json.
        request_body = request.get_json()
        # Validation of entered data.
        if not match("^([A-Za-z0-9]+|[A-Za-z0-9][A-Za-z0-9._-]+[A-Za-z0-9])@([A-Za-z0-9]+|[A-Za-z0-9._-]+[A-Za-z0-9])\.[A-Za-z0-9]+$",
                     request_body["email_receiver"]):
            raise ValueError

        # Calling function from Activation_number_sender module with user's email.
        sending_result = sending_activation_number(request_body["email_receiver"])

    # Return 400 if email does not meet the requirements.
    except (KeyError, TypeError, ValueError, IndexError):
        return jsonify(result="Invalid email address or data key: {email_receiver: 'string'}."), 400

    else:
        # If return from sending_activation_number is dictionary it means email was send successfully, and we got
        # activation number from function. We have to return this number in sending_result to frontend, to check if the
        # user entered the correct number.
        if isinstance(sending_result, dict):
            # Returning 200 status
            return jsonify(result=sending_result), 200
        # Returning 500 status, email wasn't send successfully.
        else:
            return jsonify(result=sending_result), 500


@app.route("/users/register", methods=["POST"])
def register_user():
    """The function responsible for adding new users to the database. Allowed methods: POST."""
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Assignment request body into request data variable.
        request_data = request.get_json()
        # Validation of entered data.
        if not (match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń]{2,45}$", request_data["first_name"]) and
                match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń]{2,45}$", request_data["last_name"]) and
                match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń0-9]{5,45}$", request_data["login"]) and
                match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń0-9!@#$%^&*]{7,45}$", request_data["password"]) and
                match(
                    "^([A-Za-z0-9]+|[A-Za-z0-9][A-Za-z0-9._-]+[A-Za-z0-9])@([A-Za-z0-9]+|[A-Za-z0-9._-]+[A-Za-z0-9])\.[A-Za-z0-9]+$",
                    request_data["email"])):
            raise ValueError
        # Making connection and cursor.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Making query.
        query = """INSERT INTO users(first_name, last_name, login, password, email)
                   VALUES(%(first_name)s, %(last_name)s, %(login)s,  %(password)s, %(email)s) """
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()

    # If error was occurred.
    except mysql.connector.Error as message:
        # If "login_UNIQUE" in message.msg it means that user with the given login is already in database, login
        # column has unique key. Returning 400 status.
        if "login_UNIQUE" in message.msg:
            return jsonify(login_error="The user with the given login is already registered."), 400

        # If "email_UNIQUE" in message.msg it means that user with the given email is already in database, email
        # column has unique key. Returning 400 status.
        elif "email_UNIQUE" in message.msg:
            return jsonify(email_error="The user with the given e-mail address is already registered."), 400

        # If other error, returning 500 status.
        else:
            return jsonify(result=message.msg), 500

    # If the user does not provide valid keys and their values in json, it will return a status of 400.
    except (ValueError, TypeError, KeyError, IndexError):
        return jsonify(result="The entered data does not meet the requirements. Required data: {first_name: 'string', "
                              "last_name: 'string', login: 'string', password: 'string', email: 'string'}."), 400

    # If it succeeds, returning 201 status code.
    else:
        return jsonify(result="User successfully created."), 201

    # Closing connection and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/scores", methods=["GET"])
def get_scores():
    """The function responsible for getting scores from the database. Allowed methods: GET."""
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Assigning ?limit= from parameter into limit variable.
        limit = request.args.get("limit")
        # Checking is user given limit parameter. If he did, creating query with limit if he didn't, query will not
        # have limit parameter.
        if limit:
            # Validation of entered data.
            if not (int(limit) > 0):
                raise ValueError

            # Making query.
            query = f"""SELECT DISTINCT users.first_name, users.last_name, top_scores.points FROM users
                        JOIN top_scores ON users.user_id=top_scores.user_id
                        ORDER BY points DESC
                        LIMIT {limit}"""

        else:
            # Making query.
            query = """SELECT DISTINCT users.first_name, users.last_name, top_scores.points FROM users
                       JOIN top_scores ON users.user_id=top_scores.user_id
                       ORDER BY points DESC"""
        # Making connection and cursor.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Executing query.
        cur.execute(query)

    # If error with executing query then check what type of error.
    except mysql.connector.Error as message:
        # Returning 500 status response.
        return jsonify(result=message.msg), 500

    # If the user does not provide valid value in parameter, it will return a status of 400.
    except (ValueError, TypeError, KeyError, IndexError):
        return jsonify(result="Invalid value in the parameter."), 400

    # If everything ok then return results fetched from the cursor with 200 status.
    else:
        return jsonify(result=cur.fetchall()), 200

    # Closing connection and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/scores", methods=["POST"])
@token_required
def add_score():
    """The function responsible for adding scores to the database (protected by access_token). Allowed methods: POST."""
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Assignment request body into request data variable.
        request_data = request.get_json()
        # Validation of entered data.
        request_data["user_id"] = int(request_data["user_id"])
        if not (int(request_data["points"]) > 1000):
            raise ValueError
        # Checking whether the user refers to the user saved in the token.
        if not validate_user_id(request_data["user_id"], request.headers["access-token"]):
            return jsonify(result="Invalid user id."), 403
        # Making connection and cursor.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Making query.
        query = """INSERT INTO top_scores(user_id, points)
                   VALUES(%(user_id)s, %(points)s)"""
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()

    # Error with executing query.
    except mysql.connector.Error as message:
        # Returning 500 status.
        return jsonify(result=message.msg), 500

    # If the user does not provide valid keys and their values in json, it will return a status of 400.
    except (ValueError, TypeError, KeyError, IndexError):
        return jsonify(result="The entered data does not meet the requirements. Required data: {user_id: integer, "
                              "points: integer>1000}."), 400

    # If it succeeds, returning  with 201 status code.
    else:
        return jsonify(result="Score added successfully"), 201

    # Closing connection and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/questions", methods=["POST"])
@token_required
def add_questions():
    """The function responsible for adding questions to the database (protected by access_token).
    Allowed methods: POST."""
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Assignment request body into request data variable.
        request_body = request.get_json()
        # Making query.
        query = """INSERT INTO questions(content, A, B, C, D, right_answer, difficulty)
                   VALUES"""
        # If request body is list of dictionaries (a lot of questions), then dictionaries will be written into SQL query
        # by for loop and added to the main query.
        if isinstance(request_body, list):
            for dictionary in request_body:
                content = dictionary["content"]
                a = dictionary["answers"][0]
                b = dictionary["answers"][1]
                c = dictionary["answers"][2]
                d = dictionary["answers"][3]
                right_answer = dictionary["right_answer"]
                difficulty = dictionary["difficulty"]

                # For not last records with commas.
                if request_body.index(dictionary) < (len(request_body) - 1):
                    query += fr""" ("{content}", "{a}", "{b}", "{c}", "{d}", "{right_answer}", {difficulty}),"""

                # For last record without comma.
                else:
                    query += fr""" ("{content}", "{a}", "{b}", "{c}", "{d}", "{right_answer}", {difficulty})"""

        # If request body is dictionary (1 question), then will be converted into SQL query and added to the main query.
        elif isinstance(request_body, dict):
            content = request_body["content"]
            a = request_body["answers"][0]
            b = request_body["answers"][1]
            c = request_body["answers"][2]
            d = request_body["answers"][3]
            right_answer = request_body["right_answer"]
            difficulty = request_body["difficulty"]
            query += fr""" ("{content}", "{a}", "{b}", "{c}", "{d}", "{right_answer}", {difficulty})"""

        # If user want to add other type than list/dict, there will be ValueError raised.
        else:
            raise ValueError

        # Making connection and cursor.
        connection = database_connect()
        cur = connection.cursor()
        # Executing and committing changes.
        cur.execute(query)
        connection.commit()

    # Error with executing query, returning 500 status with msg.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    # If KeyError, returning 400 status code with json.
    except KeyError:
        return jsonify(result="Required keys: content, answers, right_answer, difficulty."), 400

    # If IndexError, ValueError or TypeError that user worded incorrectly questions in request body and returning 400
    # status with information.
    except (ValueError, TypeError, IndexError):
        return jsonify(result="The question was worded incorrectly. Wording required: "
                              "[{content: 'string', answers: ['string', 'string', 'string', 'string'], "
                              "right_answer: 'string', difficulty: integer}] or {content: 'string', answers: "
                              "['string', 'string', 'string', 'string'], right_answer: 'string', "
                              "difficulty: integer}."), 400

    # If everything ok, then returning 201 status with information.
    else:
        return jsonify(result="question added successfully"), 201

    # Closing connection and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/users/login", methods=["POST"])
def login_user():
    """The function responsible for getting user id from the database and JWT tokens. Allowed methods: POST."""
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Assignment request body into request data variable.
        request_data = request.get_json()
        # Validation of entered data.
        if not (match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń0-9]{5,45}$", request_data["login"]) and
                match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń0-9!@#$%^&*]{7,45}$", request_data["password"])):
            raise ValueError
        # Making connection and cursor.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Making query.
        query = """SELECT user_id FROM users
                   WHERE login=%(login)s AND password=%(password)s AND active_flag=1"""
        # Executing query.
        cur.execute(query, request_data)

    # Return details of error with 500 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    # If the user does not provide valid keys and their values in json, it will return a status of 400.
    except (ValueError, TypeError, KeyError, IndexError):
        return jsonify(result="The entered data does not meet the requirements. Required data: {login: 'string', "
                              "password: 'string'}."), 400

    # If wasn't errors, checking if record with provided login, password and active_flag=1 was selected.
    else:
        # Assigning cursor's data to user_id variable.
        user_id = cur.fetchall()
        # If user is not None, it means that user with given login and password is in database and can log in.
        if user_id:
            # Creating access and refresh tokens with user id number.
            tokens = create_tokens(user_id[0]["user_id"])
            # Making response object with status 200 and user_id number in response body.
            resp = make_response(jsonify(result=user_id[0]["user_id"]), 200)
            # Adding access and refresh token headers.
            resp.headers["access-token"] = tokens[0]
            resp.headers["refresh-token"] = tokens[1]
            # Returning response.
            return resp

        # If user_id is None that means user with given login and password doesn't exist in database, user entered
        # incorrect data. Returning 401 status.
        else:
            return jsonify(result="Bad login, password or your account has not been activated"), 401

    # Closing connection with database and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/users/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    """The function responsible for getting user's data (protected by access_token). Allowed methods: GET."""
    # Checking whether the user refers to the user saved in the token.
    if not validate_user_id(user_id, request.headers["access-token"]):
        return jsonify(result="Invalid user id."), 403
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Making connection and cursor as dictionary.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Creating request_data and adding user_id from endpoint's subresource.
        request_data = {"user_id": user_id}
        # Making query.
        query = """SELECT user_id, first_name, last_name, login, password, email, active_flag FROM users
                   WHERE user_id=%(user_id)s AND active_flag=1"""
        # Executing query.
        cur.execute(query, request_data)

    # Return details of error with 500 status code.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    else:
        user_data = cur.fetchall()
        if user_data:
            # When everything ok, returning 200 status with selected info about user in response body.
            return jsonify(result=user_data), 200
        else:
            # Else returning 401 status with error message.
            return jsonify(result="The user with the given id does not exist"), 401

    # Closing connection with database and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/users/<int:user_id>", methods=["PATCH"])
@token_required
def update_user(user_id):
    """The function responsible for updating user's data in the database (protected by access_token).
    Allowed methods: PATCH."""
    # Checking whether the user refers to the user saved in the token.
    if not validate_user_id(user_id, request.headers["access-token"]):
        return jsonify(result="Invalid user id."), 403
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Making connection and cursor.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Making query.
        query = """UPDATE users"""
        # Assignment request body into request data variable.
        request_data = request.get_json()
        # Adding user_id from endpoint's subresource to the request_data.
        request_data["user_id"] = user_id

        # Checking what information user want to change. If "first_name" key in request_data then creating and adding
        # query with SET first_name.
        if "first_name" in request_data.keys():
            # Validation of entered data.
            if not match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń]{2,45}$", request_data["first_name"]):
                raise ValueError
            query += """ SET first_name=%(first_name)s"""

        # If "last_name" key in request_data then creating and adding query with SET last_name.
        elif "last_name" in request_data.keys():
            # Validation of entered data.
            if not match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń]{2,45}$", request_data["last_name"]):
                raise ValueError
            query += """ SET last_name=%(last_name)s"""

        # If "password" key in request_data then creating and adding query with SET_password.
        elif "password" in request_data.keys():
            # Validation of entered data.
            if not match("^[A-ZĘÓĄŚŁŻŹĆŃa-zęóąśłżźćń0-9!@#$%^&*]{7,45}$", request_data["password"]):
                raise ValueError
            query += """ SET password=%(password)s"""

        # If other key in request_data (in front end user can change only first_name, last_name and password) then
        # raise KeyError.
        else:
            raise KeyError

        # Adding into query WHERE clause
        query += """ WHERE user_id=%(user_id)s AND active_flag=1"""
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()
        # Checking if a record has changed in the database, if not it means that the user has changed the data to
        # identical data that was previously in the database.
        is_it_done = cur.rowcount
        if not is_it_done:
            raise ReferenceError

    # If error with executing query then returning 500 status.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    # If KeyError then returning 400 status with info.
    except KeyError:
        return jsonify(result="Required keys: first_name ,last_name or password."), 400

    # If ReferenceError then returning 409 status with info.
    except ReferenceError:
        return jsonify(result="User with given id does not exist or "
                              "you are trying to update a resource with the same data."), 409

    # If the user does not provide valid keys and their values in json, it will return a status of 400.
    except (ValueError, TypeError, IndexError):
        return jsonify(result="The entered data does not meet the requirements. Required data: {first_name: 'string'} "
                              "or {last_name: 'string'} or {password: 'string'}."), 400

    # If it succeeds, returning 200 status with successful information.
    else:
        return jsonify(result="Update successful."), 200

    # Closing connection and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


@app.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user(user_id):
    """The function responsible for setting the user flag to inactive in the database (protected by access_token).
    Allowed methods: DELETE."""
    # Checking whether the user refers to the user saved in the token.
    if not validate_user_id(user_id, request.headers["access-token"]):
        return jsonify(result="Invalid user id."), 403
    # Making empty connection and cursor, if connection and cursor won't be created then in finally won't be error.
    connection = None
    cur = None

    # Trying to perform a database operation.
    try:
        # Making connection and cursor.
        connection = database_connect()
        cur = connection.cursor(dictionary=True)
        # Creating request_data and adding user_id from endpoint's subresource.
        request_data = {"user_id": user_id}
        # Making query.
        query = """UPDATE users
                   SET active_flag=False 
                   WHERE user_id=%(user_id)s AND active_flag=1"""
        # Execute and commit query.
        cur.execute(query, request_data)
        connection.commit()
        # Checking if a record has deleted from the database, if not it means that the user wanted to delete record
        # which doesn't exist in database.
        is_it_done = cur.rowcount
        if not is_it_done:
            raise ReferenceError

    # If error with executing query, returning 500 status with msg.
    except mysql.connector.Error as message:
        return jsonify(result=message.msg), 500

    # If ReferenceError, nothing was deleted from database. Returning information to user with 409 status.
    except ReferenceError:
        return jsonify(result="User with given id does not exist or has already been deleted."), 409

    # If everything ok, then returning 200 status with successful information.
    else:
        return jsonify(result="Deletion completed successfully."), 200

    # Closing connection and cursor if it exists.
    finally:
        if connection:
            connection.close()
            if cur:
                cur.close()


# Main
if __name__ == "__main__":
    # Running app on server.
    app.run(debug=True, port=3000)
