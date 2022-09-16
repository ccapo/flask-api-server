# flask-api-server
A Flask API Server

## Setup Environment
```
git clone https://github.com/ccapo/flask-api-server.git
sudo apt install virtualenv python3.8
virtualenv --python=/usr/bin/python3.8 /home/ubuntu/flask-api-server/env
source env/bin/activate
```

## Install Packages
```
pip install -r requirements.txt
```

## Create .env file
```
python env_setup.py > .env
```

## Initialize the Database
```
cd data
python init_db.py
cd ../
```

## Run API Server (Promote to service?)
```
python app.py
```

## Exit Environment
```
deactivate
```
