import random, logging
import random, logging
from blueprints import db
from flask_restful import fields
import datetime

from blueprints.users import *

class FeedLike(db.Model):

    __tablename__ = "feedLike"

    id_like = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_feed = db.Column(db.Integer)
    liked_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    response_field = {
        'id_like' : fields.Integer,
        'id_feed' : fields.Integer,
        'liked_by' : fields.Integer,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__ (self, id_like, id_feed, liked_by, created_at, updated_at):
        self.id_like = id_like
        self.id_feed = id_feed
        self.liked_by = liked_by
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<FeedLike %r>' % self.id_like