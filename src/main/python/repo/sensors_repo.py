SENSORS = {
    1: {"data": [{"temp": 7.6, "hum": 22, "recorded": "2021-12-10 14:52:25.536249"},
                 {"temp": 8.2, "hum": 21, "recorded": "2021-12-10 13:52:25.536249"}],
        "metadata": {"country": "Ireland", "city": "Galway"}},
    2: {"data": [],
        "metadata": {"country": "Ireland", "city": "Dublin"}},
}


class SensorsRepo(object):
    def __init__(self):
        pass

    def fetch_all(self):
        return SENSORS

    def fetch_by_id(self, sens_id):
        try:
            sensor = SENSORS[sens_id]
        except KeyError:
            return
        return {"sensor %i" % sens_id: sensor}

    def delete_by_id(self, sens_id):
        del SENSORS[sens_id]

    def add_new(self, **kwargs):
        SENSORS[kwargs["sens_id"]] = {"metadata": kwargs["metadata"], "data": []}

    def record_sensor_data(self, sens_id, **kwargs):
        SENSORS[sens_id]["data"].append(kwargs["data"])
