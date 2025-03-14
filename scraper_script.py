from datetime import datetime
import pytz
import json
from route import Route
from ETA import get_eta
from helping_functions import eta_to_mins


def scrape():
    gmt_hour = datetime.now(pytz.timezone('GMT')).hour

    with open(f"jobs{gmt_hour}.json", "r") as f:
        routes = [Route.from_dict(route) for route in json.load(f)]

    for r in routes:
        url = r.url
        eta = get_eta(url)
        eta_mins = eta_to_mins(eta)


        #user and route data for the DB
        route_id = r.route_id

        #<<<<<<<<<<<<<<<SEND TO DB>>>>>>>>>>>>>>>>


