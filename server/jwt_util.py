import jwt
import time
import base64
import detection
import pyotp

ISSUER = 'sample-auth-server'
JWT_LIFE_SPAN = 1800

class JwtUtil:

  def __init__(self):
    with open('private.pem', 'rb') as f:
      self.private_key = f.read()

    self.detection = detection.Detection()

  def authenticate_user_credentials(self, app_config, image, otp):
    content = image.split(';')[1]
    image_encoded = content.split(',')[1]
    body = base64.decodebytes(image_encoded.encode('utf-8'))        
    username = self.detection.detect(body)
    if (username is not None):
      totp = pyotp.TOTP(app_config['USER_OTP_SECRETS'][username])
      if (totp.now() == otp):
        return username

    return None

  def verify_client_info(self, app_config, client_id, redirect_uri):
    # verify client_id and redirect_uri validity
    try:
      client_id_idx = app_config['CLIENT_IDS'].index(client_id)
      redirect_uri_idx = app_config['REDIRRECT_URIS'].index(redirect_uri)
      return client_id_idx == redirect_uri_idx
    except:
      return False

  def generate_id_token(self, nonce, client_id, username):
    payload = {
      'iss': ISSUER,
      'sub': username,
      'name': username,
      'nonce': nonce,
      'aud': client_id,
      'iat': time.time(),
      'exp': time.time() + JWT_LIFE_SPAN
    }

    access_token = jwt.encode(payload, self.private_key, algorithm = 'RS256').decode()

    return access_token