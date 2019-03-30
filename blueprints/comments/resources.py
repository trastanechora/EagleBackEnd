import json
from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint, Flask
from . import *
from blueprints import db
from datetime import date, datetime
from blueprints.users import *
from blueprints.PostFeed import *

from flask_jwt_extended import jwt_required, get_jwt_claims

bp_comments = Blueprint('comments', __name__)
api = Api(bp_comments)

class CommentsResources(Resource):

    # @jwt_required
    def get(self, id = None):
        if id == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('id_feed', location = 'args')
            parser.add_argument('id_user', location = 'args')
            args = parser.parse_args()

            offsets = (args['p'] * args['rp']) - args['rp']
            qry = Comments.query

            if args['id_feed'] is not None:
                qry = qry.filter(Comments.id_feed.like("%"+args['id_feed']+"%"))
            if args['id_user'] is not None:
                qry = qry.filter(Comments.id_user.like("%"+args['id_user']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offsets).all():
                comments = marshal(row, Comments.response_field)
                qry_user = Users.query.get(row.id_user)
                comments['user'] = marshal(qry_user, Users.response_field)
                rows.append(comments)
            return rows, 200, {'Content_type' : 'application/json'}

        else:
            qry = Comments.query.get(id)
            comments = marshal(qry, Comments.response_field)
            qry_feed = Feeds.query.get(qry.id_feed)
            comments['feed'] = marshal(qry_feed, Feeds.response_field)
            qry_user = Users.query.get(qry.id_user)
            comments['user'] = marshal(qry_user, Users.response_field)
            if qry is not None:
                return comments, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND'}, 404, {'Content_type' : 'application/json'}
   
    @jwt_required
    def post(self):
        jwtClaims = get_jwt_claims() ##  buat kalo butuh data klaim
        parser = reqparse.RequestParser()
        parser.add_argument('id_feed', location='json')
        parser.add_argument('content', location = 'json')
        parser.add_argument('image', location = 'json')
        args = parser.parse_args()

        id_user = jwtClaims['id']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        comments = Comments(None, args['id_feed'], id_user, args['content'], args['image'], created_at, updated_at)
        db.session.add(comments)
        db.session.commit()

        comment = marshal(comments, Comments.response_field)
        qry_user = Users.query.get(id_user)
        comment['user'] = marshal(qry_user, Users.response_field)
        
        return comment, 200, {'Content_type' : 'application/json'}
    
    # @jwt_required
    def put(self, id):
        qry = Comments.query.get(id)
        parser = reqparse.RequestParser()
        parser.add_argument('content', location = 'json')
        parser.add_argument('image', location = 'json')
        args = parser.parse_args()
        
        if args['content'] is not None:
            qry.content = args['content']
        if args['image'] is not None:
            qry.attached_image = args['image']
            
        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, Comments.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    # @jwt_required
    def delete(self, id):
        qry = Comments.query.get(id)

        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self, id = None):
        return {}, 200

api.add_resource(CommentsResources, '', '/<int:id>')
