import os
import unittest
from flask import json
from main import create_app
from models import Actor, Movie, db
from models import setup_db

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        self.database_name = "casting_agency_test"
        self.database_path = f"postgresql://postgres@localhost:5432/{self.database_name}"

        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

        self.new_actor = {
            'name': 'Test Actor',
            'age': 30,
            'gender': "Male"}
        self.new_movie = {
            'title': 'Test Movie',
            'release_date': '2023-10-01'
        }

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        pass

    def _auth_header(self, token):
        return {
            'Authorization': f'Bearer {token}'
        }
    def test_get_actors_authoriuzed(self):
        res = self.client().get('/actors', headers=self._auth_header(os.environ.get("assistant_token")))
        self.assertEqual(res.status_code, 200)
        
    def test_get_actors_unauthorized(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_post_actor_director(self):
        res= self.client().post('/actors', json=self.new_actor, headers=self._auth_header(os.environ.get("director_token")))
        self.assertEqual(res.status_code, 201)

    def test_post_actor_assistant(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self._auth_header(os.environ.get("assistant_token")))
        self.assertEqual(res.status_code, 403)

    def test_patch_actor(self):
        with self.app.app_context():
            actor = Actor(name='Test Actor', age=50, gender="Male")
            db.session.add(actor)
            db.session.commit()
            actor_id = actor.id
        res=self.client().patch(f'/actors/{actor_id}', json={
            'name': 'Updated Actor',
            'age': 55,
            'gender': 'Male'
        }, headers=self._auth_header(os.environ.get("director_token")))
        self.assertEqual(res.status_code, 200)

    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/9999', json={
            'name': 'Updated Actor',
            'age': 55,
            'gender': "Male",
        }, headers=self._auth_header(os.environ.get("director_token")))
        self.assertEqual(res.status_code, 404)
    
    def test_delete_actor_director(self):
        with self.app.app_context():
            actor = Actor(name='Test Actor', age=50, gender="Male")
            db.session.add(actor)
            db.session.commit()
            actor_id = actor.id
        res = self.client().delete(f'/actors/{actor_id}', headers=self._auth_header(os.environ.get("director_token")))
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_unauthorized(self):
        with self.app.app_context():
            actor = Actor(name='Test Actor', age=40, gender="male")
            db.session.add(actor)
            db.session.commit()
            actor_id = actor.id
        res = self.client().delete(f'/actors/{actor_id}', headers=self._auth_header(os.environ.get("assistant_token")))
        self.assertEqual(res.status_code, 403)
    
    def test_get_movies_assistant(self):
        res = self.client().get('/movies', headers=self._auth_header(os.environ.get("assistant_token")))
        self.assertEqual(res.status_code, 200)

    def test_post_movie_producer(self):
        self.new_movie = {
            'title': 'New Movie',
            'release_date': '2023-10-01'
        }
        res = self.client().post('/movies', json=self.new_movie, headers=self._auth_header(os.environ.get("producer_token")))
        self.assertEqual(res.status_code, 201)

    def test_delete_movie_producer(self):
        with self.app.app_context():
            movie = Movie(title='Test Movie', release_date='2023-10-01')
            db.session.add(movie)
            db.session.commit()
            movie_id = movie.id
        res = self.client().delete(f'/movies/{movie_id}', headers=self._auth_header(os.environ.get("producer_token")))
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_unauthorized(self):
        res= self.client().delete('/movies/9999', headers=self._auth_header(os.environ.get("assistant_token")))
        self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()
