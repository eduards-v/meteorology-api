from unittest import TestCase
from datetime import datetime, date
import simplejson as json

from utils.json_encoders import DatetimeEncoder


class TestJsonEncoders(TestCase):
    def test_datetime_encoder_serialize_date(self):
        today = date.today()
        with_date = {"recorded": today}
        serialized_date = json.dumps(with_date, cls=DatetimeEncoder)

        self.assertIn(str(today), serialized_date)

    def test_datetime_encoder_serialize_datetime(self):
        datetime_now = datetime.now()
        with_date = {"recorded": datetime_now}
        serialized_date = json.dumps(with_date, cls=DatetimeEncoder)

        self.assertIn(str(datetime_now), serialized_date)

    def test_datetime_encoder_serialize_with_no_datetime(self):
        no_datatime = {"recorded": "2021-12-14 19:56:25.745767"}
        serialized_date = json.dumps(no_datatime, cls=DatetimeEncoder)
        self.assertIn("2021-12-14 19:56:25.745767", serialized_date)
