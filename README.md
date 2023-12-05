## Full Stack Developer Nanodegree Program - Udacity x Misk 

January 27, 2021

Part 5: Capstone Project
Project 5: Capstone Project
-----

# Full Stack - Capstone Project

## About
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Motivation
This is the final project in the Full Stack Nanodegree.
Bulding this project ensures the understaning of all the concepts in this ND
- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Virual Env
```
python3 -m virtualenv env
source env/bin/activate
```

#### PIP Dependencies

To install all necessary dependencies:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
## Running the Test
```
python3 test.py
```
We can now also open the application via Heroku using the URL:
https://halafsndcapstone.herokuapp.com/

The live application can only be used to generate tokens via Auth0, the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.

## DATA MODELING:

### models.py
Models:
- There are two tables created: Movies and Actors
- Movies with attributes title and release year
- Actors with attributes name, age and gender

## API ARCHITECTURE AND TESTING
### Endpoints

### GET'/actors'
Returns a list of all actors 
Auth requires : Casting Assistant, Casting Director or Executive Producer Role

### GET'/movies'
Returns a list of all movies
Auth requires : Casting Assistant, Casting Director or Executive Producer Role

### DELETE'/actors/id'
Returns a list of all actors after deleting the requested actor
Auth requires : Casting Director or Executive Producer

### DELETE'/movies/id'
Returns a list of all movies after deleting the requested movie
Auth requires : Executive Producer Role

### POST'/actors'
Returns a list of all actors with a new actor
Auth requires : Casting Director or Executive Producer Role
Auth requires : Casting Director or Executive Producer Role

### POST'/movies' 
Returns a list of all movies with a new movie
Auth requires : Executive Producer Role

### PATCH'/actors/id'
Returns a list of all actors with an updated actor
Auth requires : Casting Director or Executive Producer Role
### PATCH'/movies/id'
Returns a list of all movies with an updated movie
Auth requires : Casting Director or Executive Producer Role