from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_restful import fields, marshal_with

from dateutil import parser
from datetime import date

app = Flask(__name__)
api = Api(app)

# This is temporary, will be replaced by db
ICE = {
    4.5: {
        100: 8,
        80: 8,
        70: 4
    },
    8.5: {
        100: 4,
        80: 4,
        70: 4
    },
    14: {
        100: 4,
        80: 4,
        70: 4
    }
}


class Shipment(object):

    """Encode a shipment, with the following:

    shipment number
    departure zip code
    destination zip code
    departure date/time
    arrival date/time
    hours of travel
    temperature
    food weight
    ice weight
    box size
    liner type

    Following class methods:
    * query_weather_api
    * calculate max temp
    * query ice weight
    """

    def calc_max_T(self):
        if self.dep_zip and self.dest_zip:
            T = 80
        else:
            T = 80
        self.T = T

    def ice_weight(self):
        food = self.f_weight
        T = self.T
        self.ice = ICE[food][T]

    def parse_date(self, datestr):
        if datestr is None:
            return date.today()
        else:
            return parser.parse(datestr).date()


    def __init__(self, ship_n=None, dep_zip=None, dest_zip=None, dep_date=None, f_weight=None):
        self.ship_n = ship_n
        self.dep_zip = dep_zip
        self.dest_zip = dest_zip
        self.dep_date = self.parse_date(dep_date)
        self.f_weight = f_weight
        self.calc_max_T()
        self.ice_weight()

resource_fields = {
    'ship_n': fields.String,
    'dep_zip': fields.Integer,
    'dest_zip': fields.Integer,
    'dep_date': fields.String,
    'f_weight': fields.Float,
    'T': fields.Float,
    'ice': fields.Integer
}

PARSER = reqparse.RequestParser()
PARSER.add_argument('ship_n', type=str)
PARSER.add_argument('dep_zip', type=int)
PARSER.add_argument('dest_zip', type=int)
PARSER.add_argument('dep_date', type=str)
PARSER.add_argument('f_weight', type=float)


class Ship(Resource):

    """Shows a shipment, including ice weight.
    The object is an instance of the class Shipment

    Following class methods:
    * get
    """

    @marshal_with(resource_fields)
    def post(self):
        """POST method. For a given shipment, returns
        an ice weight.

        Args:

        Returns:
            TYPE: Same json as input, with an extra key: ice, in pounds
        """

        ARGS = PARSER.parse_args()
        # print("Passing these:",
        #     ARGS.ship_n, ARGS.dep_zip, ARGS.dest_zip,
        #     ARGS.dep_date, ARGS.f_weight)

        s = Shipment(ARGS.ship_n,
            ARGS.dep_zip,
            ARGS.dest_zip,
            ARGS.dep_date,
            ARGS.f_weight)

        return s


api.add_resource(Ship, '/')

if __name__ == '__main__':
    app.run(debug=True)