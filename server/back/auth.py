import jwt
import random
import time
import base64

ISSUER = 'sample-auth-server'
JWT_LIFE_SPAN = 1800

authorization_codes = {}

with open('private.pem', 'rb') as f:
  private_key = f.read()

def authenticate_user_credentials(image):
  content = image.split(';')[1]
  image_encoded = content.split(',')[1]
  body = base64.decodebytes(image_encoded.encode('utf-8'))  
  # print(body)
  # with open('test.jpg', 'wb') as f:
  #   f.write(body)
  return True

def verify_client_info(client_id, redirect_url):
  return True

def generate_id_token(nonce, client_id):
  payload = {
    "iss": ISSUER,
    "sub": "{0}".format(random.randint(0, 2147483647)),
    "nonce": nonce,
    "aud": client_id,
    "iat": time.time(),
    "exp": time.time() + JWT_LIFE_SPAN
  }

  access_token = jwt.encode(payload, private_key, algorithm = 'RS256').decode()

  return access_token
