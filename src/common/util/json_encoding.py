from datetime import date, datetime, time, timedelta

import pendulum
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """
        serialize a date or datetime as string to send over json
    """

    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, (datetime)):
            in_utc = pendulum.instance(o, tz="UTC").in_tz("America/Sao_Paulo")
            return in_utc.isoformat()
        elif isinstance(o, (time, date)):
            return o.isoformat()
        elif isinstance(o, (timedelta)):
            hours, minutes = convert_timedelta(o)
            hours = hours.zfill(2)
            minutes = minutes.zfill(2)
            data = "{}:{}".format(hours, minutes)
            return data
        elif isinstance(o, (bytes)):
            o = o.decode("utf-8")
            return str(o)
        return JSONEncoder.default(self, o)


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return str(hours), str(minutes)
