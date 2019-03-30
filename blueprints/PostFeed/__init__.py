import random, logging
import random, logging
from blueprints import db
from flask_restful import fields
import datetime

from blueprints.users import *

class Feeds(db.Model):

    __tablename__ = "feed"

    id_feed = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_user = db.Column(db.Integer)
    content = db.Column(db.String(3000))
    tag = db.Column(db.String(255))
    attached_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    response_field = {
        'id_feed' : fields.Integer,
        'id_user' : fields.Integer,
        'content' : fields.String,
        'tag' : fields.String,
        'attached_image' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__ (self, id_feed, id_user, content, tag, attached_image, created_at, updated_at):
        self.id_feed = id_feed
        self.id_user = id_user
        self.content = content
        self.tag = tag
        self.attached_image = attached_image
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<Feed %r>' % self.id_feed