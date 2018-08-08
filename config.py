import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'etSSOy3Ee34rm$QFLXYzI3Yn6hVo$QZ3'
    DIARY_API_URL = os.environ.get('DIARY_API_URL') or 'http://localhost:5000'
    DIARY_API_VERSION = os.environ.get('DIARY_API_VERSION') or 'v1'
    DIARY_API_TIMEOUT = os.environ.get('DIARY_API_TIMEOUT') or 5
