# flask-api-server
A Flask API Server

## Setup Environment
```
virtualenv --python=/usr/bin/python3.8 /home/ubuntu/flask-api-server/env
source env/bin/activate
```

## Install Packages
```
pip install -r requirements.txt
```

## Generate .env file
```
python env_generation.py > .env
```

## Initialize the Database
```
python init_db.py
```

## Run API Server (Promote to service?)
```
python app.py
```

## Exit Environment
```
deactivate
```
