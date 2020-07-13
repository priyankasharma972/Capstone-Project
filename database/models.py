
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
database_path = "postgresql://postgres:Hari987@localhost:5432/capstonedb"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
def db_drop_and_create_all():
    """drops the database tables and starts fresh
    can be used to initialize a clean database"""
    db.drop_all()
    db.create_all()


#----------------------------------------------------------------------------#
# Data Models.
#----------------------------------------------------------------------------#
movie_actor_relationship_table = Table('movie_actor_relationship_table', db.Model.metadata,
                                       Column('movie_id', Integer, ForeignKey('movies.id')),
                                       Column('actor_id', Integer, ForeignKey('actors.id')))

                                       
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title= Column(String(100), unique= True, nullable=False)
    release_date= Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    movies = db.relationship('Movie', secondary=movie_actor_relationship_table,
                            backref='movies_list', lazy=True)

    def __repr__(self):
        return f'<Actor {self.id} name: {self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender
    }
