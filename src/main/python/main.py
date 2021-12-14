from flask import Flask
from flask_restful import Api

from resources.sensor_resources import Sensors, Sensor, SensorData


def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Sensors, '/sensors/')
    api.add_resource(Sensor, '/sensors/<int:sens_id>/')
    api.add_resource(SensorData, '/sensors/<int:sens_id>/data/')
    app.run(debug=True)


if __name__ == '__main__':
    main()
