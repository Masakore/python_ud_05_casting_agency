# from sqlalchemy import Column
import enum
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

db = SQLAlchemy()


def setup_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()

    # migrate = Migrate(app, db)


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'<Movie {self.id}, {self.title}, {self.release_date}'


class Gender(enum.Enum):
    male = 1
    female = 2
    others = 3


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    gender = db.Column(db.Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': Gender(self.gender).name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'<Actor {self.id}, {self.name}, {self.age}, {self.gender}'
