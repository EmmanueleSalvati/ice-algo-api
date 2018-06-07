
from requests import get
from uszipcode import ZipcodeSearchEngine
from datetime import date
import datetime
from dateutil import tz

# Dark SKY key
with open("dark-sky-key.txt", "r") as k:
    dskey = k.read().split()[-1]


def get_lat_long(zipcode):
    """Retrieve Latitude and Longitude from the zip code
    (US only).

    Needed to query Dark Sky API

    Args:
        zipcode (INT): five-digits zip code

    Returns:
        STR: "Lat,Long"
    """
    search = ZipcodeSearchEngine()
    zipcode = search.by_zipcode(str(zipcode))

    return str(zipcode.Latitude) + "," + str(zipcode.Longitude)


def date_to_unix(the_date):
    """convert a datetime.date object into UNIX timestamp

    Args:
        the_date (DATETIME.DATE): The date to convert
    """
    return the_date.strftime("%s")


def make_url(dskey, zipcode, the_date):
    """Create url for DarkSKY based on zipcode

    Args:
        dskey (TYPE): Description
        zipcode (TYPE): Description

    Returns:
        TYPE: Description
    """
    latlong = get_lat_long(zipcode)
    unixtime = date_to_unix(the_date)
    w = 'https://api.darksky.net/forecast/' + \
        str(dskey) + '/' +\
        str(latlong) + "," +\
        str(unixtime)
    return w


def get_max_T(response):
    return response['daily']['data'][0]['temperatureMax']


def get_time_at_max_T(response):
    time = response['daily']['data'][0]['temperatureMaxTime']
    timezone = tz.gettz(response['timezone'])

    return datetime.datetime.fromtimestamp(time, timezone)


def test_api():
    zipcode = "11201"
    the_date = date.today()

    url = make_url(dskey, zipcode, the_date)
    g = get(url).json()
    # print(g)
    timezone = tz.gettz(g['timezone'])

    for hour in g['hourly']['data']:
        print(datetime.datetime.fromtimestamp(hour['time'], timezone), hour['temperature'])

    print(get_time_at_max_T(g))
    print(get_max_T(g))
