
from requests import get
from uszipcode import ZipcodeSearchEngine
from datetime import date
import datetime
from dateutil import tz
from dateutil.relativedelta import relativedelta

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
        dskey (STR): api key
        zipcode (STR): zip code
        the_date (DATETIME.DATE): date
    Returns:
        STR: url for the api call
    """

    latlong = get_lat_long(zipcode)
    unixtime = date_to_unix(the_date)
    w = 'https://api.darksky.net/forecast/' + \
        str(dskey) + '/' +\
        str(latlong) + "," +\
        str(unixtime)
    return w


def get_max_T(response):
    """Return the maximum temperature from the api

    Args:
        response (TYPE): Description

    Returns:
        TYPE: Description
    """
    return response['daily']['data'][0]['temperatureMax']


def get_time_at_max_T(response):
    """Get the time for the max Temperature.
    Not really needed, just for testing

    Args:
        response (TYPE): Description

    Returns:
        TYPE: Description
    """
    time = response['daily']['data'][0]['temperatureMaxTime']
    timezone = tz.gettz(response['timezone'])

    return datetime.datetime.fromtimestamp(time, timezone)


def call_api(zipcode, the_date):
    """Call Dark SKY api

    Args:
        zipcode (STR): Description
        the_date (DATETIME.DATE): Description

    Returns:
        TYPE: Description
    """

    url = make_url(dskey, zipcode, the_date)
    g = get(url).json()

    return g


def create_api_queries(dep_zip, dest_zip, dep_date):
    """Create four queries:
    departure location + departure date
    departure location + estimated arrival date (1 day after departure)
    destination location + departure date
    destination location + estimated arrival date (1 day after departure)

    Args:
        dep_zip (STR): Description
        dest_zip (STR): Description
        dep_date (DATETIME.DATE): Description
    """

    dest_date = dep_date + relativedelta(days=1)
    q1 = make_url(dskey, dep_zip, dep_date)
    q2 = make_url(dskey, dep_zip, dest_date)
    q3 = make_url(dskey, dest_zip, dep_date)
    q4 = make_url(dskey, dest_zip, dest_date)

    return (q1, q2, q3, q4)


def get_weather(dep_zip, dest_zip, dep_date):
    """Summary

    Args:
        dep_zip (TYPE): Description
        dest_zip (TYPE): Description
        dep_date (TYPE): Description
    """
    pass


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
