from repo.sensors_repo import SensorsRepo


class SensorsService(object):
    def __init__(self):
        self.repo = SensorsRepo()

    def get_all(self):
        return self.repo.fetch_all()

    def get_by_id(self, sens_id):
        return self.repo.fetch_by_id(sens_id)

    def add_new(self, **kwargs):
        print("Sensors Service: %s" % kwargs)
        # create dbo here from kwargs
        self.repo.add_new(**kwargs)

    def delete_by_id(self, sens_id):
        return self.repo.delete_by_id(sens_id)

    def record_data(self, sens_id, **kwargs):
        print("Sensors Service: sens_id: %i data: %s" % (sens_id, kwargs))
        # create dbo here from kwargs
        self.repo.record_sensor_data(sens_id, **kwargs)
