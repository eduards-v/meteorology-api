from repo.sensors_repo import SensorsRepo


class SensorsService(object):
    def __init__(self):
        self.repo = SensorsRepo()

    def get_all(self):
        return self.repo.fetch_all()

    def get_by_id(self, sens_id):
        sensor = self.repo.fetch_by_id(sens_id)
        return sensor

    def add_new(self, sensor):
        self.repo.add_new(sensor)

    def delete_by_id(self, sens_id):
        return self.repo.delete_by_id(sens_id)

    def record_data(self, sensor):
        self.repo.record_sensor_data(sensor)
