from sqlalchemy import Column, String, create_engine
from sqlalchemy.sql.sqltypes import Integer
from flask_sqlalchemy import SQLAlchemy
import json
import os
database_path = "postgresql://mnoquxqfufqqav:2c91509ac75cddf7dd5c4d4e1706cfb2736701c96d80b1ee9870ae2f529202cd@ec2-52-206-193-199.compute-1.amazonaws.com:5432/d3feue6vgsu064"

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


'''
Movie
has title and release year
'''
class Movie(db.Model):  
  __tablename__ = 'movie'

  id = Column(db.Integer, primary_key=True)
  title = Column(db.String)
  release_date = Column(db.Date)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}
  
  def insert(self):
    db.session.add(self)
    db.session.commit()

'''
Actor
has name, age, gender
'''
class Actor(db.Model):  
  __tablename__ = 'actor'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String)
  age = Column(db.Integer)
  gender = Column(db.String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age, 
      'gender': self.gender}

  def insert(self):
    db.session.add(self)
    db.session.commit()
