import random, logging
import random, logging
from blueprints import db
from flask_restful import fields
import datetime

from blueprints.users import *

class Farms(db.Model):

    __tablename__ = "farm"

    id_farm = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_user = db.Column(db.Integer)
    deskripsi = db.Column(db.String(2000))
    plant_type = db.Column(db.String(100))
    planted_at = db.Column(db.DateTime)
    ready_at = db.Column(db.DateTime)
    address = db.Column(db.String(500))
    city = db.Column(db.String(225))
    photos = db.Column(db.String(255))
    farm_size = (db.Column(db.Integer))
    coordinates = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    response_field = {
        'id_farm' : fields.Integer,
        'id_user' : fields.Integer,
        'deskripsi' : fields.String,
        'plant_type' : fields.String,
        'planted_at' : fields.DateTime,
        'ready_at' : fields.DateTime,
        'address' : fields.String,
        'city' : fields.String,
        'photos' : fields.String,
        'farm_size' : fields.Integer,
        'coordinates' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__ (self, id_farm, id_user, deskripsi, plant_type, planted_at, ready_at, address, city, photos, farm_size, coordinates, created_at, updated_at):
        self.id_farm = id_farm
        self.id_user = id_user
        self.deskripsi = deskripsi
        self.plant_type = plant_type
        self.planted_at = planted_at
        self.ready_at = ready_at
        self.address = address
        self.city = city
        self.photos = photos
        self.farm_size = farm_size
        self.coordinates = coordinates
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Farms %r>' % self.id_farm