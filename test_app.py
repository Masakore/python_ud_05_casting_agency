from os import name
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers

from app import create_app
from models import Movie, Actor, Gender


casting_agent_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImgzSHZERzI5NU51NlZpbmJOVFRnNiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZC1weS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjExMjhjZDVkMDU2NzUwMDcwZGM5YjY3IiwiYXVkIjoibW9kZWxfYWdlbmN5IiwiaWF0IjoxNjMwMTk2MTAwLCJleHAiOjE2MzAyMDMzMDAsImF6cCI6ImtKVkVBWGZhV2xwQ2hSQWlTaUxkS1VpVERITlFIbmZFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.F6E8jnWu1VGGF59mlhOlzO61kbdprz9AyF75PQziSo4qkbBZLUMmcIcmbLzwLJPxnGiJR63h66IyAuLWZGCQskBsB-6sr-4LMa9eHGVEmtjOTg-aYGLlmgWGP5uF_6moaYhx3F1ExDIveG2bfbcXzPEgdIC7MVIglw2-uD8ZdOWKigPc1mgQKt6EuH1-odzWPF6cUTWgEW5N5J0Cr3W8i2ck9CHmg19xH4eIim2ovonecojuxeP_-Ki5gazgVR6tdll4DUJlxaAGZOqqi9S2Go_5AiO_yy3GVrkQ95q6hTofx8ja-hkZGpfu3a1euwL9AMxOYDlcZ7TFvznw7_f5aA"
casting_director_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImgzSHZERzI5NU51NlZpbmJOVFRnNiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZC1weS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyYWQ2OWViNWIwNzYwMDZhZjQ5OGE3IiwiYXVkIjoibW9kZWxfYWdlbmN5IiwiaWF0IjoxNjMwMTk3NDY5LCJleHAiOjE2MzAyMDQ2NjksImF6cCI6ImtKVkVBWGZhV2xwQ2hSQWlTaUxkS1VpVERITlFIbmZFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyJdfQ.cxJSKB4i6PiqvNtbvmH1cf0BysjVO5UuqyXfa8X_fhPTR1LyUby7PUHwBF4jzzU9hxqf9ghRsCd138nl1qY28aD4IEHeVCaEBr3xYbAK_nAHAGH07IfOkpk3Dm2gGNKCA4B4Fax9P1jheET_k8e8qRyhpefxvKzvC2wVB9I897Hh5nSdFY8qHCIS-krVwMWfuilVEJY10IxqhjItcgGyNyqGx519uJKgdivMRPpbByuK56gXzUlrkbWLABrrCrlxhHV-zRRpsAEIP1kZon0BDCFXYTkgIcXFnfKF6KEj0_QLpTZnFAxsQHM0UCBI4Wbwif2Ywl9HETpV4QpkhwhGRQ"
executive_producer_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImgzSHZERzI5NU51NlZpbmJOVFRnNiJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZC1weS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEwYWFhNTJlMTZiOTEwMDZhZDU0OWY3IiwiYXVkIjoibW9kZWxfYWdlbmN5IiwiaWF0IjoxNjMwMTk2ODMyLCJleHAiOjE2MzAyMDQwMzIsImF6cCI6ImtKVkVBWGZhV2xwQ2hSQWlTaUxkS1VpVERITlFIbmZFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.zdvuRudVQ9NnfNZ3N5qvGvG6d8Kb6K29AVrhs6XqgxzO-SK8SlRDAGqKHqSFlVIzA1l2PikSNhf6fmMrH0SvscH12-UpgCbuxRER81vJgZkueZN5ewms36qEEWhinVU2WJr2cGDjiHR_wrTfW2FFz4PFgneq1Tw9B8ryyky1xD7XP4c2d-PrVV0FFk4yC8BsNrsrWRmALcQoe2XVHkXKwMsRoNR3q4oNqx306F94TGYVz4Avp4h8rdam96yBwH4FfK1lpZ-CUpfd2vum6IhlKrV4l4fJGdml8Zs07hSULeBR5K4-zWmN_a7QuTWyzXx534PS0jGKdDPwYadzPbExXg"
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
