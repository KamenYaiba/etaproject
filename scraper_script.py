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
        user_id = r.user_id
        time_frame = r.time_frame
        time_zone = r.offset_to_gmt

        route_average = 0 #get the average from the DB for the hour gmt_hour (defined above)
        data_count = 0 #how many data points were used to calculate the average in the DB

        if data_count == 0:
            new_average = eta_mins
        else:
            new_average = (data_count * route_average + eta_mins) / (data_count + 1)

        #send the new_average to the DB, and update data_count
        new_average
        data_count + 1


