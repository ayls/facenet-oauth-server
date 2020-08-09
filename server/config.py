class Config(object):
  CLIENT_IDS = []
  REDIRRECT_URIS = []
  USER_OTP_SECRETS = {}

class DevelopmentConfig(Config):
  CLIENT_IDS = [ 'sample-client' ]
  REDIRRECT_URIS = [ 'http://localhost:8080' ]
  USER_OTP_SECRETS = { 'YourUsername': 'ValueReturnedByPyOTP' }

class ProductionConfig(Config):
  pass