class Config(object):
  ISSUER = 'facenet-oauth'
  JWT_LIFE_SPAN = 43200  
  CLIENT_REDIRECTS = {}
  USER_OTP_SECRETS = {}

class DevelopmentConfig(Config):
  CLIENT_REDIRECTS = { 'sample-client': 'http://localhost:8080' }
  USER_OTP_SECRETS = { 'you': 'your-key' }

class ProductionConfig(Config):
  CLIENT_REDIRECTS = {}
  USER_OTP_SECRETS = {}