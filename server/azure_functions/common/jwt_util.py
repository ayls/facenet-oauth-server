import jwt
import time
import base64
import json
import os
from . import detection
import pyotp

class JwtUtil:

  def __init__(self, config):
    self.config = config

    scriptPath = os.path.abspath(__file__)
    scriptDir = os.path.dirname(scriptPath)
    with open(os.path.join(scriptDir, 'private.pem'), 'rb') as f:
      self.private_key = f.read()

    self.detection = detection.Detection()

  def authenticate_user_credentials(self, image, otp):
    content = image.split(';')[1]
    image_encoded = content.split(',')[1]
    body = base64.decodebytes(image_encoded.encode('utf-8'))        
    username = self.detection.detect(body)
    if (username is not None):
      user_otp_secrets_raw = self.config['USER_OTP_SECRETS']
      user_otp_secrets_dict = json.loads(user_otp_secrets_raw)      
      totp = pyotp.TOTP(user_otp_secrets_dict[username])
      if (totp.now() == otp):
        return username

    return None

  def verify_client_info(self, client_id, redirect_uri):
    try:
      redirects_raw = self.config['CLIENT_REDIRECTS']
      redirects_dict = json.loads(redirects_raw)
      configured_redirect = redirects_dict[client_id]
      return redirect_uri == configured_redirect
    except:
      return False

  def generate_id_token(self, client_id, username, nonce):
    payload = {
      'iss': self.config['ISSUER'],
      'sub': username,
      'name': username,
      'nonce': nonce,
      'aud': client_id,
      'iat':  (int)(time.time()),
      'exp':  (int)(time.time()) + int(self.config['JWT_LIFE_SPAN'])
    }

    id_token = jwt.encode(payload, self.private_key, algorithm = 'RS256').decode()

    return id_token
