import logging
import azure.functions as func
from ..common import *

def main(mytimer: func.TimerRequest) -> None:
  initJwtUtil()  
  logging.info('Server warmed up')