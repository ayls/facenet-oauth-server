import os
import json
#import ssl
import urllib.parse as urlparse
import jwt_util

from urllib.parse import urlencode
from jwt_util import (JWT_LIFE_SPAN)
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_cors import CORS

app = Flask(__name__)
if app.config['ENV'] == 'production':
  app.config.from_object('config.ProductionConfig')
else:
  app.config.from_object('config.DevelopmentConfig')
CORS(app)

jwt = jwt_util.JwtUtil(app.config)

def process_redirect_uri(redirect_uri, new_entries):
  # Prepare the redirect URL
  url_parts = list(urlparse.urlparse(redirect_uri))
  queries = dict(urlparse.parse_qsl(url_parts[4]))
  queries.update(new_entries)
  url_parts[4] = urlencode(queries)
  url = redirect_uri + "#" + url_parts[4]
  return url

@app.route('/.well-known/openid-configuration')
def wellKnownConfig():
  # Return jwks definition
  wrapped_data = {
    'issuer': jwt_util.ISSUER,
    'authorization_endpoint': request.host_url +'auth',
    'end_session_endpoint': request.host_url + 'signout',
    'jwks_uri': request.host_url + 'jwks'
  }
  return jsonify(wrapped_data)


@app.route('/jwks')
def jwks():
  # Return jwks definition
  json_url = os.path.join(app.root_path, 'public.jwk')
  data = json.load(open(json_url))
  wrapped_data = {
    "keys": [ data ]
  }
  return jsonify(wrapped_data)

@app.route('/auth')
def auth():
  # Describe the access request of the client and ask user for approval
  client_id = request.args.get('client_id')
  redirect_uri = request.args.get('redirect_uri')
  state = request.args.get('state')
  nonce = request.args.get('nonce')

  if None in [ client_id, redirect_uri, state, nonce ]:
    return json.dumps({
      'error': 'invalid_request'
    }), 400

  if not jwt.verify_client_info(client_id, redirect_uri):
    return json.dumps({
      'error': 'invalid_client or redirect_uri'
    })

  return render_template('sign_in.html',
                         client_id = client_id,
                         redirect_uri = redirect_uri,                         
                         state = state,
                         nonce = nonce)

@app.route('/signout')
def signout():
  # id_token_hint = request.args.get('id_token_hint')
  # revoke the token here

  return render_template('signed_out.html')

@app.route('/accessdenied')
def accessdenied():
  return render_template('access_denied.html')  

@app.route('/signin', methods = ['POST'])
def signin():
  # Issues authorization code
  captured_image_data = request.form.get('captured_image_data')
  otp = request.form.get('otp')
  client_id = request.form.get('client_id')
  redirect_uri = request.form.get('redirect_uri')
  state = request.form.get('state') 
  nonce = request.form.get('nonce')

  if None in [captured_image_data, otp, client_id, redirect_uri, state, nonce]:
    return json.dumps({
      'error': 'invalid_request'
    }), 400

  if not jwt.verify_client_info(client_id, redirect_uri):
    return json.dumps({
      'error": "invalid_client'
    }), 401  

  username = jwt.authenticate_user_credentials(captured_image_data, otp)
  if username is None:
    return redirect(url_for('accessdenied'), 302)

  id_token = jwt.generate_id_token(client_id, username, nonce)

  return redirect(process_redirect_uri(redirect_uri, {
    'id_token': id_token,
    'expires_in': JWT_LIFE_SPAN,
    'state': state
    }), code = 302)


if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(host='0.0.0.0', port = 5000, debug = True, ssl_context = context)
  app.run(host='0.0.0.0', port = 5001, debug = True)