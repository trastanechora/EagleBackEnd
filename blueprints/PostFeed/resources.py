import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from blueprints.users import *

from . import *
from blueprints.users import *

bp_feed = Blueprint('feed', __name__)
api = Api(bp_feed)

class FeedResource(Resource):

    def __init__(self):
        pass

    def get(self, id_feed = None):
        if id_feed == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('id_user', location = 'args')
            parser.add_argument('tag', location = 'args')
            args = parser.parse_args()

            offsets = (args['p'] * args['rp']) - args['rp']
            qry = Feeds.query

            # biar bisa kasih filter di params
            if args['id_user'] is not None:
                qry = qry.filter(Feeds.id_user.like("%"+args['id_user']+"%"))
            if args['tag'] is not None:
                qry = qry.filter(Feeds.tag.like("%"+args['tag']+"%"))

            # if args['id_user'] is not None:
            #     qry = qry.filter_by(args['id_user'])
            # if args['tag'] is not None:
            #     qry = qry.filter_by(args['tag'])

            rows = []
            for row in qry.limit(args['rp']).offset(offsets).all():
                feeds = marshal(row, Feeds.response_field)
                users = Users.query.get(row.id_user)
                feeds['user'] = marshal(users, Users.response_field)
                rows.append(feeds)
            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Feeds.query.get(id_feed)
            feeds = marshal(qry, Feeds.response_field)
            users = Users.query.get(qry.id_user)
            feeds['user'] = marshal(users, Users.response_field)
            if qry is not None:
                return feeds, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND'}, 404, {'Content_type' : 'application/json'}
   
    @jwt_required
    def post(self):
        jwtClaims = get_jwt_claims() ##  buat kalo butuh data klaim
        parser = reqparse.RequestParser()
        parser.add_argument('content', location = 'json', required=True)
        parser.add_argument('tag', location = 'json')
        parser.add_argument('image', location = 'json')
        args = parser.parse_args()

        id_user = jwtClaims['id']
        # id_user = 1
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        feeds = Feeds(None, id_user, args['content'], args['tag'], args['image'], created_at, updated_at)
        db.session.add(feeds)
        db.session.commit()

        feed = marshal(feeds, Feeds.response_field)
        users = Users.query.get(id_user)
        feed['user'] = marshal(users, Users.response_field)
        
        return feed, 200, {'Content_type' : 'application/json'}
    
    @jwt_required
    def put(self, id_feed):
        qry = Feeds.query.get(id_feed)
        parser = reqparse.RequestParser()
        parser.add_argument('content', location = 'json')
        parser.add_argument('tag', location = 'json')
        parser.add_argument('image', location = 'json')
        args = parser.parse_args()
        
        if args['content'] is not None:
            qry.content = args['content']
        if args['tag'] is not None:
            qry.tag = args['tag']
        if args['image'] is not None:
            qry.attached_image = args['image']
            
        qry.updated_at = datetime.datetime.now()

        db.session.commit()

        feeds = marshal(qry, Feeds.response_field)
        users = Users.query.get(qry.id_user)
        feeds['user'] = marshal(users, Users.response_field)

        if qry is not None:
            return feeds, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self, id_feed):
        qry = Feeds.query.get(id_feed)

        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self, id_feed = None):
        return {}, 200

api.add_resource(FeedResource, '', '/<int:id_feed>')