from flask import Flask, request
from flask_restful import Resource, Api

from services.sensors_service import SensorsService


class Sensor(Resource):
    def __init__(self):
        self.service = SensorsService()

    def get(self, sens_id):
        sensor = self.service.get_by_id(sens_id)
        if not sensor:
            return {"message": "The sensor with id %i not found" % sens_id}, 404
        return self.service.get_by_id(sens_id)

    def put(self, sens_id):
        sensor = self.service.get_by_id(sens_id)
        if not sensor:
            return {"message": "The sensor with id %i not found" % sens_id}, 404

        json_data = request.get_json(force=True)
        self.service.record_data(sens_id, **json_data)

        return {"message": "Recorded data for the sensor with id %i" % sens_id}, 201

    def delete(self, sens_id):
        sensor = self.service.get_by_id(sens_id)
        if not sensor:
            return {"message": "The sensor with id %i not found" % sens_id}, 404

        self.service.delete_by_id(sens_id)
        return {"message": "Deleted the sensor with id %i" % sens_id}, 204


class Sensors(Resource):
    def __init__(self):
        self.service = SensorsService()

    def get(self):
        return self.service.get_all()

    def post(self):
        new_sens = request.get_json(force=True)

        if self.service.get_by_id(new_sens["sens_id"]):
            return {"message": "The sensor with id %i already exists" % new_sens["sens_id"]}, 403

        self.service.add_new(**new_sens)
        return {'message': 'Added the new sensor with id %i' % new_sens["sens_id"]}, 201


class MeteoApi(Resource):
    def get(self):
        return {'description': 'Meteorological Sensors API'}


def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(MeteoApi, '/')
    api.add_resource(Sensors, '/sensors/')
    api.add_resource(Sensor, '/sensors/<int:sens_id>/')
    app.run(debug=True)


if __name__ == '__main__':
    main()
