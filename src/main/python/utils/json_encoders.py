from datetime import datetime
import simplejson as json


class DateEncoder(json.JSONEncoder):
    """ Customer JSON encoder extension to convert datetime object to string
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
