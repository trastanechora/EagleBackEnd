import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import datetime
from blueprints.users import *
from sqlalchemy import and_
import dateutil.parser

from . import *
from blueprints.users import *

bp_farm = Blueprint('farm', __name__)
api = Api(bp_farm)

class FarmResource(Resource):

    def __init__(self):
        pass

    def get(self, id_farm = None):
        if id_farm == None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 5)
            parser.add_argument('search', location = 'args')
            parser.add_argument('id_user', location = 'args')
            parser.add_argument('planted_at', location = 'args')
            parser.add_argument('ready_at', location = 'args')
            parser.add_argument('plant_type', location = 'args')
            parser.add_argument('address', location = 'args')
            parser.add_argument('city', location = 'args')
            parser.add_argument('category', location = 'args')
            args = parser.parse_args()

            offsets = (args['p'] * args['rp']) - args['rp']
            qry = Farms.query

            if args['search'] is not None:
                qry = qry.filter(Farms.plant_type.like("%"+args['search']+"%"))
                if qry.first() is None:
                    qry = Farms.query.filter(Farms.deskripsi.like("%"+args['search']+"%"))
                    if qry.first() is None:
                        qry = Farms.query.filter(Farms.city.like("%"+args['search']+"%"))
                        if qry.first() is None:
                            return {'status': 'Not Found', 'message': 'Farm is not found'}, 404, {'Content-Type': 'application/json'}

            if args['id_user'] is not None:
                qry = qry.filter(Farms.id_user.like("%"+args['id_user']+"%"))

            if args['plant_type'] is not None:
                qry = qry.filter(Farms.plant_type.like("%"+args['plant_type']+"%"))

            if args['planted_at'] is not None:
                qry = qry.filter(and_(Farms.planted_at >= args['planted_at'], Farms.planted_at < args['planted_at'] + str(datetime.timedelta(days=1))))
            
            if args['ready_at'] is not None:
                qry = qry.filter(and_(Farms.ready_at >= args['ready_at'], Farms.ready_at < args['ready_at'] + str(datetime.timedelta(days=1))))

            if args['address'] is not None:
                qry = qry.filter(Farms.address.like("%"+args['address']+"%"))
            
            if args['city'] is not None:
                qry = qry.filter(Farms.city.like("%"+args['city']+"%"))

            if args['category'] is not None:
                qry = qry.filter(Farms.category.like("%"+args['category']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offsets).all():
                farms = marshal(row, Farms.response_field)
                users = Users.query.get(row.id_user)
                farms['user'] = marshal(users, Users.response_field)
                rows.append(farms)
            return rows, 200, {'Content_type' : 'application/json'}
        else:
            qry = Farms.query.get(id_farm)
            farms = marshal(qry, Farms.response_field)
            users = Users.query.get(qry.id_user)
            farms['user'] = marshal(users, Users.response_field)
            if qry is not None:
                return farms, 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND'}, 404, {'Content_type' : 'application/json'}
   
    @jwt_required
    def post(self):
        jwtClaims = get_jwt_claims() ##  buat kalo butuh data klaim
        parser = reqparse.RequestParser()
        parser.add_argument('farm_size', type=int, location = 'json', required=True)
        parser.add_argument('coordinates', location = 'json', required=True)
        parser.add_argument('center', location = 'json', required=True)
        args = parser.parse_args()

        deskripsi = ""
        plant_type = ""
        planted_at = datetime.datetime.now()
        ready_at = datetime.datetime.now()
        address = ""
        city = ""
        photos = ""

        if args['farm_size'] > 0 and args['farm_size'] <= 250:
            category = "kecil"
        elif args['farm_size'] > 250 and args['farm_size'] <= 100:
            category = "sedang"
        elif args['farm_size'] > 1000 and args['farm_size'] <= 2000:
            category = "besar"
        elif args['farm_size'] > 2000:
            category = "sangat besar"

        id_user = jwtClaims['id']
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        farms = Farms(None, id_user, deskripsi, plant_type, planted_at, ready_at, address, city, photos, args['farm_size'], category, args['coordinates'], args['center'], created_at, updated_at)
        db.session.add(farms)
        db.session.commit()

        farm = marshal(farms, Farms.response_field)
        users = Users.query.get(id_user)
        farm['user'] = marshal(users, Users.response_field)
        
        return farm, 200, {'Content_type' : 'application/json'}
    
    @jwt_required
    def put(self, id_farm):
        qry = Farms.query.get(id_farm)
        parser = reqparse.RequestParser()
        parser.add_argument('description', location = 'json')
        parser.add_argument('plant_type', location = 'json')
        parser.add_argument('planted_at', location = 'json')
        parser.add_argument('ready_at', location='json')
        parser.add_argument('address', location = 'json')
        parser.add_argument('city', location = 'json')
        parser.add_argument('photos', location = 'json')
        parser.add_argument('farm_size', location = 'json')
        parser.add_argument('category', location = 'json')
        parser.add_argument('coordinates', location = 'json')
        parser.add_argument('center', location = 'json')
        args = parser.parse_args()
        
        if args['description'] is not None:
            qry.description = args['description']
        if args['plant_type'] is not None:
            qry.plant_type = args['plant_type']
        if args['planted_at'] is not None:
            datetime_object = dateutil.parser.parse(args['planted_at'])
            qry.planted_at = datetime_object
        if args['ready_at'] is not None:
            datetime_object = dateutil.parser.parse(args['planted_at'])
            qry.ready_at = datetime_object
        if args['address'] is not None:
            qry.address = args['address']
        if args['city'] is not None:
            qry.city = args['city']
        if args['photos'] is not None:
            qry.photos = args['photos']
        if args['farm_size'] is not None:
            qry.farm_size = args['farm_size']
        if args['category'] is not None:
            qry.category = args['category']
        if args['coordinates'] is not None:
            qry.attached_coordinates = args['coordinates']
        if args['center'] is not None:
            qry.attached_center = args['center']

        qry.updated_at = datetime.datetime.now()

        db.session.commit()

        farms = marshal(qry, Farms.response_field)
        users = Users.query.get(qry.id_user)
        farms['user'] = marshal(users, Users.response_field)

        if qry is not None:
            return farms, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def delete(self, id_farm):
        qry = Farms.query.get(id_farm)

        db.session.delete(qry)
        db.session.commit()

        if qry is not None:
            return 'Deleted', 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'NOT_FOUND', 'message' : 'ID not found'}, 404, {'Content_type' : 'application/json'}

    def options(self, id_farm = None):
        return {}, 200

api.add_resource(FarmResource, '', '/<int:id_farm>')