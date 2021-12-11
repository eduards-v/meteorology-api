from marshmallow import Schema, fields, post_load


class SensorModelSchema(Schema):
    sens_id = fields.Int(required=True)
    metadata = fields.Dict()
    data = fields.List(fields.Dict())

    @post_load
    def create_sensor(self, data, **kwargs):
        return SensorModel(**data)


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

    def __str__(self):
        return "Sensor: {id}; Metadata: {meta};".format(id=self.sens_id,
                                                        meta=self.metadata)


if __name__ == '__main__':
    dbo1 = SensorModel(1, {"country": "Ireland", "city": "Galway"},
                       data=[
                           {"temp": 7.6, "hum": 22, "recorded": "2021-12-10 14:52:25.536249"},
                           {"temp": 8.2, "hum": 21, "recorded": "2021-12-10 13:52:25.536249"}
                       ])

    post = {
        "sens_id": 3,
        "metadata":
            {
                "country": "Germany",
                "city": "Berlin"
            }
    }

    put = {
        "sens_id": 1,
        "data": [{
            "temp": 14,
            "hum": 14,
            "recorded": "2021-12-11 16:52:25.536249"
        }]
    }
    res = SensorModelSchema().dump(dbo1)
    res2 = SensorModelSchema().load(post)
    res3 = SensorModelSchema().load(put)
    print(res)
    print(repr(res2))
    print(res3.data)
