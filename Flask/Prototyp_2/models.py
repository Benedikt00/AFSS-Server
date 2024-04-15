from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import Column, BigInteger, ForeignKey, Integer, String

from extensions import db

class Article(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    article_name = db.Column(db.String(50))
    article_description = db.Column(db.Text)
    category = db.Column(db.String(20))
    groupes = db.Column(db.String(50))
    weight = db.Column(db.Integer)
    picture = db.Column(db.String(100))

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    max_cont = db.Column(db.Integer)
    allocated_cont = db.Column(db.Integer)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Integer, db.ForeignKey('area.id'))
    category = db.Column(db.String(20))
    occupation_status = db.Column(db.Boolean, nullable=False)
    size = db.Column(db.String(10))
    position = db.Column(db.JSON) #xyz
    area_rel = db.relationship('Area', backref=db.backref('area', lazy=True))

class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stocks = db.Column(db.JSON)
    barcode = db.Column(BIGINT(unsigned=True))
    current_location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    target_location = db.Column(db.Integer, db.ForeignKey('location.id'))
    size = db.Column(db.String(10))
    current_location_rel = db.relationship('Location', foreign_keys=[current_location], backref=db.backref('current_containers', lazy=True))
    target_location_rel = db.relationship('Location', foreign_keys=[target_location], backref=db.backref('target_containers', lazy=True))

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container = db.Column(db.Integer, db.ForeignKey('container.id'))
    article = db.Column(db.Integer, db.ForeignKey('article.id'))
    quantity = db.Column(db.Integer)
    container_rel = db.relationship('Container', backref=db.backref('stock', lazy=True))
    article_rel = db.relationship('Article', backref=db.backref('stock', lazy=True))

class Categories(db.Model):
    title = db.Column(db.String(50), primary_key=True)
    unit = db.Column(db.String(10))
    prefixes = db.Column(db.JSON)
    

class PrimaryGroup(db.Model):
    __tablename__ = 'primary_groupes'
    title = db.Column(db.String(50), primary_key=True)

class SecondaryGroup(db.Model):
    __tablename__ = 'seondary_groupes'
    prim_title = db.Column(db.String(50), db.ForeignKey('primary_groupes.title'), primary_key=True)
    title = db.Column(db.String(50), primary_key=True)

    primary_group = db.relationship('PrimaryGroup', backref='secondary_groups')