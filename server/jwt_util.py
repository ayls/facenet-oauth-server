import jwt
import time
import base64
import detection

ISSUER = 'sample-auth-server'
JWT_LIFE_SPAN = 1800

class JwtUtil:

  def __init__(self):
    with open('private.pem', 'rb') as f:
      self.private_key = f.read()

    self.detection = detection.Detection()

  def authenticate_user_credentials(self, image):
    content = image.split(';')[1]
    image_encoded = content.split(',')[1]
    body = base64.decodebytes(image_encoded.encode('utf-8'))        
    return self.detection.detect(body)

  def verify_client_info(self, client_id, redirect_uri):
    # verify client_id and redirect_uri validity
    return True

  def generate_id_token(self, nonce, client_id, username):
    payload = {
      "iss": ISSUER,
      "sub": username,
      "name": username,
      "nonce": nonce,
      "aud": client_id,
      "iat": time.time(),
      "exp": time.time() + JWT_LIFE_SPAN
    }

    access_token = jwt.encode(payload, self.private_key, algorithm = 'RS256').decode()

    return access_token
