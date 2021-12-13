from repo.connectors.psql.driver import PostgresConnection


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
            return []
        return [dict(sensor) for sensor in sensors]

    def fetch_by_id(self, sens_id):
        query = "select sens_id, city_name, country_name from sensors " \
                "LEFT JOIN cities ON sensors.cit_id = cities.cit_id " \
                "LEFT JOIN countries ON cities.ctr_id = countries.ctr_id WHERE sens_id = %s;"
        with PostgresConnection(database=self._database) as conn:
            sensor = conn.fetchone(query, (sens_id,))
        return dict(sensor) if sensor else {}

    def delete_by_id(self, sens_id):
        query = "DELETE from sensors WHERE sens_id = %s;"
        with PostgresConnection(database=self._database) as conn:
            conn.run(query, (sens_id, ))

    def add_new(self, sens_id, metadata):
        query = "INSERT INTO sensors (sens_id, cit_id) " \
                "VALUES (%s, (select cit_id from cities where city_name = %s));"
        with PostgresConnection(database=self._database) as conn:
            conn.run(query, (sens_id, metadata["city_name"]))

    def record_sensor_data(self, sens_id, sens_data):
        query = "INSERT INTO sensors_data (sens_id, temperature, humidity, recorded) " \
                "VALUES (%s, %s, %s, %s);"
        with PostgresConnection(database=self._database) as conn:
            for record in sens_data:
                conn.run(query, (sens_id,
                                 record["temperature"],
                                 record["humidity"],
                                 record["recorded"]))

    def get_latest_data(self, sens_id):
        query = "select sensors.sens_id, temperature, humidity, recorded from sensors " \
                "LEFT JOIN sensors_data ON sensors.sens_id = sensors_data.sens_id " \
                "WHERE sensors.sens_id = %s ORDER BY recorded DESC LIMIT 1;"
        with PostgresConnection(database=self._database) as conn:
            latest_data = conn.fetchone(query, (sens_id, ))
        return dict(latest_data)
