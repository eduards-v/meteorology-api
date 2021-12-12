import psycopg2
from psycopg2.extras import DictCursor


class PostgresDriver(object):
    def __init__(self, database, connection):
        self._database = database
        self._conn = connection

    def _run(self, query, *args):
        cursor = self._conn.cursor()
        try:
            cursor.execute(query, *args)
        except psycopg2.Error as err:
            self._conn.rollback()
            cursor.close()
            raise
            # Map psycopg2 exceptions to a custom exceptions
            # Raise the custom exception
        except Exception:
            # Catch the generic exception to close the cursor. Raise exception for later handling
            cursor.close()
            raise

        return cursor

    def run(self, query, *args):
        cursor = self._run(query, *args)
        cursor.close()

    def fetchone(self, query, *args):
        cursor = self._run(query, *args)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetchall(self, query, *args):
        cursor = self._run(query, *args)
        results = cursor.fetchall()
        cursor.close()
        return results


class PostgresConnection(object):
    def __init__(self, database, username=None, password=None, host="localhost", port=5432):
        self._database = database
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._connection = None

    def __enter__(self):
        # fetch default database credentials (username/password) here from the security locker
        # for the demo purposes I will use default meteodba/meteodba123 credentials
        # example getting credentials:
        # try:
        #       creds = CredentialsManager().get_creds("psql")
        # except CredentialsManagerException as err
        #       handle exception

        username = self._username or "meteodba"
        password = self._password or "meteodba123"

        self._connection = psycopg2.connect(user=username, password=password, database=self._database,
                                            host=self._host, port=self._port,
                                            cursor_factory=DictCursor)

        return PostgresDriver(self._database, self._connection)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit all transactions for the current connections on exit or roll them back on unhandled exception.
        # ACID property; all or nothing
        if exc_type:
            # may want to log here
            self._connection.rollback()
        else:
            self._connection.commit()
        self._connection.close()


if __name__ == '__main__':
    with PostgresConnection(database="meteodb") as conn:
        res = conn.fetchall("SELECT * FROM countries;")

    print(res)
    for r in res:
        print(dict(r))
        print(r["country_name"])

    with PostgresConnection(database="meteodb") as conn:
        res = conn.fetchall("SELECT * FROM cities;")

    print(res)
    for r in res:
        print(dict(r))
        print(r["city_name"])

    cq = "select city_name, country_name from cities LEFT JOIN countries ON cities.ctr_id = countries.ctr_id;"
    with PostgresConnection(database="meteodb") as conn:
        res = conn.fetchall(cq)

    print(res)
    for r in res:
        print(dict(r))
        print(r["city_name"])

    cq = "select city_name, country_name from cities " \
         "LEFT JOIN countries ON cities.ctr_id = countries.ctr_id " \
         "WHERE country_name in (%s, %s);"

    with PostgresConnection(database="meteodb") as conn:
        res = conn.fetchall(cq, ("Ireland", "England"))

    for r in res:
        print(dict(r))
