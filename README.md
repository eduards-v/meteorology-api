# Meteorology API
## API to subscribe and persist meteorological sensors and the data
Brief description of the API here...

## Prerequisites to start API server

* Python 3 environment
* Restful Flask framework

#### Setup python virtual environment
```
python -m venv \path\to\project\venv
```
#### Activate venv on Windows
```
\path\to\project\venv\Scripts\activate.bat
```
#### Activate venv on Mac or Linux
```
source /path/to/project/venv/bin/activate
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
pip install -r /path/to/project/requirements.txt
```

## Starting API server
Navigate to the project root directory meteorology-api.

To start API server from the root project directory run the following command from the consul
```
python src\main\python\main.py
```

