from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey

import json
import os
os.environ['DATABASE_URL'] = 'postgres://wcpfrltkueqkqp:5c1ba825b1d9289949ea09b640559ad1e839b39b49163c3611a5f5dc9dc517f7@ec2-54-156-121-142.compute-1.amazonaws.com:5432/dbfnqbr0tidg57'
database_path = os.environ['DATABASE_URL']

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
Movies
Have title and release year
'''
class Movies(db.Model):
  __tablename__ = 'movies'
  
  id = Column(Integer(), primary_key=True)
  title = Column(String(80))
  release_year = Column(Integer())

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_year': self.release_year}
  '''
  insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()
  '''
  delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  '''
  update()
  '''
  def update(self):
    db.session.commit()

  def __repr__(self):
    return json.dumps(self.format())


'''
Actors 
Have name, age and gender
'''
class Actors(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer(), primary_key=True)
  name = Column(String(80))
  age = Column(Integer())
  gender = Column(Integer())

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender}
  '''
  insert()
  '''
  def insert(self):
    db.session.add(self)
    db.session.commit()
  '''
  delete()
  '''
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  '''
  update()
  '''
  def update(self):
    db.session.commit()
  def __repr__(self):
    return json.dumps(self.format())
