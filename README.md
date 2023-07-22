![logo frontend](https://github.com/Grzegorz96/millionaire-app-frontend/assets/129303867/1b1610c8-d435-47a3-92be-df9ce009fef5)
# API for MILLIONAIRE.app

The API allows the user to connect to the database from the level of the frontend application. The program contains many endpoints needed for the functioning of the frontend. It also has a JSON Web Token generator, a function that protect endpoints, a function that refreshes expired access tokens and a program for automatically sending generated activation numbers to email.


## Description of the modules

The program consists of 3 modules and each of them is responsible for something else. The API.py module is responsible for receiving requests, handling them and returning answers. In addition, this module generates a JWT access token and a JWT refresh token for a newly logged-in user, refreshes expired access tokens and protects some endpoints for which an access token is required. Ie is responsible for direct operations on the MySQL database. Database_connection.py is responsible for creating the database connection required by the function in API.py. The last module Activation_numvber_sender.py is used to generate the activation code and send it to the imported email address. In order for the program to work, it additionally requires the .env environment variables. All 3 modules retrieve the necessary data and passwords from the .env file.


## Features

- Access token and refresh token generation function.
- A function that protects endpoints against access by unauthorized persons.
- The function of sending the generated confirmation number to the user's e-mail address.
- The function of refreshing expired access tokens (15 minutes of validity) using an active refresh token (10 hours of validity).
- Database CRUD functions.
- Handling various errors and returning the appropriate code status.


## Technology used

**Server:** 
- Languages: Python, SQL
- Third Party Libraries: Flask, PyJWT, mysql-connector-python, python-dotenv
- Hosting for API: www.pythonanywhere.com
- Hosting for MySQL database: www.pythonanywhere.com


## Installation

### To run API on localhost:

#### Requirements:

##### Programs and libraries:
- Python 3.11
- MySQL Server 8.0
- Flask 2.3.2
- PyJWT 2.7.0
- mysql-connector-python 8.0.33
- python-dotenv

##### Environment Variables:

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_HOST`=IP or name of your host

`DATABASE_USER`=Your database username

`DATABASE_PASSWORD`=Your database password

`DATABASE_DATABASE`=The name of your database

`API_SECRET_KEY`=Secret key for encoding and decoding your JSON Web Tokens

 - ```bash
import uuid
SECRET_KEY = uuid.uuid4().hex
```

`EMAIL_SENDER`=Email from which messages will be sent to users

`EMAIL_SENDER_PASSWORD`=Generated password for the given e-mail

##### Tables for database:
- users
- top_scores
- questions
```bash
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `login` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `active_flag` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login_UNIQUE` (`login`),
  UNIQUE KEY `email_UNIQUE` (`email`)
```
  
```bash
CREATE TABLE `top_scores` (
  `top_score_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `points` int NOT NULL,
  PRIMARY KEY (`top_score_id`),
  KEY `user_id_fk` (`user_id`),
  CONSTRAINT `user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
```

```bash
CREATE TABLE `questions` (
  `question_id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(120) NOT NULL,
  `A` varchar(45) NOT NULL,
  `B` varchar(45) NOT NULL,
  `C` varchar(45) NOT NULL,
  `D` varchar(45) NOT NULL,
  `right_answer` varchar(1) NOT NULL,
  `difficulty` int NOT NULL,
  PRIMARY KEY (`question_id`),
  UNIQUE KEY `content_UNIQUE` (`content`)
```

#### Instruction:
- Download MySQL Server 8.0, install it on your computer and create a database
- Optional install mysql workbench for easier database work
- Download millionaire-app-backend repository:
```bash
 git clone https://github.com/Grzegorz96/millionaire-app-backend.git
```
- Create .env file in your Backend folder
- Add the required environment variables to the .env file
- Create the required tables in the database
- Install required packages on your venv:
```bash
  pip install Flask
  pip install PyJWT
  pip install mysql-connector-python
  pip install python-dotenv 
```
- Run API.py:
```bash
 py .\API.py
```

## API Reference

#### HTTP GET METHODS

```http
  GET /questions
  GET /users/register/check-data
  GET /scores
  GET /users/login
  GET /users/<user_id>  
```

| Resource  | Type     | Required | Description                |
| :-------- | :------- | :------- |:------------------------- |
| `questions` | `string`| **Required** |  Your API key |

#### HTTP POST METHODS

```http
  POST /users/send-activation-number
  POST /users/register
  POST /scores
  POST /questions
  GET /users/<user_id>  
```

| Resource  | Type     | Required | Description                |
| :-------- | :------- | :------- |:------------------------- |
| `questions` | `string`| **Required** |  Your API key |

#### HTTP PATCH METHODS

```http
  PATCH /users/<user_id>
```

| Resource  | Type     | Required | Description                |
| :-------- | :------- | :------- |:------------------------- |
| `questions` | `string`| **Required** |  Your API key |

#### HTTP DELETE METHODS

```http
  DELETE /users/<user_id>
```

| Resource  | Type     | Required | Description                |
| :-------- | :------- | :------- |:------------------------- |
| `questions` | `string`| **Required** |  Your API key |


## Lessons Learned

While creating this project, I learned how to combine many programs. I've worked on different libraries with different technologies. I had to implement JWT tokens myself so that the frontend program could catch the returned new access tokens, overwrite the expired one in the user object and repeat the query again. I created user login and registration logic so that all processes are safe for the user. Logging in consists of 2 steps, the first is to check whether the given user is in the database, then if so, downloading his id and creating a JWT for him, the next query is a request for information about this user, using the ID and access token. Registration consists of 3 steps, the first is to check if the given user is not already in the database, the next is to check if the given email really belongs to the user by sending the user an e-mail to verify the e-mail address before registration, the last step is to place the user in the database. I think that implementing these functions took me the most time but also learned a lot. I learned to connect with the proprietary API that performs queries on the database. It also took me a long time to catch most of the bugs and handle them. I increased my skills in creating program logic. I gained knowledge about the implementation of graphic and sound files in the application.


## Features to be implemented

- Additional data validation on the backend. At the moment, data validation takes place only on the frontend.


## Authors

- [@Grzegorz96](https://www.github.com/Grzegorz96)


## Contact

E-mail: grzesstrzeszewski@gmail.com


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Screnshoots
