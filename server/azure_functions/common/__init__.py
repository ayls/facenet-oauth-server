from . import jwt_util

jwtUtil: jwt_util.JwtUtil = None

def initJwtUtil(config) -> jwt_util.JwtUtil:
  global jwtUtil
  if jwtUtil is None:
    jwtUtil = jwt_util.JwtUtil(config)

  return jwtUtil