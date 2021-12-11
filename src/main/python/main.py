from flask import Flask, request
from flask_restful import Resource, Api

from dbo.sensor_dbo import SensorModelSchema
from services.sensors_service import SensorsService


class Sensor(Resource):
    def __init__(self):
        self.service = SensorsService()

    def get(self, sens_id):
        sensor = self.service.get_by_id(sens_id)
        if not sensor:
            return {"message": "The sensor with id %i not found" % sens_id}, 404
        print(sensor.data)
        print(sensor)
        return SensorModelSchema().dump(sensor)

    def put(self, sens_id):
        sensor = self.service.get_by_id(sens_id)
        if not sensor:
            return {"message": "The sensor with id %i not found" % sens_id}, 404

        json_data = request.get_json(force=True)
        json_data["sens_id"] = sens_id
        sensor = SensorModelSchema().load(json_data)
        self.service.record_data(sensor)

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
        sensors = self.service.get_all()
        return SensorModelSchema(many=True).dump(sensors)

    def post(self):
        json_data = request.get_json(force=True)

        if self.service.get_by_id(json_data["sens_id"]):
            return {"message": "The sensor with id %i already exists" % json_data["sens_id"]}, 403

        sensor = SensorModelSchema().load(json_data)
        self.service.add_new(sensor)

        return SensorModelSchema().dump(sensor), 201


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
