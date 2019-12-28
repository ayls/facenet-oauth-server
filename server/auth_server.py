import os
import json
#import ssl
import urllib.parse as urlparse

from urllib.parse import urlencode
from auth import (authenticate_user_credentials, generate_id_token,  
                  verify_client_info, JWT_LIFE_SPAN)
from flask import Flask, redirect, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def process_redirect_uri(redirect_uri, new_entries):
  # Prepare the redirect URL
  url_parts = list(urlparse.urlparse(redirect_uri))
  queries = dict(urlparse.parse_qsl(url_parts[4]))
  queries.update(new_entries)
  url_parts[4] = urlencode(queries)
  url = redirect_uri + "#" + url_parts[4]
  return url

@app.route('/jwks')
def jwks():
  # Return jwks definition
  json_url = os.path.join(app.root_path, "public.jwk")
  data = json.load(open(json_url))
  return jsonify(data)

@app.route('/auth')
def auth():
  # Describe the access request of the client and ask user for approval
  client_id = request.args.get('client_id')
  redirect_uri = request.args.get('redirect_uri')
  state = request.args.get('state')
  nonce = request.args.get('nonce')  

  if None in [ client_id, redirect_uri, state, nonce ]:
    return json.dumps({
      "error": "invalid_request"
    }), 400

  if not verify_client_info(client_id, redirect_uri):
    return json.dumps({
      "error": "invalid_client"
    })

  return render_template('Implicit_grant_access.html',
                         client_id = client_id,
                         redirect_uri = redirect_uri,
                         state=state,
                         nonce=nonce)

@app.route('/signin', methods = ['POST'])
def signin():
  # Issues authorization code
  captured_image_data = request.form.get('captured_image_data')  
  client_id = request.form.get('client_id')
  redirect_uri = request.form.get('redirect_uri')
  state = request.form.get('state')  
  nonce = request.form.get('nonce')    

  if None in [captured_image_data, client_id, redirect_uri, state, nonce]:
    return json.dumps({
      "error": "invalid_request"
    }), 400

  if not verify_client_info(client_id, redirect_uri):
    return json.dumps({
      "error": "invalid_client"
    })  

  if not authenticate_user_credentials(captured_image_data):
    return json.dumps({
      'error': 'access_denied'
    }), 401

  id_token = generate_id_token(nonce, client_id)

  return redirect(process_redirect_uri(redirect_uri, {
    'id_token': id_token,
    'expires_in': JWT_LIFE_SPAN,
    'state': state
    }), code = 302)


if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5001, debug = True)