import logging
import os
from ..common import renderer
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
  scriptpath = os.path.abspath(__file__)
  scriptdir = os.path.dirname(scriptpath)
  htmlFilename = os.path.join(scriptdir, 'signed_out.html')
  htmlContent = renderer.renderTemplate(htmlFilename, {})

  return func.HttpResponse(
        htmlContent,
        status_code=200,
        mimetype='text/html'
  )  