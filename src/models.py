from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#como no me dejaba con "Base", tuve que buscar cómo hacerlo con db.Model y los demás.

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorite', backref='user')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'gender': self.gender
        }

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    favorite_id = db.Column(db.Integer, nullable=False)
    favorite_type = db.Column(db.String(50), nullable=False)

    #con mapperargs pude hacer lo de favoritos
    __mapper_args__ = {
        'polymorphic_on': favorite_type,
        'polymorphic_identity': 'favorite'
    }

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'favorite_id': self.favorite_id,
            'favorite_type': self.favorite_type
        }

class CharacterFavorite(Favorite):
    __mapper_args__ = {
        'polymorphic_identity': 'character'
    }

class PlanetFavorite(Favorite):
    __mapper_args__ = {
        'polymorphic_identity': 'planet'
    }
