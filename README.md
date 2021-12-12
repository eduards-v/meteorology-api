# Meteorology API
## API to subscribe and persist meteorological sensors and the data
Brief description of the API here...

## Prerequisites to start API server

* Python 3 environment
* Restful Flask framework
* PostgreSQL 13 database


<details>
<summary>Setup python virtual environment</summary>

#### Setup python virtual environment
```
# Windows
python -m venv \path\to\project\meteorology-api\venv

# Unix
python -m venv /path/to/project/meteorology-api/venv
```
#### Activate venv on Windows
```
\path\to\project\meteorology-api\venv\Scripts\activate.bat
```
#### Activate venv on Mac or Linux
```
source /path/to/project/meteorology-api/venv/bin/activate
```
#### Deactivate virtual environment
```
deactivate
```
</details>

<details>
<summary>Install python dependency packages via pip</summary>

Notes: 
* make sure you activate your virtual environment before installing, 
otherwise packages will be installed to your global python site packages
* Use path delimiting character corresponding to your OS (Unix, Windows)
```
pip install -r /path/to/project/meteorology-api/requirements.txt
```
</details>

<details>
<summary>Setup PostgreSQL database</summary>

Download PostgreSQL server [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) for your OS.

I'm using PostgreSQL 13, but the current project is version agnostic for any currently **_supported_** versions.

Once software is installed and server is started, create database and execute the schema file.

#### Create database
```
/path/to/postgres/bin/psql -U postgres -c "create database meteodb;"
```

#### Create *meteodb* schema
Navigate to the project root directory meteorology-api.
```
psql -U postgres -d meteodb -f src/main/resources/database_schema.ddl
```

**Note**: schema DDL will create a role *meteodba* for a *meteodb* database with a default password *meteodba123.*
</details>

<details>
<summary>Starting API server</summary>

Navigate to the project root directory meteorology-api.

To start API server from the root project directory run the following command from the consul
```
python src\main\python\main.py
```
</details>

<details>
<summary>API Usage</summary>

Available paths and methods

###Get All sensors

**Request**

```
GET /sensors/

curl -X GET http://localhost:5000/sensors/ -H 'Content-Type: application/json'
```

**Response**
```
HTTP/1.1 200 OK
content-length: 567
content-type: application/json
date: Sun, 12 Dec 2021 21:59:21 GMT
server: Werkzeug/2.0.2 Python/3.9.7

[
    {
        "metadata": {
            "city_name": "Galway",
            "country_name": "Ireland"
        },
        "sens_id": 1
    },
    {
        "metadata": {
            "city_name": "Berlin",
            "country_name": "Germany"
        },
        "sens_id": 2
    },
    {
        "metadata": {
            "city_name": "Berlin",
            "country_name": "Germany"
        },
        "sens_id": 999
    }
]
```

###Subscribe a new sensor

**Request**
```
POST /sensors/

curl -X POST http://localhost:5000/sensors/ 
-H 'Content-Type: application/json' 
-d '{ "sens_id": 777, "metadata": { "country_name": "Germany", "city_name": "Berlin" }}'
```
**Response**
```
HTTP/1.1 201 CREATED
content-length: 129
content-type: application/json
date: Sun, 12 Dec 2021 21:56:15 GMT
server: Werkzeug/2.0.2 Python/3.9.7

{
    "metadata": {
        "country_name": "Germany",
        "city_name": "Berlin"
    },
    "sens_id": 777
}
```

###Find a sensor by ID
**Request**
```
GET /sensors/{id}/

curl -X GET http://localhost:5000/sensors/1/ 
-H 'Content-Type: application/json'
```
**Response**
```
OK
content-length: 111
content-type: application/json
date: Sun, 12 Dec 2021 22:02:38 GMT
server: Werkzeug/2.0.2 Python/3.9.7

{
    "metadata": {
        "city_name": "Galway",
        "country_name": "Ireland"
    },
    "sens_id": 1
}
```

###Get sensor's latest record
**Request**
```
GET /sensors/{id}/data/

curl -X GET http://localhost:5000/sensors/1/data/ 
-H 'Content-Type: application/json'
```

**Response**
```
HTTP/1.1 200 OK
content-length: 169
content-type: application/json
date: Sun, 12 Dec 2021 22:04:41 GMT
server: Werkzeug/2.0.2 Python/3.9.7

{
    "sens_id": 1,
    "data": [
        {
            "temperature": 13.5,
            "humidity": 70,
            "recorded": "2021-12-09 19:04:56"
        }
    ]
}
```

###Send sensor's latest records
**Request**
```
PUT /sensors/{id}/

curl -X PUT http://localhost:5000/sensors/1/ 
-H 'Content-Type: application/json' 
-d '{"data": [{ "temperature": 14.1, "humidity": 17, "recorded": "2021-12-11 22:52:25.536249"}, 
{"temperature": 13.7,"humidity": 16,"recorded": "2021-12-11 21:52:25.536249"} ]}'
```

**Response**
```
HTTP/1.1 201 CREATED
content-length: 60
content-type: application/json
date: Sun, 12 Dec 2021 22:11:47 GMT
server: Werkzeug/2.0.2 Python/3.9.7

{
    "message": "Recorded data for the sensor with id 1"
}
```

###Delete sensor by ID
**Request**
```
DELETE /sensors/{id}/

curl -X DELETE http://localhost:5000/sensors/777/ -H 'Content-Type: application/json'
```

**Response**
```
HTTP/1.1 204 NO CONTENT
content-type: application/json
date: Sun, 12 Dec 2021 22:17:05 GMT
server: Werkzeug/2.0.2 Python/3.9.7
```
</details>
