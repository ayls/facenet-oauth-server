import logging
import json
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
  responseBody = json.dumps({
    'issuer': os.environ['ISSUER'],
    'authorization_endpoint': os.environ['HOST_URL'] +'/auth',
    'end_session_endpoint': os.environ['HOST_URL'] + '/signout',
    'jwks_uri': os.environ['HOST_URL'] + '/jwks',
    'token_endpoint_auth_methods_supported': [ 'none' ],    
    'response_types_supported': [ 'id_token' ],
    'response_modes_supported': [ 'query' ],
    'subject_types_supported': [ 'public' ],
    'id_token_signing_alg_values_supported': [ 'RS256' ],
    'grant_types_supported': [ 'implicit' ],	
    'scopes_supported': [ 'openid' ],
    'request_uri_parameter_supported': False
  })

  return func.HttpResponse(
        responseBody,
        status_code=200,
        mimetype='application/json')    
