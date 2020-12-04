import logging
import json
import os
from ..common import *
import urllib.parse as urlparse
from urllib.parse import urlencode
import azure.functions as func

def redirect(redirect_uri, new_entries):
  url_parts = list(urlparse.urlparse(redirect_uri))
  queries = dict(urlparse.parse_qsl(url_parts[4]))
  queries.update(new_entries)
  url = redirect_uri + "#" + urlencode(queries)
  print(url)
  return func.HttpResponse(
        status_code=302,
        headers={ 'Location': url })

def main(req: func.HttpRequest) -> func.HttpResponse:
  requestBody = req.get_body().decode('utf-8') 
  formData = dict(urlparse.parse_qsl(requestBody))
  capturedImageData = formData['captured_image_data']
  otp = formData['otp']
  clientId = formData['client_id']
  redirectUri = formData['redirect_uri']
  state = formData['state']
  nonce = formData['nonce']

  if None in [capturedImageData, otp, clientId, redirectUri, state, nonce]:
    error = json.dumps({
      'error': 'invalid request'
    })
    return func.HttpResponse(
          error,
          status_code=400,
          mimetype='application/json')

  jwtUtil = initJwtUtil(os.environ)    
  if not jwtUtil.verify_client_info(clientId, redirectUri):
    error = json.dumps({
      'error': 'invalid client_id or redirect_uri'
    })
    return func.HttpResponse(
          error,
          status_code=400,
          mimetype='application/json')    

  username = jwtUtil.authenticate_user_credentials(capturedImageData, otp)
  if username is None:
    return func.HttpResponse(
          status_code=302,
          headers={ 'Location': '/accessdenied' })

  idToken = jwtUtil.generate_id_token(clientId, username, nonce)
  return redirect(redirectUri, {
    'id_token': idToken,
    'expires_in': os.environ['JWT_LIFE_SPAN'],
    'state': state
    })        
