"""
Python3 needed.
Make sure you install the libraries listed in requirements.txt:
```pip3 install -r requirements.txt```

Then simply run ```python3 ice_algo_api.py``` to run the api

Look at ```query_ice_algo_api.py``` for an example usage:
```python3 query_ice_algo_api.py```
"""

from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from darksky import get_weather

from dateutil import parser
from datetime import date

import numpy as np
from scipy import interpolate

app = Flask(__name__)
api = Api(app)

# This is the result of the heat chamber. See below for nterpolated values.
# This dictionary is not actually used.
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

# Old 1D Interpolation
# x = [70, 80, 100]
# xnew = np.arange(70, 100, 0.1)

# y4 = [4, 8, 8]
# f4 = interpolate.interp1d(x, y4)
# y8 = [4, 4, 4]
# f8 = interpolate.interp1d(x, y8)
# y14 = [4, 4, 4]
# f14 = interpolate.interp1d(x, y14)

# ynew4 = f4(xnew)   # use interpolation function returned by `interp1d`
# ynew8 = f8(xnew)
# ynew14 = f14(xnew)

# 2D interpolation
weights = [3.5, 4.55, 8.54, 14.35, 19.25]
temps = [0, 50, 70, 80, 100, 200]

ice = [[0, 2, 4, 8, 8, 8],  # 3.5
       [0, 2, 4, 8, 8, 8],  # 4.55
       [0, 0, 4, 4, 4, 4],  # 8.54
       [0, 0, 4, 4, 4, 4],  # 14.35
       [0, 0, 4, 4, 4, 4]]  # 19.25

interp_ice = interpolate.interp2d(temps, weights, ice)


def find_closest_even_int(num):
    """
    Return the closest even number. Used for rounding the ice weight
    to multiples of 2 lbs
    """

    floor = np.floor(num)
    ceil = np.ceil(num)

    if floor % 2 == 0:
        return floor
    else:
        return ceil


# INTERP_ICE = {
#     4.5: {np.round(x, 1): find_closest_even_int(y) for (x, y) in zip(xnew, ynew4)},
#     8.5: {np.round(x, 1): find_closest_even_int(y) for (x, y) in zip(xnew, ynew8)},
#     14: {np.round(x, 1): find_closest_even_int(y) for (x, y) in zip(xnew, ynew14)}
# }


class Shipment(object):

    """Encode a shipment, with the following:

    shipment number
    departure zip code
    destination zip code
    departure date/time
    arrival date/time
    temperature
    food weight
    ice weight

    Following class methods:
    * query_weather_api
    * calculate max temp
    * query ice weight
    """

    def query_weather_api(self):
        """
        Set the maximum T, by querying the weather api with the following
        parameters:
        departure zip code
        destination zip code
        departure date
        """

        try:
            T = get_weather(self.dep_zip, self.dest_zip, self.dep_date)
            self.T = np.round(T, 1)
        except NameError:
            print("ALERT, WEATHER API DID NOT WORK! SETTING DEFAULT TO 80")
            self.T = 80

    def ice_weight(self):
        """Summary
        Calculate ice weight from the 2D interpolation
        """

        food = self.f_weight
        T = self.T
        self.ice = find_closest_even_int(interp_ice(T, food))
        # self.ice = INTERP_ICE[food][T]  # Old 1D interpolation

    def parse_date(self, datestr):
        if datestr is None:
            return date.today()
        else:
            return parser.parse(datestr).date()

    def __init__(self,
                 ship_n=None, dep_zip=None, dest_zip=None,
                 dep_date=None, f_weight=None):
        self.ship_n = ship_n
        self.dep_zip = dep_zip
        self.dest_zip = dest_zip
        self.dep_date = self.parse_date(dep_date)
        self.f_weight = f_weight
        self.query_weather_api()
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
    * post
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

        s = Shipment(ARGS.ship_n,
                     ARGS.dep_zip,
                     ARGS.dest_zip,
                     ARGS.dep_date,
                     ARGS.f_weight)

        return s


api.add_resource(Ship, '/')

if __name__ == '__main__':
    app.run(debug=True)
