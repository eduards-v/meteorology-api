# Meteorology API
## API to subscribe and persist meteorological sensors and the data
Brief description of the API here...

## Prerequisites to start API server

* Python 3 environment
* Restful Flask framework
* PostgreSQL 13 database

Click on each section down below to unfold more details.

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

### Get All sensors

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

### Subscribe a new sensor


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

### Find a sensor by ID

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

### Get sensor's latest record

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

### Send sensor's latest records

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

### Delete sensor by ID

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

<details>
<summary>Challanges faced during development</summary>

</br>

#### Architectural Challanges

My first and probably the most time-consuming challenge was to get up-to-speed with web server development.
I had to carefully choose which REST API framework to use because it would be hard to pivot away due to time constraints.
    
To me, two apparent choices were Django and Flask Restful.
I went ahead with the Flask Restful framework because:
* The Flask is WSGI, Django is a full-stack web framework. So since I don't need to design UI, Flask won here.
* Flask seems to be more flexible in design approach. Django is a feature-packed, heavier framework.
* Flask is more minimalistic, perfect for the timeframe I had.
* Django is monolithic; Flask is diversified. For RestFul micro-services, we don't do monoliths.
* As for ORM, both Django and Flask provide excellent support for it. Django has built-in ORM, providing native support; Flask uses SQLAlchemy. I decided not to use SQLAlchemy and designed ORM with PostgreSQL and psycopg2 driver.

</br>

The second challenge I faced was to pivot away from Flask's native marshaling feature.</br>
I found it quite ugly and hard to understand. On top of that, Flask developers stopped developing that feature and recommended using something better.</br>
That is where the Marshmallow came in handy. It is not only easy to use and grasp, but it also does a great job in encapsulation my model object.

</br>

#### Implementation Challanges

Another time-consuming challenge was Marshmallow's struggle to serialize Decimal and datetime objects.
Thankfully, it allowed me to implement a pre-dump method in which I could use simplejson library to serialize Decimal and datetime.
https://github.com/eduards-v/meteorology-api/blob/main/src/main/python/models/sensor_model.py#L18

I had to take it further with the datetime object and implement a custom encoder extension for simplejson to cast it to a string because the psycopg2 driver returns the datetime object from the PostgreSQL database. However, it seemed to be the cleanest option.
https://github.com/eduards-v/meteorology-api/blob/main/src/main/python/utils/json_encoders.py#L5



</details>
