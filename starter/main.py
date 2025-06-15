import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'WELCOME!'
        }), 200


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': formatted_actors
        }),200


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor():
        body = request.get_json()
        if not body:
            abort(400)
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if not name or not age or not gender:
            abort(400)
        
        actor = Actor(name=name, age=age, gender=gender)
        db.session.add(actor)
        db.session.commit()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 201


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name', actor.name)
        age = body.get('age', actor.age)
        gender = body.get('gender', actor.gender)

        actor.name = name
        actor.age = age
        actor.gender = gender

        db.session.commit()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]
            return jsonify({
                'success': True,
                'movies': formatted_movies
            }), 200
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
            body = request.get_json()
            if not body:
                abort(400)
            title = body.get('title')
            release_date = body.get('release_date')
        
            if not title or not release_date:
                abort(400)
        
            movie = Movie(title=title, release_date=release_date)
            db.session.add(movie)
            db.session.commit()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        title = body.get('title', movie.title)
        release_date = body.get('release_date', movie.release_date)

        movie.title = title
        movie.release_date = release_date

        db.session.commit()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)
        
            db.session.delete(actor)
            db.session.commit()
        
            return jsonify({
                'success': True,
                'deleted': actor_id
            }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)

        db.session.delete(movie)
        db.session.commit()

        return jsonify({
            'success': True,
            'deleted': movie_id
        }), 200

    @app.errorhandler(AuthError)
    def auth_error(error):
            return jsonify({
                'success': False,
                'error': error.status_code,
                'message': error.error['description']
            }), error.status_code
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app




if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)