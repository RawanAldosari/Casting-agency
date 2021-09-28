import os
from models import Actor, Movie, setup_db
from flask import Flask, request, abort, jsonify, session, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
import json
from auth import AuthError, requires_auth

# AUTH0_CALLBACK_URL = constants.AUTH0_CALLBACK_URL
# AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
# AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
# AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
# AUTH0_BASE_URL = 'https://' + os.environ['AUTH0_DOMAIN']
# AUTH0_AUDIENCE = constants.AUTH0_AUDIENCE



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)


  return app


app = create_app()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, PATCH, DELETE, OPTIONS')
    return response


@app.route('/')
def health():
    return render_template('index.html')      

@app.route('/callback')
def callback(response):
    return {
        'token': response.headers
        }

# ROUTES
# @app.route('/login')
# def login():
#      return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
#                                      audience=AUTH0_AUDIENCE)
                                    


'''
endpoint
    GET requests
'''
@app.route("/actors")
@requires_auth('get:actors')
def get_actors(payload): 
    all_actors = Actor.query.order_by(Actor.id).all()    

    if all_actors is None:
        abort(404)

    actors = [actor.format() for actor in all_actors]

    return {
        "success": True, 
        "actors": actors
    }, 200



@app.route("/movies/<int:id>", methods=['GET'])
@requires_auth('get:actor_details')
def get_actors_details(payload,id): 

    actor= Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None: 
        abort(404)

    return {
        "success": True, 
        "actor": actor
    }, 200


@app.route("/movies")
@requires_auth('get:movies')
def get_movies(payload): 
    all_movies = Movie.query.order_by(Movie.id).all()    

    if all_movies is None:
        abort(404)

    movies = [movie.format() for movie in all_movies]
    return {
        "success": True, 
        "movies": movies
    }, 200


@app.route("/movies/<int:id>", methods=['GET'])
@requires_auth('get:movie_details')
def get_movies_details(payload,id): 

    movie= Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None: 
        abort(404)

    return {
        "success": True, 
        "movie": movie
    }, 200

'''
endpoint
    POST 
'''
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movie(payload): 
    body = request.get_json()

    try:
        if 'title' and 'release_date' not in body:
            abort(400)
        
        movies =  Movie.query.all()

        title = body['title']
        release_date = body['release_date']

        for movie in movies: 
            if (movie['title'] == title and movie["release_date"] == release_date): 
                abort(400)
        
        movie = Movie(title= title, release_date= release_date)
        movie.insert()

        total_movies= len(movies)

        return {
            "success": True,
            "movie": [movie.format()], 
            "total_movies": total_movies
        }, 200


    except Exception as e:
        print(e)
        abort(404)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(payload): 
    body = request.get_json()

    try:
        if 'name' and 'age' and 'gender' not in body:
            abort(400)

        
        actors =  Actor.query.all()

        name = body['name']
        age = body['age']
        gender = body['gender']

        for actor in actors: 
            if actor['age'] == age and actor["name"] == name and actor["gender"] == gender: 
                abort(400)
        
        actor = Actor(name= name, age= age, gender=gender)
        actor.insert()

        total_actors= len(Actor.query.all())

        return {
            "success": True,
            "actor": [actor.format()], 
            "total_actors": total_actors
        }, 200

    except Exception as e:
        print(e)
        abort(404)

'''
@TODO implement endpoint
    PATCH 
'''
@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def edit_movie(payload, id): 

    movie= Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None: 
        abort(404)

    body = request.get_json()

    try:
        if 'title' and 'release_date' not in body:
            abort(422)

        title = body['title']
        release_date = body['release_date']

        movie.title= title
        movie.release_date= release_date
        movie.update()

        return {
            "success": True,
            "movie": [movie.format()]
        }, 200

    except Exception as e:
        print(e)
        abort(400)

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def edit_actor(payload, id): 

    actor= Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None: 
        abort(404)

    body = request.get_json()

    try:
        if 'name' and 'age' and 'gender' not in body:
            abort(422)

        name = body['name']
        age = body['age']
        gender = body['gender']

        actor.name= name
        actor.age= age
        actor.gender= gender
        actor.update()

        return {
            "success": True,
            "actor": [actor.format()]
        }, 200

    except Exception as e:
        print(e)
        abort(400)

'''
@TODO implement endpoint
    DELETE 
'''

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, id): 

    movie= Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None: 
        abort(404)

    try:
        movie.delete()
        total_movies= len(Movie.query.all())


        return {
            "success": True,
            "delete": id, 
            "total_movies": total_movies
        }, 200

    except Exception as e:
        print(e)
        abort(400)


@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, id): 

    actor= Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None: 
        abort(404)

    try:
        actor.delete()
        total_actors= len(Actor.query.all())

        return {
            "success": True,
            "delete": id, 
            "total_actors": total_actors
        }, 200

    except Exception as e:
        print(e)
        abort(400)


# Error Handling
'''
Example error handling for unprocessable entity
'''

# error handler for 422
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

# error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


# error handler for 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)