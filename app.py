import os
from flask import Flask, jsonify, abort
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth import requires_auth, AuthError


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        # greeting = "Hello"
        # if excited == 'true':
        #     greeting = greeting + "!!!!!"
        return 'hello!'

    # @app.route('/coolkids')
    # def be_cool():
    #     return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/Movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movies.query.all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    @app.route('/Actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actors.query.all()
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/Movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(token):
        try:
            data = request.get_json()
            title = data['title']
            release_year = data['release_year']
            if not title:
                abort(400)
            if not release_year:
                abort(400)
            movie = Movies(title=title, release_year=release_year)
            movie.insert()
            return jsonify({
                'success': True,
                'movies': movie.format()
            }), 200
        except Exception:
            abort(422)

    @app.route('/Actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(token):
        try:
            data = request.get_json()
            name = data['name']
            age = data['age']
            gender = data['gender']
            if not name:
                abort(400)
            if not age:
                abort(400)
            if not gender:
                abort(400)
            actor = Actors(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True,
                'actors': actor.format()
            }), 200
        except Exception:
            abort(422)

    @app.route('/Movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(token, id):
        try:
            data = request.get_json()
            movie = Movies.query.filter_by(id=id).one_or_none()
            title = data.get('title', None)
            release_year = data.get('release_year', None)
            if movie is None:
                abort(400)
            if title is not None:
                movie.title = title
            if release_year is not None:
                movie.release_year = release_year

            movie.update()
            return jsonify({
                'success': True,
                'movies': movie.format()
            }), 200
        except Exception:
            abort(422)

    @app.route('/Actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(token, id):
        try:
            data = request.get_json()
            actor = Actors.query.filter_by(id=id).one_or_none()
            name = data.get('name', None)
            age = data.get('age', None)
            gender = data.get('gender', None)

            if actor is None:
                abort(400)
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender

            actor.update()
            return jsonify({
                'success': True,
                'actors': actor.format()
            }), 200
        except Exception:
            abort(422)

    @app.route('/Actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(token, id):
        try:
            actor = Actors.query.filter(Actors.id == id).one_or_none()

            if actor is None:
                abort(400)
            actor.delete()

            return jsonify({
                'success': True,
                'actors': id
            }), 200
        except Exception:
            abort(422)

    @app.route('/Movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(id):
        try:
            movie = Movies.query.filter(Actors.id == id).one_or_none()
            if movie is None:
                abort(400)
            movie.delete()

            return jsonify({
                'success': True,
                'movies': id
            }), 200
        except Exception:
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resourse not found'
        }), 404

    @app.errorhandler(AuthError)
    def authentication_error(f):
        return jsonify({
            'success': False,
            'error': f.status_code,
            'message': f.error['description'],
            'code': f.error['code']
        }), f.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
