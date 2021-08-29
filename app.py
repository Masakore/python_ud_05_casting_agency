from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Movie, Actor, Gender
from werkzeug.exceptions import NotFound, UnprocessableEntity
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    config = 'config'if test_config is None else 'dev_config'
    app.config.from_object(config)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTION')
        return response

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        try:
            result = Movie.query.all()

            if len(result) == 0:
                abort(404)

            movies = []
            for movie in result:
                movies.append(movie.format())

            return jsonify({
                "success": True,
                "movies": movies
            }), 200

        except NotFound:
            abort(404)

        except Exception:
            abort(500)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        try:
            result = Actor.query.all()

            if len(result) == 0:
                abort(404)

            actors = []
            for actor in result:
                actors.append(actor.format())

            return jsonify({
                "success": True,
                "actors": actors
            }), 200

        except NotFound:
            abort(404)

        except Exception:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                "success": True,
                "delete": movie_id
            }), 200

        except NotFound:
            abort(404)

        except Exception:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                "success": True,
                "delete": actor_id
            }), 200

        except NotFound:
            abort(404)

        except Exception:
            abort(500)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if (new_title is None or new_release_date is None):
            abort(422)

        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            return jsonify({
                'success': True
            }), 201

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if (new_name is None or new_age is None or new_gender is None):
            abort(422)

        try:
            actor = Actor(name=new_name, age=new_age,
                          gender=Gender[new_gender].value)
            actor.insert()

            return jsonify({
                'success': True
            }), 201

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if (new_title is None and new_release_date is None):
            abort(422)

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            if (new_title is not None) and len(new_title) != 0:
                movie.title = new_title

            if (new_release_date is not None) and len(new_release_date) != 0:
                movie.title = new_release_date

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if (new_name is None and new_age is None and new_gender is None):
            abort(422)

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)

            if (new_name is not None) and len(new_name) != 0:
                actor.name = new_name

            if (new_age is not None) and len(new_age) != 0:
                actor.age = new_age

            if (new_gender is not None) and len(new_gender) != 0:
                actor.gender = new_gender

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

        except UnprocessableEntity:
            abort(422)

        except Exception:
            abort(500)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5000, debug=True)