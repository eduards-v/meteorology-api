from dbo.sensor_dbo import SensorModel

SENSORS = {
    1: SensorModel(sens_id=1,
                   metadata={"country": "Ireland", "city": "Galway"},
                   data=[{"temp": 7.6, "hum": 22, "recorded": "2021-12-10 14:52:25.536249"},
                       {"temp": 8.2, "hum": 21, "recorded": "2021-12-10 13:52:25.536249"}]),
    2: SensorModel(sens_id=2,
                   metadata={"country": "Ireland", "city": "Dublin"})
}


class SensorsRepo(object):
    def __init__(self):
        pass

    def fetch_all(self):
        return SENSORS.values()

    def fetch_by_id(self, sens_id):
        try:
            sensor = SENSORS[sens_id]
        except KeyError:
            return
        return sensor

    def delete_by_id(self, sens_id):
        del SENSORS[sens_id]

    def add_new(self, sensor_dbo):
        SENSORS[sensor_dbo.sens_id] = sensor_dbo

    def record_sensor_data(self, sensor):
        SENSORS[sensor.sens_id].data.append(sensor.data[0])
