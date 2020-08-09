class Config(object):
  CLIENT_IDS = []
  REDIRRECT_URIS = []

class DevelopmentConfig(Config):
  CLIENT_IDS = [ "sample-client" ]
  REDIRRECT_URIS = [ "http://localhost:8080" ]

class ProductionConfig(Config):
  pass