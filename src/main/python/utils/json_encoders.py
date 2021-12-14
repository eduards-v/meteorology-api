from datetime import datetime, date
import simplejson as json


class DatetimeEncoder(json.JSONEncoder):
    """ Customer JSON encoder extension to convert date and datetime object to string
    """
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
