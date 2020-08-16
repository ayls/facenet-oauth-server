import jwt
import time
import base64
import detection
import pyotp

ISSUER = 'sample-auth-server'
JWT_LIFE_SPAN = 1800

class JwtUtil:

  def __init__(self, app_config):
    self.app_config = app_config

    with open('private.pem', 'rb') as f:
      self.private_key = f.read()

    self.detection = detection.Detection()

  def authenticate_user_credentials(self, image, otp):
    content = image.split(';')[1]
    image_encoded = content.split(',')[1]
    body = base64.decodebytes(image_encoded.encode('utf-8'))        
    username = self.detection.detect(body)
    if (username is not None):
      totp = pyotp.TOTP(self.app_config['USER_OTP_SECRETS'][username])
      if (totp.now() == otp):
        return username

    return None

  def verify_client_info(self, client_id, redirect_uri):
    # verify client_id and redirect_uri validity
    try:
      client_id_idx = self.app_config['CLIENT_IDS'].index(client_id)
      redirect_uri_idx = self.app_config['REDIRECT_URIS'].index(redirect_uri)
      return client_id_idx == redirect_uri_idx
    except:
      return False

  def generate_id_token(self, client_id, username, nonce):
    payload = {
      'iss': self.app_config['ISSUER'],
      'sub': username,
      'name': username,
      'nonce': nonce,
      'aud': client_id,
      'iat': time.time(),
      'exp': time.time() + self.app_config['JWT_LIFE_SPAN']
    }

    id_token = jwt.encode(payload, self.private_key, algorithm = 'RS256').decode()

    return id_token
