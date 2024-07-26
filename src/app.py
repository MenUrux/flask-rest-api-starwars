"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(name=body['name'], email=body['email'], password=body['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

""" [GET] /planets Get a list of all the planets in the database. """
@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planet(name=body['name'], climate=body['climate'], terrain=body['terrain'])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

""" [GET] /planets/<int:planet_id> Get one single planet's information. """
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

""" [GET] /people Get a list of all the people in the database. """
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(characters), 200

@app.route('/characters', methods=['POST'])
def create_character():
    body = request.get_json()
    new_character = Character(name=body['name'], birth_year=body['birth_year'], gender=body['gender'])
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

""" [GET] /people/<int:people_id> Get one single person's information. """
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        raise APIException('Character not found', status_code=404)
    return jsonify(character.serialize()), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/favorites', methods=['POST'])
def create_favorite():
    body = request.get_json()
    new_favorite = Favorite(user_id=body['user_id'], favorite_id=body['favorite_id'], favorite_type=body['favorite_type'])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201


""" [DELETE] /favorite/planet/<int:planet_id> Delete a favorite planet with the id = planet_id. """
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(user_id=request.user.id, favorite_id=planet_id, favorite_type='planet').first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200


""" [DELETE] /favorite/people/<int:people_id> Delete a favorite people with the id = people_id. """
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite = Favorite.query.filter_by(user_id=request.user.id, favorite_id=people_id, favorite_type='people').first()
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
