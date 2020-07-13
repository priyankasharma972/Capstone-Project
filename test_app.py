
from dotenv import load_dotenv
load_dotenv()

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from database.models import setup_db, db_drop_and_create_all, Actor, Movie, db


database_path="postgresql://postgres:Hari987@localhost:5432/capstone_testdb"


CASTING_ASSISTANT_TOKEN = os.environ.get('CASTING_ASSISTANT_TOKEN')
CASTING_DIRECTOR_TOKEN = os.environ.get('CASTING_DIRECTOR_TOKEN')
EXECUTIVE_PRODUCER_TOKEN = os.environ.get('EXECUTIVE_PRODUCER_TOKEN')

def set_auth_header(role):
    if role == 'casting-assistant':
        return {'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)}
    elif role == 'casting-director':
        return {'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)}
    elif role == 'executive-producer':
        return {'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}

class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    

    #GET MOVIES SUCCESS
    def test_get_movies(self):

        # get response and load data
        response = self.app.get('/movies', headers=set_auth_header('casting-assistant'))
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    #GET MOVIES UNAUTHORIZED
    def test_get_movies_unauthorized(self):

        # send request without token, load response
        response = self.app.get('/movies', headers=set_auth_header(''))
        # check status code and message
        self.assertEqual(response.status_code, 401)

    #POST MOVIES SUCCESS
    def test_add_movies(self):
        data = {
            "title": "radhika",
            "release_date": "11"
          }
        response = self.app.post('/movies', json=data, headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['success'], True)

    #POST MOVIES UNAUTHORIZED
    def test_add_movies_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "release_date"
            }
        response = self.app.post('/movies', json=data, headers=set_auth_header('casting-assistant'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()['success'], False)

    #POST MOVIES FAILED
    def test_add_movies_failed(self):
        response = self.app.post('/movies', json={}, headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['success'], False)

    #UPDATED MOVIES SUCCESS
    def test_update_movie_details(self):
        data = {
            "title": "title",
            "release_date": "23"}
        self.app.post('/movies', json=data,headers=set_auth_header('executive-producer'))
        movie_id = Movie.query.first().id
        response = self.app.patch(f'/movies/{movie_id}', json=data,headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success'], True)

    #UPDATED MOVIES FAILED
    def test_update_movie_details_failed(self):
        data = {
            "title": "title",
            "release_date": "23"}
        self.app.post('/movies', json=data,headers=set_auth_header('executive-producer'))
        movie_id = Movie.query.first().id
        response = self.app.patch(f'/movies/{movie_id}', json={
            "title": '',
            "release_date": ''
        },headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 400)

    #DELETE MOVIE SUCCESS
    def test_delete_movie(self):
        data = {
            "title": "title",
            "release_date": "23"
        }
        self.app.post('/movies', json=data, headers=set_auth_header('executive-producer'))
        movie_id = Movie.query.first().id
        response = self.app.delete(f'/movies/{movie_id}', json=data,headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success'], True)
    
    #DELETE MOVIE UNAUTHORIZED
    def test_delete_movie_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "23"
        }
        self.app.post('/movies', json=data, headers=set_auth_header('executive-producer'))
        movie_id = Movie.query.first().id
        response = self.app.delete(f'/movies/{movie_id}', json=data,headers=set_auth_header('casting-director'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()['message'], {'code': 'unauthorized', 'description': 'Permission not found.'})

    #GET ACTORS SUCCESS
    def test_get_actors(self):
        response = self.app.get('/actors', headers=set_auth_header('casting-assistant'))
        self.assertEqual(response.status_code, 200)

    #GET ACTORS UNAUTHORIZED
    def test_get_actors_unauthorized(self):
        response = self.app.get('/actors', headers=set_auth_header(''))
        self.assertEqual(response.status_code, 401)

    #POST ACTORS SUCCESS
    def test_post_actor(self):
        data = {
            "name": "Priyanka",
            "gender": "Female"
        }
        response = self.app.post('/actors', json=data, headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['success'], True)

    #POST ACTORS FAILED
    def test_post_actor_failed(self):
        response = self.app.post('/actors', json={}, headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['success'], False)

    #POST ACTORS UNAUTHORIZED
    def test_post_actor_unauthorized(self):
        data = {
            "name": "Priyanka",
            "gender": "Female"
        }
        response = self.app.post('/actors', json=data, headers=set_auth_header('casting-assistant'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()['message'], {'code': 'unauthorized', 'description': 'Permission not found.'})

    #UPDATE ACTORS SUCCESS
    def test_update_actor(self):
        data = {
            "name": "Priyanka",
            "gender": "Female"
        }
        self.app.post('/actors', json=data,headers=set_auth_header('executive-producer'))
        actor_id = Actor.query.first().id
        response = self.app.patch(f'/actors/{actor_id}', json=data,headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success'], True)

    #UPDATE ACTORS UNAUTHORIZED
    def test_update_actor_unauthorized(self):
        data ={
            "name": "Priyanka",
            "gender": "Female"
        }
        self.app.post('/actors', json=data,headers=set_auth_header('executive-producer'))

        actor_id = Actor.query.first().id
        response = self.app.patch(f'/actors/{actor_id}', json=data,headers=set_auth_header('casting-assistant'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()['message'], {'code': 'unauthorized', 'description': 'Permission not found.'})

    #UPDATE ACTORS FAILED
    def test_update_actor_failed(self):
        data = {
            "name": "Priyanka",
            "gender": "Female"
        }
        self.app.post('/actors', json=data,headers=set_auth_header('executive-producer'))
        actor_id = Actor.query.first().id
        response = self.app.patch(f'/actors/{actor_id}', data={},headers=set_auth_header('casting-assistant'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()['message'], {'code': 'unauthorized', 'description': 'Permission not found.'})

    #DELETE ACTORS SUCCESS
    def test_delete_actor(self):
        data = {
            "name": "Priyanka",
            "gender": "Female"
        }
        self.app.post('/actors', json=data,headers=set_auth_header('executive-producer'))
        actor_id = Actor.query.first().id
        response = self.app.delete(f'/actors/{actor_id}', json=data,headers=set_auth_header('executive-producer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['success'], True)

    #DELETE ACTORS UNAUTHORIZED
    def test_delete_actor_unauthorized(self):
        data = {
            "name": "Priyanka",
            "gender": "Female"
        }
        self.app.post('/actors', json=data,headers=set_auth_header('executive-producer'))
        actor_id = Actor.query.first().id
        response = self.app.delete(f'/actors/{actor_id}', json=data,headers=set_auth_header('casting-assistant'))
        self.assertEqual(response.status_code, 403)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
