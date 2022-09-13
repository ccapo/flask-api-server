from flask import request
from functools import wraps
from datetime import datetime, timedelta
from pytz import timezone
import jwt
import os

class Auth:
  def __init__(self, db):
    self.db = db
    self.API_TOKEN = os.getenv('API_TOKEN', 'shhhh')
    self.JWT_SECRET = os.getenv('JWT_SECRET', 'shhhh')

  # API token required for internal endpoints
  def token_required(self, f):
    @wraps(f)
    def decorated(*args, **kwargs):
      token = None
      if 'X-API-KEY' in request.headers:
        token = request.headers.get('X-API-KEY')
      if not token:
        return {
          "message": "API token is missing",
          "error": "Unauthorized"
        }, 401
      if token != self.API_TOKEN:
        return {
            "message": "Invalid API token",
            "error": "Unauthorized"
        }, 401

      return f(token, *args, **kwargs)

    return decorated

  # JWT required for external endpoints
  def jwt_required(self, f):
    @wraps(f)
    def decorated(*args, **kwargs):
      token = None
      if 'Authorization' in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
      if not token:
        return {
          "message": "Authentication token is missing",
          "error": "Unauthorized"
        }, 401

      try:
        data = jwt.decode(token, self.JWT_SECRET, algorithms=["HS256"], options={"require": ["iss", "iat", "exp"]})
        customer_uuid = data['customer_uuid']
        client_uuid = data['client_uuid']
        customer = None
        client = None

        # Fetch from DB
        result = self.db.get_client(customer_uuid, client_uuid)
        if result is not None:
          customer = result['customer_uuid']
          client = result['client_uuid']

        if customer is None or client is None:
          return {
            "message": "Invalid Authentication token",
            "error": "Unauthorized"
          }, 401

        # Check if token has been revoked
        result = self.db.get_authorization(customer_uuid, client_uuid)
        if result is None:
          return {
            "message": "Invalid Authentication token",
            "error": "Unauthorized"
          }, 401
        if result['token'] != token:
          return {
            "message": "Invalid Authentication token",
            "error": "Unauthorized"
          }, 401
      except Exception as e:
        return {
          "message": "Something went wrong",
          "error": str(e)
        }, 500

      return f(customer, client, *args, **kwargs)

    return decorated

  def jwt_token(self, customer_uuid, client_uuid, expiry_hours = 1):
    payload = {
        "customer_uuid": customer_uuid,
        "client_uuid": client_uuid,
        "iss": "awn",
        "iat": datetime.now(tz=timezone('utc')),
        "exp": datetime.now(tz=timezone('utc')) + timedelta(hours = expiry_hours)
    }
    token = jwt.encode(payload, self.JWT_SECRET, algorithm="HS256")
    return token
