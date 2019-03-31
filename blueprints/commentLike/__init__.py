import random, logging
import random, logging
from blueprints import db
from flask_restful import fields
import datetime

from blueprints.users import *

class CommentsLike(db.Model):

    __tablename__ = "commentsLike"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_comment = db.Column(db.Integer)
    liked_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    response_field = {
        'id' : fields.Integer,
        'id_comment' : fields.Integer,
        'liked_by' : fields.Integer,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__ (self, id, id_comment, liked_by, created_at, updated_at):
        self.id = id
        self.id_comment = id_comment
        self.liked_by = liked_by
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<CommentsLike %r>' % self.id