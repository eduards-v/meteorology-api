from models.sensor_model import SensorModelSchema
from repo.connectors.psql.driver import PostgresConnection
from utils.dict_utils import nest_flat_dict


class SensorsRepo(object):
    def __init__(self):
        self._database = "meteodb"

    def fetch_all(self):
        query = "select sens_id, city_name, country_name from sensors " \
                "LEFT JOIN cities ON sensors.cit_id = cities.cit_id " \
                "LEFT JOIN countries ON cities.ctr_id = countries.ctr_id;"
        with PostgresConnection(database=self._database) as conn:
            sensors = conn.fetchall(query)
        if not sensors:
            return

        # driver returns list of DictRow objects
        # convert into the model object
        sensors = [nest_flat_dict(dict(sensor), "metadata", "city_name", "country_name") for sensor in sensors]
        return SensorModelSchema(many=True).load(sensors)

    def fetch_by_id(self, sens_id):
        query = "select sens_id, city_name, country_name from sensors " \
                "LEFT JOIN cities ON sensors.cit_id = cities.cit_id " \
                "LEFT JOIN countries ON cities.ctr_id = countries.ctr_id WHERE sens_id = %s;"
        with PostgresConnection(database=self._database) as conn:
            sensor = conn.fetchone(query, (sens_id,))
        if not sensor:
            return

        # driver returns DictRow object
        # convert into the model object
        sensor = nest_flat_dict(dict(sensor), "metadata", "city_name", "country_name")
        return SensorModelSchema().load(sensor)

    def delete_by_id(self, sens_id):
        query = "DELETE from sensors WHERE sens_id = %s;"
        with PostgresConnection(database=self._database) as conn:
            conn.run(query, (sens_id, ))

    def add_new(self, sensor_model):
        query = "INSERT INTO sensors (sens_id, cit_id) " \
                "VALUES (%s, (select cit_id from cities where city_name = %s));"
        with PostgresConnection(database=self._database) as conn:
            conn.run(query, (sensor_model.sens_id, sensor_model.metadata["city_name"]))

    def record_sensor_data(self, sensor_model):
        query = "INSERT INTO sensors_data (sens_id, temperature, humidity, recorded) " \
                "VALUES (%s, %s, %s, %s);"
        with PostgresConnection(database=self._database) as conn:
            for record in sensor_model.data:
                conn.run(query, (sensor_model.sens_id,
                                 record["temperature"],
                                 record["humidity"],
                                 record["recorded"]))

    def get_latest_data(self, sens_id):
        query = "select sensors.sens_id, temperature, humidity from sensors " \
                "LEFT JOIN sensors_data ON sensors.sens_id = sensors_data.sens_id " \
                "WHERE sensors.sens_id = %s ORDER BY recorded DESC LIMIT 1;"
        with PostgresConnection(database=self._database) as conn:
            latest_data = conn.fetchone(query, (sens_id, ))
        if not latest_data:
            return

        latest_data = nest_flat_dict(dict(latest_data), "data", "temperature", "humidity")

        # wrap data into the list as expected by the model. Need to find a better approach to the problem.
        latest_data["data"] = [latest_data["data"].copy()]
        return SensorModelSchema().load(latest_data)
