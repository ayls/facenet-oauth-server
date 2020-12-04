import logging
import azure.functions as func
from ..common import *
import os

def main(mytimer: func.TimerRequest) -> None:
  jwtUtil = initJwtUtil(os.environ)    
  logging.info('Server warmed up')