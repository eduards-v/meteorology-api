# Meteorology API
## API to subscribe and persist meteorological sensors and the data
Brief description of the API here...

## Prerequisites to start API server

* Python 3 environment
* Restful Flask framework
* PostgreSQL 13 database

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

#### Install python dependency packages via pip
Notes: 
* make sure you activate your virtual environment before installing, 
otherwise packages will be installed to your global python site packages
* Use path delimiting character corresponding to your OS (Unix, Windows)
```
pip install -r /path/to/project/meteorology-api/requirements.txt
```

## Setup PostgreSQL database
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


## Starting API server
Navigate to the project root directory meteorology-api.

To start API server from the root project directory run the following command from the consul
```
python src\main\python\main.py
```
