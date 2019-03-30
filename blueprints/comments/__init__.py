from blueprints import db
from flask_restful import fields
import datetime

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_feed = db.Column(db.Integer)
    id_user = db.Column(db.Integer)
    content = db.Column(db.String(3000))
    attached_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    response_field = {
        "id" : fields.Integer,
        "id_feed" : fields.Integer,
        "id_user" : fields.Integer,
        "content" : fields.String,
        "attached_image" : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, id, id_feed, id_user, content, attached_image, created_at, updated_at):
        self.id = id
        self.id_feed = id_feed
        self.id_user = id_user
        self.content = content
        self.attached_image = attached_image
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f'<Comments {self.id}>'

db.create_all()