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
    def get(self, id_feed):
        qry = FeedLike.query.all()
        # qry = qry.filter(FeedLike.id_feed == id_feed)

        # rows = []
        # for row in qry:
            # print(row)
        feeds = marshal(qry, FeedLike.response_field)
        # rows.append(feeds)
        feed = {}
        feed['like'] = feeds
        feed['total'] = len(feeds)
        if feeds is not None:
            return feed, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'test': marshal(FeedLike.query, FeedLike.response_field)}, 500, {'Content_type' : 'application/json'}
   
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
    def put(self, id_feed):
        qry = FeedLike.query.get(id_feed)
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

    # # @jwt_required
    # def delete(self, id_feed):
    #     qry = Feeds.query.get(id_feed)

    #     db.session.delete(qry)
    #     db.session.commit()

    #     if qry is not None:
    #         return 'Deleted', 200, {'Content_type' : 'application/json'}
    #     else:
    #         return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    # def options(self, id_feed = None):
    #     return {}, 200

api.add_resource(FeedLikeResource, '', '/<int:id_feed>')