class Config(object):
  ISSUER = 'sample-auth-server'
  JWT_LIFE_SPAN = 1800  
  CLIENT_IDS = []
  REDIRECT_URIS = []
  USER_OTP_SECRETS = {}

class DevelopmentConfig(Config):
  CLIENT_IDS = [ 'sample-client' ]
  REDIRECT_URIS = [ 'http://localhost:8080' ]
  USER_OTP_SECRETS = { 'YourUsername': 'ValueReturnedByPyOTP' }

class ProductionConfig(Config):
  pass