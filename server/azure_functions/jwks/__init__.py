import logging
import json
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
  scriptpath = os.path.abspath(__file__)
  scriptdir = os.path.dirname(scriptpath)
  jwkFilename = os.path.join(scriptdir, 'public.jwk')  
  jwkFile = open(jwkFilename, 'r')
  jwkData = jwkFile.read()
  jwkFile.close()   

  jwkJson = json.loads(jwkData)
  responseBody = json.dumps( {
    "keys": [ jwkJson ]
  })

  return func.HttpResponse(
        responseBody,
        status_code=200,
        mimetype='application/json')  
