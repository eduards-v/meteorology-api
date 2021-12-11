
class SensorsService(object):
    def __init__(self):
        pass

    def get_all(self):
        pass

    def get_by_id(self, sens_id):
        pass

    def add_new(self, **kwargs):
        print("Sensors Service: %s" % kwargs)

    def delete_by_id(self, sens_id):
        pass

    def record_data(self, sens_id, **kwargs):
        print("Sensors Service: sens_id: %i data: %s" % (sens_id, kwargs))
