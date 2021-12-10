from flask import Flask
from flask_restful import Resource, Api


class Sensor(Resource):
    def __init__(self):
        self.service = None

    def get(self, sens_id):
        pass

    def put(self, sens_id):
        pass

    def delete(self, sens_id):
        pass


class Sensors(Resource):
    def __init__(self):
        pass

    def get(self):
        pass

    def post(self):
        pass


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
