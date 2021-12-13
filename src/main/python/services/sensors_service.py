from models.sensor_model import SensorModelSchema
from repo.sensors_repo import SensorsRepo
from utils.dict_utils import nest_flat_dict


class SensorsService(object):
    def __init__(self):
        self.repo = SensorsRepo()

    def get_all(self):
        sensors = self.repo.fetch_all()
        if not sensors:
            return sensors
        # driver returns list of DictRow objects
        # convert into the model object
        sensors = [nest_flat_dict(sensor, "metadata", "city_name", "country_name") for sensor in sensors]
        return SensorModelSchema(many=True).load(sensors)

    def get_by_id(self, sens_id):
        sensor = self.repo.fetch_by_id(sens_id)
        if not sensor:
            return sensor
        # driver returns DictRow object
        # convert into the model object
        sensor = nest_flat_dict(sensor, "metadata", "city_name", "country_name")
        return SensorModelSchema().load(sensor)

    def add_new(self, sensor):
        self.repo.add_new(sensor.sens_id, sensor.metadata)

    def delete_by_id(self, sens_id):
        return self.repo.delete_by_id(sens_id)

    def record_data(self, sensor):
        self.repo.record_sensor_data(sensor.sens_id, sensor.data)

    def get_latest_data(self, sens_id):
        latest_data = self.repo.get_latest_data(sens_id)

        # process data returned by the psql drive to build a model
        latest_data = nest_flat_dict(latest_data, "data", "temperature", "humidity", "recorded")
        # Wrap data into the list as expected by the model. Assign empty list if data values are None
        latest_data["data"] = [latest_data["data"].copy()] if latest_data["data"]["temperature"] else []

        return SensorModelSchema().load(latest_data)
