import os
import json
import unittest
from models import Actors, Movies, setup_db, db
from app import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.Executive = os.environ.get('Executive')
        self.assistant = os.environ.get('ASSISTANT')
        self.director = os.environ.get('DIRECTOR')
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.new_movie = {
            "title": "like a boss",
            "release_date": 2020
        }

        self.new_actor = {
            "name": "Ian Somerhalder",
            "age": 42,
            "gender": "male"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

# success
# Get Endpoint
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': 'Bearer ' + self.assistant})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': 'Bearer ' + self.assistant})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
# POST

    def test_post_actor(self):
        response = self.client().post(
            '/actors', json=self.new_actor,
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movie(self):
        response = self.client().post(
            '/movies', json=self.new_movie,
            headers={'Authorization': 'Bearer ' + self.Executive})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

# Update
    def test_update_actor(self):
        response = self.client().patch(
            '/actors/1',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movies(self):
        response = self.client().patch(
            '/movies/1',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

# Delete
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/1',
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        actor = Actors.query.filter(Actors.id == 1).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_delete_movies(self):
        response = self.client().delete(
            '/movies/1',
            headers={'Authorization': 'Bearer ' + self.Executive})
        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

# Fail
# Get fails

    def test_get_actors_fail(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    def test_get_movies_fail(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

# Post fails
    def test_post_actor_fail(self):
        response = self.client().post(
            '/actors',
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

    def test_post_movie_fail(self):
        response = self.client().post(
            '/movies',
            headers={'Authorization': 'Bearer ' + self.Executive})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

# Update fails

    def test_update_actor_fail(self):
        response = self.client().patch(
            '/actors/1',
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

    def test_update_movies(self):
        response = self.client().patch(
            '/movies/1',
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

# Delete fails

    def test_delete_actor_fail(self):
        response = self.client().delete('/actors/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

    def test_delete_movies_fail(self):
        response = self.client().delete('/movies/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

# RBAC tests

# Assistant
    def test_assistant_post_actor(self):
        response = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + self.assistant})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")

    def test_assistant_update_actor(self):
        response = self.client().patch(
            '/actors/1',
            json=self.new_actor,
            headers={'Authorization': 'Bearer ' + self.assistant})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")

# Director

    def test_director_post_movie(self):
        response = self.client().post(
            '/movies', json=self.new_movie,
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")

    def test_director_delete_movies(self):
        response = self.client().delete(
            '/movies/1',
            headers={'Authorization': 'Bearer ' + self.director})
        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")
# Executive

    def test_executive_post_movie(self):
        response = self.client().post(
            '/movies', json=self.new_movie,
            headers={'Authorization': 'Bearer ' + self.Executive})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_executive_delete_movies(self):
        response = self.client().delete(
            '/movies/1',
            headers={'Authorization': 'Bearer ' + self.Executive})
        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)


if __name__ == "__main__":
    unittest.main()
