import logging
import json
import os
from ..common import *
from ..common import renderer
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
  clientId = req.params.get('client_id')
  redirectUri = req.params.get('redirect_uri')
  state = req.params.get('state')
  nonce = req.params.get('nonce')

  if None in [ clientId, redirectUri, state, nonce ]:
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

  scriptpath = os.path.abspath(__file__)
  scriptdir = os.path.dirname(scriptpath)
  htmlFilename = os.path.join(scriptdir, 'sign_in.html')
  htmlContent = renderer.renderTemplate(
    htmlFilename,
    { 
      'client_id' : clientId,
      'redirect_uri' : redirectUri,
      'state' : state,
      'nonce' : nonce    
    }
  )
  
  return func.HttpResponse(
        htmlContent,
        status_code=200,
        mimetype='text/html'
  )
