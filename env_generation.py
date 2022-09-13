from base64 import b64encode
from os import urandom

def create_token(nbytes = 128):
  random_bytes = urandom(nbytes)
  return b64encode(random_bytes)

api_token = create_token()
jwt_secret = create_token()

print(f"API_TOKEN={api_token.decode()}")
print(f"JWT_SECRET={jwt_secret.decode()}")
print(f"PORT=5050")
print(f"ENV=dev")
print(f"DEBUG=True")