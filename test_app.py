import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

CASTING_DIRECTOR= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVvWVFrSU50LTlBdWxFdGh4WjJpNiJ9.eyJpc3MiOiJodHRwczovL3Jhd2FubWFjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTFiZWQ0ODhjYWVjZDAwNjkyMDQ2MTYiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYzMjc2ODc5OSwiZXhwIjoxNjMyNzc1OTk5LCJhenAiOiJWNURIcUU4aVlnaTdad3NuR3RHVUdTUVVCbVMyeDdMMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3Rvcl9kZXRhaWxzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZV9kZXRhaWxzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.ib9HQabV6V2FiGFgZo4zArWYK6UMEb3aMRc16sOYV1Rw76vRIZFz3bg3bdOHSQr7kzewA8f7ynfsKSY47glOfnJfHhGMyhDWax0lLrlDCPTqD69O1wRKam5YQbmYctbQvsie5lt6oiHtGltbFXjLsgw6tyt5pptWXZxu8kCiA4DmVkIKTGQAJb9VQBxRmqjkWXOVx0OGEW103YsE6codx2Ic2v4iI_LykB0N8TjykdAaHNKOAi-oREAHenGs9--_vgotlM9xhlhFZP3SBV2qlIDu_aAl7ZSTfPh_dQ3U1kNNRqN4DY-hpp2jnN3jEzI1sIOSN1XgeSwKz3B0Ilo2lQ"
CASTING_ASSISTANT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVvWVFrSU50LTlBdWxFdGh4WjJpNiJ9.eyJpc3MiOiJodHRwczovL3Jhd2FubWFjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTRmN2ExYjFlMzhkOTAwNjg1NzVmYmMiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYzMjc2ODYwMCwiZXhwIjoxNjMyNzc1ODAwLCJhenAiOiJWNURIcUU4aVlnaTdad3NuR3RHVUdTUVVCbVMyeDdMMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9yX2RldGFpbHMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllX2RldGFpbHMiLCJnZXQ6bW92aWVzIl19.QFwsh0qtBBHcn88HMknV0F0agJnXCb6d13x_SDlBbDV44QO3zTxKBXHN1FhI-4nsVmH_lAhuVc_3_ADrFu1NUsVMByKjJAiwsU4uf1MhzuisL6M9e0ZtIhmu2lVDiLmkoUUTowyjzhphWnCG1DR5fp4QgaIx9xv_bPQcMEIK-osoNMS9Mn7DwvUR9Q3Pih0yckwzIFAnf-xJUKUNCdLJGtIkDF0LfD5M1LfRD-NOwA8j4ZDpuEeuXqCMOCF_O5ejg4PH5cADyCcawJq7TDEqnPvHhThv_vrHr92deCWy8DCO5A8AntR8AgHstnHPLo3aHVU5ET-UhppwrIS0fyaOXA"; 
EXECUTIVE_PRODUCER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVvWVFrSU50LTlBdWxFdGh4WjJpNiJ9.eyJpc3MiOiJodHRwczovL3Jhd2FubWFjLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTFiZWNmYzM0NzZmYjAwNzE1YTY3ZmUiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYzMjc2ODcwMywiZXhwIjoxNjMyNzc1OTAzLCJhenAiOiJWNURIcUU4aVlnaTdad3NuR3RHVUdTUVVCbVMyeDdMMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JfZGV0YWlscyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVfZGV0YWlscyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.kYz4H7-Yf1o2wKYNGItzdnoaLRCOuikmBiBpW2lAZnlN9jNGJkm8ykdMrR60kImug0SnFOQc6K1WH5p2f-_IWUYqZsDkYF1OhjWIFjEOCwndhHLxS5wuRUE3jtLkEgZPE2Fp64H5md91HkxVKULN9PFsH8agxI3igAp9CPpXJQ-dWGDVtREEv06P7sztTh0awovbPjIAoTLazArBbfLVsfoL22P_rokpIUKo-4UQXXz4jam-Mj6Y9v904m8lv0tRHeiTZwElRBoOEClurs4cJW1oHW4bzb4LOnwK001tbmwtE-mHiXgF5LZLovB99VYvKUVH4a7EZtTt4K1g_o2YdA"


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '2130107','localhost:5432', "casting_agency")
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'mary',
            'age': 20,
            'gender': "female"
        }

        self.new_movie = {
            'title': 'The handmaiden',
            'release_date': '10/12/2016'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # /actors test

    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_sent_invalid_actor_request(self):

        res = self.client().get('/actors/male',
                                headers={
                                    "Authorization": "Bearer " + CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # /actor-details test

    def test_get_actor_details(self):

        res = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_404_sent_invalid_actor_id(self):

        res = self.client().get(
            '/actors/600000000000',            
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # /movies test

    def test_get_movies(self):

        res = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_sent_invalid_movie_request(self):

        res = self.client().get('/movies/new',
                                headers={
                                    "Authorization": "Bearer " + CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # /movie-details test

    def test_get_movie_details(self):

        res = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_sent_invalid_movie_id(self):

        res = self.client().get(
            '/movies/900000000000',            
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


    # /actors/{} Delete test

    def test_delete_actor(self):

        total_actors = len(Actor.query.all())
        actor = Actor(name=self.new_actor['name'], age=self.new_actor['age'],
                            gender=self.new_actor['gender'])
        actor.insert()
        actor_id = actor.id

        res = self.client().delete(f'/actors/{actor_id}', 
        headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(res.data)

        actor = Actor.query.filter(
            Actor.id == actor.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(data['total_actors'], total_actors)
        self.assertEqual(actor, None)

    def test_404_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/ten', 
        headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # /movies/{} Delete test

    def test_delete_movie(self):

        total_movies = len(Movie.query.all())
        movie = Movie(title=self.new_movie['title'], release_date=self.new_movie['release_date'])
        movie.insert()
        movie_id = movie.id

        res = self.client().delete(f'/movies/{movie_id}', 
        headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(res.data)

        movie = Movie.query.filter(
            Movie.id == movie.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)
        self.assertEqual(data['total_movies'], total_movies)
        self.assertEqual(movie, None)

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete('/movie/eleven',
                headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # /actors Post test

    def test_add_actor(self):

        total_actors = len(Actor.query.all())
        res = self.client().post('/actors', json=self.new_actor,
                         headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
                         )

        data = json.loads(res.data)
        new_total = len(Actor.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(new_total - total_actors, 1)

    def test_422_if_actor_creation_fails(self):

        res = self.client().post('/actors', json={
            'name': '',
            'age': 'one',
            'gender': "elder",
        }, 
        headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    # /movies Post test

    def test_add_movie(self):

        total_movies = len(Movie.query.all())
        res = self.client().post('/movies', json=self.new_movie,
                         headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
                         )

        data = json.loads(res.data)
        new_total = len(Movie.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(new_total - total_movies, 1)

    def test_422_if_movie_creation_fails(self):

        res = self.client().post('/movies', json={
            'title': '',
            'release_date': 'two thousend',
        }, 
        headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")


    # /actor/{} edit test

    def test_edit_actor(self):
        res = self.client().patch('/actors/1', json=self.new_actor,
                                  headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_actor(self):
        update_actor = {}
        res = self.client().patch('/actors/2', json={"name": "amy"},
                                  headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    # /movies/{} edit test

    def test_edit_movie(self):
        res = self.client().patch('/movies/1', json=self.new_movie,
                                  headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_update_movie(self):
        update_actor = {}
        res = self.client().patch('/movies/2', json={"title": "robber"},
                                  headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    # RBAC tests

    # Casting assistant
    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies',
                                headers={"Authorization": "Bearer " +  CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_update_actor_casting_assistant(self):
        res = self.client().patch('/movies/1', json=self.new_movie,
                                  headers= {"Authorization": "Bearer " +  CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")


    # Casting Director
    def test_get_actor_details_casting_director(self):
        res = self.client().get('/actors/1',
                                headers={"Authorization": "Bearer " +  CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_add_movie_casting_assistant(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": "Bearer " +  CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    # EXECUTIVE_PRODUCER

    def test_get_actors_executive_producer(self):
        res = self.client().get('/actors',
                                headers={"Authorization": "Bearer " +  EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_actor_executive_producer(self):
        add_actor = {'name': 'rawan', 'age': 21, "gender": "female"}
        res = self.client().post('/actors', json= add_actor, 
                                headers={"Authorization": "Bearer " +  EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
