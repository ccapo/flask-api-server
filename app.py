from flask import Flask, request
from dotenv import load_dotenv
import signal
import time
import os
import logging

from db import Database
from authorization import Auth

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%y-%m-%d %H:%M:%S')

# Start the clock
startTime = time.time()

# Load .env variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Define app config parameters
app.config['HOST'] = os.getenv('HOST', '0.0.0.0')
app.config['PORT'] = os.getenv('PORT', 80)
app.config['ENV'] = os.getenv('ENV', 'production')
app.config['DEBUG'] = os.getenv('DEBUG', False)
app.config['DATABASE'] = os.path.join(os.getcwd(), './data/db.sqlite3')

# Database
db = Database(app.config['DATABASE'])

# Auth
auth = Auth(db)

# Our signal handler
def signal_handler(signum, frame):
  db.close()
  print("")
  logging.info(f"Signal {signum} received, exiting...")
  exit(0)

# Register our signal handler with desired signal
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# External Endpoints
@app.route('/', methods=['GET'])
def uptime():
  return {'uptime': time.time() - startTime}

## TODO: Consider moving logic from Flask to MQTT listener
@app.route('/register', methods=['POST'])
def register():
  body = request.get_json()
  customer_uuid = body['customer_uuid']
  client_uuid = body['client_uuid']
  registration_token = body['registration_token']

  result = db.get_registration(customer_uuid)
  if result is not None:
    if result['token'] == registration_token:
      # Check if client exists for customer, if not create it
      db.upsert_client(customer_uuid, client_uuid)
      token = auth.jwt_token(customer_uuid, client_uuid)
      updated = db.upsert_authorization(customer_uuid, client_uuid, token)
      if updated:
        return {"message": "Successfully registered", "token": token}
      else:
        return {"message": "Registration token is invalid"}, 401
    else:
      return {"message": "Registration token is invalid"}, 401
  else:
    return {"message": "Registration token is invalid"}, 401

@app.route('/scan/upload', methods=['POST'])
@auth.jwt_required
def scan_upload(customer, client):
  try:
    body = request.get_json()
    db.set_scan_data(customer, client, body['data'])
    return {"message": "Scan result received"}, 201
  except Exception as e:
    return {
      "message": "Something went wrong",
      "error": str(e)
    }, 500

@app.route('/audit/upload', methods=['POST'])
@auth.jwt_required
def audit_upload(customer, client):
  try:
    body = request.get_json()
    db.set_audit_data(customer, client, body['data'])
    return {"message": "Audit receieved"}, 201
  except Exception as e:
    return {
      "message": "Something went wrong",
      "error": str(e)
    }, 500

# Internal Endpoints
@app.route('/api/scan', methods=['POST'])
@auth.token_required
def scan(token):
  body = request.get_json()
  return {"message": "Scan initiated"}

@app.route('/api/scan/group', methods=['POST'])
@auth.token_required
def scan_group(token):
  body = request.get_json()
  return {"message": "Scan initiated for group"}

# TODO: Add endpoint to add client to specify group, creating group if it DNE
@app.route('/api/scan/group/create', methods=['POST'])
@auth.token_required
def scan_group_create(token):
  body = request.get_json()
  return {"message": "Scan group created"}

@app.route('/api/scan/group/membership', methods=['PUT'])
@auth.token_required
def scan_group_membership(token):
  body = request.get_json()
  return {"message": "Scan group membership updated"}

@app.route('/api/contain', methods=['POST'])
@auth.token_required
def contain(token):
  body = request.get_json()
  return {"message": "Containment initiated"}

@app.route('/api/uncontain', methods=['POST'])
@auth.token_required
def uncontain(token):
  body = request.get_json()
  return {"message": "Uncontainment initiated"}

if __name__ == '__main__':
  app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])