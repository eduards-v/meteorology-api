from marshmallow import Schema, fields, post_load, pre_dump
import simplejson as json

from utils.json_encoders import DatetimeEncoder


class SensorModelSchema(Schema):
    sens_id = fields.Int(required=True)
    metadata = fields.Dict()
    data = fields.List(fields.Dict())

    uri = fields.Url()

    @post_load
    def create_sensor(self, model_params, **kwargs):
        return SensorModel(**model_params)

    @pre_dump
    def serialize_data(self, model, **kwargs):
        # marshmallow can't serialize Decimal object. Using simplejson instead.
        if model.data:
            serialized_data = json.dumps(model.data, cls=DatetimeEncoder)
            model.data = eval(serialized_data)
        return model


class SensorModel(object):
    def __init__(self, sens_id, metadata=None, data=None):
        self._sens_id = sens_id
        self._metadata = metadata or {}
        self._data = data or []

    @property
    def sens_id(self):
        return self._sens_id

    @property
    def metadata(self):
        return self._metadata

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, set_data):
        self._data = set_data

    def __str__(self):
        return "Sensor: {id}; Metadata: {meta};".format(id=self.sens_id,
                                                        meta=self.metadata)
