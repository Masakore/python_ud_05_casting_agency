from os import name
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers

from app import create_app
from models import Movie, Actor, Gender


casting_agent_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImgzSHZERzI5NU51NlZpbmJOVFRnNiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZC1weS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjExMjhjZDVkMDU2NzUwMDcwZGM5YjY3IiwiYXVkIjoibW9kZWxfYWdlbmN5IiwiaWF0IjoxNjMwMjA2MzA5LCJleHAiOjE2MzAyOTI3MDksImF6cCI6ImtKVkVBWGZhV2xwQ2hSQWlTaUxkS1VpVERITlFIbmZFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.ykfvo9S3zzsGtS9Khy8E24-zu1lW09VfkPasgeAynkiUtyGeh2dUvpBez0SwxiPqwUThimXTdw0Wou7P1qB2XXPhXk2ni0M17pIh8C7BBn57nSARLNouPPq77nlYPzqLyS9jADG66wfSFer0cWGfeAMp3uj4LQlFWG91YRpF6VtC7xDi8hlllWQSc_N1nLvyL-xFohuJHPQ2vWi0lAQ_Cg6-jBEj7HlRhQkzGJ4rcL3Xil8EbXyLE098I0_mfkeGwV3MypkldENwAvhdUIGqXqiS11SKSWfaahNYA0KF9TdG-3-XzIOry9QVaK2TDs8GysmNWyZ_S1KcnUaul9QQUg"
casting_director_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImgzSHZERzI5NU51NlZpbmJOVFRnNiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZC1weS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyYWQ2OWViNWIwNzYwMDZhZjQ5OGE3IiwiYXVkIjoibW9kZWxfYWdlbmN5IiwiaWF0IjoxNjMwMjA2Mzg0LCJleHAiOjE2MzAyOTI3ODQsImF6cCI6ImtKVkVBWGZhV2xwQ2hSQWlTaUxkS1VpVERITlFIbmZFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyJdfQ.kUBWZmcP3LUYE-gHuElCBm1tQU9fSgqxXBtygKKfWevi9GQPRNcA8_cEMItotLrbtnlhHOcef7jKNiM5dKI4O12v3Yy9QZKIrHRLVdCIkXQCGeq_9lrINvS7tTf-RHDUJWjDTHJBMJKIMi-E98n2GHvINre9rik3cYP0Vsglva7kjOXOZPaIAGsMZ85i7LCB8EiRqSo2fKvSPwbHGGJltNzUTXKQdi0u0TNTktCF0Qa2WoJ4JLKnLaZIfC0fszBziAreA1P8Nsa7a1xlURTeipyzZW5aVwck14KgNE0h7Jpe5dJy-ScoPxQuK--7jmjk4tV3tNbXP7NxKefwIp6xFg"
executive_producer_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImgzSHZERzI5NU51NlZpbmJOVFRnNiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZC1weS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEwYWFhNTJlMTZiOTEwMDZhZDU0OWY3IiwiYXVkIjoibW9kZWxfYWdlbmN5IiwiaWF0IjoxNjMwMjA2NDI3LCJleHAiOjE2MzAyOTI4MjcsImF6cCI6ImtKVkVBWGZhV2xwQ2hSQWlTaUxkS1VpVERITlFIbmZFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.nRWKv1Kf7J2lGCMXRdJTE3Ux-UGvKWFv0qUEmYvaPw2IdOCHGC9uAnqtsFVMAmwSunHrXXJvU0jogiiO6H4we1iuUK50V8IbuHXiuDiryfNZVPjdj1tDgHTa-QotxB7xOOtza_EJnkjGfoh8vFrQN8GfB1X1kdaKPXNpXMVgJGOe_whzKI4183XjtKnpJdxvb1Q_36M4SpapRjURhLz36AbbMhJBiVJlkhaREKMCcV_E1aGx2Wi1TNQTg1vvv9rvxMfrYuf2zNXpVIR3ga-0G7Gz5Y75ih3Xf-fTYGIO291mTXuQJ0rFZcCcyU571fwA9qnHsstdNJECUITiypOQcA"
CASTING_AGENT = 'casting_agent'
CASTING_DIRECTOR = 'casting_director'
EXECUTIVE_PRODUCER = 'executive_producer'


def getAuthHeader(role):
    jwt = None
    if role == 'casting_agent':
        jwt = casting_agent_jwt
    elif role == 'casting_director':
        jwt = casting_director_jwt
    elif role == 'executive_producer':
        jwt = executive_producer_jwt

    header = {
        'Authorization': 'Bearer ' + jwt
    }

    return header


class ModelAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(True)
        self.client = self.app.test_client

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        # TODO find a better way to delete the previous data on db
        # self.db.drop_all() didn't work
        Movie.query.delete()
        Actor.query.delete()

    def test_get_movies(self):
        Movie(title='Go for it', release_date='2020-08-01').insert()
        movie_response = self.client().get('/movies', headers=getAuthHeader(CASTING_AGENT))
        data = json.loads(movie_response.data)

        self.assertEqual(movie_response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    def test_404_returns_on_get_movies(self):
        res = self.client().get('/movies', headers=getAuthHeader(CASTING_AGENT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_actors(self):
        Actor(name='John', age='35', gender=Gender.male.value).insert()
        res = self.client().get('/actors', headers=getAuthHeader(CASTING_AGENT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    def test_404_returns_on_get_actors(self):
        res = self.client().get('/actors', headers=getAuthHeader(CASTING_AGENT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        Movie(title='Go for it', release_date='2020-08-01').insert()
        res = self.client().get('/movies', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        id = data['movies'][0]['id']
        res = self.client().delete(f'/movies/{id}', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'], id)

    def test_404_returns_on_delete_movie(self):
        res = self.client().delete('/movies/99999', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        Actor(name='John', age='35', gender=Gender.male.value).insert()
        res = self.client().get('/actors', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        id = data['actors'][0]['id']
        res = self.client().delete(f'/actors/{id}', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'], id)

    def test_404_returns_on_delete_actor(self):
        res = self.client().delete('/actors/99999', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_movie(self):
        res = self.client().post(
            '/movies', json={'title': 'TEST', 'release_date': '2021-08-01'}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_422_error_on_create_movie_if_required_field_is_missing(self):
        res = self.client().post(
            '/movies', json={'title': 'TEST'}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_actor(self):
        res = self.client().post(
            '/actors', json={'name': 'TEST', 'age': 35, 'gender': 'female'}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_422_error_on_create_actor_if_required_field_is_missing(self):
        res = self.client().post(
            '/actors', json={'name': 'TEST', 'age': 35}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        Movie(title='Go for it', release_date='2020-08-01').insert()
        res = self.client().get('/movies', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        id = data['movies'][0]['id']
        res = self.client().patch(
            f'/movies/{id}', json={'title': 'TEST'}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'TEST')

    def test_422_on_update_movie_if_all_required_fields_are_missing(self):
        Movie(title='Go for it', release_date='2020-08-01').insert()
        res = self.client().get('/movies', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        id = data['movies'][0]['id']
        res = self.client().patch(
            f'/movies/{id}', json={}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_update_actor(self):
        Actor(name='John', age='35', gender=Gender.male.value).insert()
        res = self.client().get('/actors', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        id = data['actors'][0]['id']
        res = self.client().patch(
            f'/actors/{id}', json={'name': 'TEST'}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'TEST')

    def test_422_on_update_actor_if_all_required_fields_are_missing(self):
        Actor(name='John', age='35', gender=Gender.male.value).insert()
        res = self.client().get('/actors', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        id = data['actors'][0]['id']
        res = self.client().patch(
            f'/actors/{id}', json={}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Casting Agent test cases
    def test_casting_agent_can_get_actors(self):
        Actor(name='John', age='35', gender=Gender.male.value).insert()
        res = self.client().get('/actors', headers=getAuthHeader(CASTING_AGENT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    def test_casting_agent_cannot_create_actor(self):
        res = self.client().post(
            '/actors', json={'name': 'TEST', 'age': 35, 'gender': 'female'}, headers=getAuthHeader(CASTING_AGENT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Casting Director test cases
    def test_casting_agent_can_create_actor(self):
        res = self.client().post(
            '/actors', json={'name': 'TEST', 'age': 35, 'gender': 'female'}, headers=getAuthHeader(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_casting_agent_cannot_create_movie(self):
        res = self.client().post(
            '/movies', json={'title': 'TEST', 'release_date': '2021-08-01'}, headers=getAuthHeader(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Exective Producer test cases
    def test_exective_producer_can_create_movie(self):
        res = self.client().post(
            '/movies', json={'title': 'TEST', 'release_date': '2021-08-01'}, headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_exective_producer_can_delete_movie(self):
        Movie(title='Go for it', release_date='2020-08-01').insert()
        res = self.client().get('/movies', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        id = data['movies'][0]['id']
        res = self.client().delete(f'/movies/{id}', headers=getAuthHeader(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'], id)

if __name__ == "__main__":
    unittest.main()
