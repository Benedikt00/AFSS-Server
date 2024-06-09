from flask_login import UserMixin

from extensions import db


class Parts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Bauteilname = db.Column(db.String(30), nullable=False)
    Kategorisierungen = db.Column(db.JSON, nullable=False)
    Platz = db.Column(db.String(10), nullable=False)
    Bauteilanzahl = db.Column(db.Integer)
    Bauteilanzahl_min = db.Column(db.Integer)
    Gewicht_pro_teil_in_g = db.Column(db.Integer)
    eingelagert = db.Column(db.Integer, default=0)
    ausgelagert = db.Column(db.Integer, default=1)
    wird_eingelagert = db.Column(db.Integer, default=0)
    wird_ausgelagert = db.Column(db.Integer, default=0)
    anzahl_auslagerungen = db.Column(db.Integer, nullable=False, default=0)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(100), nullable=False)
    access = db.Column(db.Integer, nullable=False)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sort = db.Column(db.Integer)
    part_id = db.Column(db.Integer, db.ForeignKey("parts.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
