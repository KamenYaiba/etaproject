from helping_functions import clean_url, time_to_gmt, add_route_to_json


class Route:
    def __init__(self, route_id, user_id, url, time_frame, offset_to_gmt):
        self.route_id = route_id
        self.user_id = user_id
        self.url = clean_url(url)
        self.time_frame = time_to_gmt(time_frame, offset_to_gmt)
        self.offset_to_gmt = offset_to_gmt

        start, end = self.time_frame

        for i in range(start, end):
            add_route_to_json(i, self)

    def to_dict(self):
        return {
            "route_id": self.route_id,
            "user_id": self.user_id,
            "url": self.url,
            "time_frame": self.time_frame,
            "offset_to_gmt": self.offset_to_gmt
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            route_id=data["route_id"],
            user_id=data["user_id"],
            url=data["url"],
            time_frame=data["time_frame"],
            offset_to_gmt=data["offset_to_gmt"]
        )


