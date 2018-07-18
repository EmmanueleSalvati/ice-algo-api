
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


# def make_url(dskey, zipcode, the_date):
def make_url(dskey, lat, lgtd, the_date):
    """Create url for DarkSKY based on lat, long

    Args:
        dskey (STR): api key
        lat (STR): latitude
        lgtd (STR): longitude
        the_date (DATETIME.DATE): date
    Returns:
        STR: url for the api call
    """

    latlong = str(lat) + "," + str(lgtd)  # get_lat_long(zipcode)
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

    *** NOT NEEDED, JUST FOR TESTING ***

    Args:
        response (TYPE): Description

    Returns:
        TYPE: Description
    """
    time = response['daily']['data'][0]['temperatureMaxTime']
    timezone = tz.gettz(response['timezone'])

    return datetime.datetime.fromtimestamp(time, timezone)


def call_api(lat, lgtd, the_date):
    """Call Dark SKY api

    ***THIS IS JUST A TEMPLATE. NOT USING IT.***

    Args:
        lat (STR): Latitude
        lgtd (STR): Longitude
        the_date (DATETIME.DATE): Description

    Returns:
        TYPE: Description
    """

    print(dskey)
    url = make_url(dskey, lat, lgtd, the_date)
    g = get(url).json()

    return g


# def create_api_queries(dep_zip, dest_zip, dep_date):
def create_api_queries(dep_lat, dep_long, dest_lat, dest_long, dep_date):
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
    # q1 = make_url(dskey, dep_zip, dep_date)
    # q2 = make_url(dskey, dep_zip, dest_date)
    # q3 = make_url(dskey, dest_zip, dep_date)
    # q4 = make_url(dskey, dest_zip, dest_date)
    q1 = make_url(dskey, dep_lat, dep_long, dep_date)
    q2 = make_url(dskey, dep_lat, dep_long, dest_date)
    q3 = make_url(dskey, dest_lat, dest_long, dep_date)
    q4 = make_url(dskey, dest_lat, dest_long, dest_date)

    return (q1, q2, q3, q4)


# def get_weather(dep_zip, dest_zip, dep_date):
def get_weather(dep_lat, dep_long, dest_lat, dest_long, dep_date):
    """Summary

    Args:
        dep_lat (STR): Departure latitude
        dep_long (STR): Departure longitude
        dest_lat (STR): Destination latitude
        dest_long (STR): Destination longitude
        dep_date (DATETIME.DATE): Departure date
    """

    # queries = create_api_queries(dep_zip, dest_zip, dep_date)
    queries = \
        create_api_queries(dep_lat, dep_long, dest_lat, dest_long, dep_date)
    weathers = tuple([get(url).json() for url in queries])
    local_temps = [get_max_T(response) for response in weathers]

    return max(local_temps)


def test_get_weather():
    dep_lat = "33.9657994"  # "90003"
    dep_long = "33.9657994"
    dest_lat = "40.698677200000006"  # "11201"
    dest_long = "-73.98594140000002"
    dep_date = date.today()

    # t = get_weather(dep_zip, dest_zip, dep_date)
    t = get_weather(dep_lat, dep_long, dest_lat, dest_long, dep_date)
    return t


def test_api():
    # zipcode = "11201"
    the_date = date.today()

    lat = "40.698677200000006"
    lgtd = "-73.98594140000002"

    url = make_url(dskey, lat, lgtd, the_date)
    g = get(url).json()
    timezone = tz.gettz(g['timezone'])

    for hour in g['hourly']['data']:
        print(datetime.datetime.fromtimestamp(hour['time'], timezone), hour['temperature'])

    print(get_time_at_max_T(g))
    print(get_max_T(g))
