import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime

from . import *

bp_feedLike = Blueprint('feedLike', __name__)
api = Api(bp_feedLike)

class FeedLikeResource(Resource):

    def __init__(self):
        pass

    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_feed', type = int, location = 'args')
        args = parser.parse_args()
        # jwtClaims = get_jwt_claims()

        # id_member = jwtClaims['id_member']

        qry = FeedLike.query.filter_by(id_feed = args['id_feed']).all()
        feeds = marshal(qry, FeedLike.response_field)

        if qry is not None:
            return feeds, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}
   
    # @jwt_required
    def post(self):
        # jwtClaims = get_jwt_claims() ##  buat kalo butuh data klaim
        parser = reqparse.RequestParser()
        parser.add_argument('id_feed', location = 'json')
        parser.add_argument('liked_by', location = 'json')
        args = parser.parse_args()

        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        feeds = FeedLike(None, args['id_feed'], args['liked_by'], created_at, updated_at)
        db.session.add(feeds)
        db.session.commit()

        feed = marshal(feeds, FeedLike.response_field)
        
        return feed, 200, {'Content_type' : 'application/json'}
    
    # @jwt_required
    def put(self, id_like):
        qry = FeedLike.query.get(id_like)
        parser = reqparse.RequestParser()
        parser.add_argument('id_feed', location = 'json')
        parser.add_argument('liked_by', location = 'json')
        args = parser.parse_args()
        
        if args['id_feed'] is not None:
            qry.id_feed = args['id_feed']
        if args['liked_by'] is not None:
            qry.liked_by = args['liked_by']
            
        qry.updated_at = datetime.datetime.now()

        db.session.commit()
        if qry is not None:
            return marshal(qry, FeedLike.response_field), 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    # @jwt_required
    def delete(self, id_like):
        qry = FeedLike.query.get(id_like)

        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self, id_like = None):
        return {}, 200

api.add_resource(FeedLikeResource, '', '/<int:id_like>')