import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'etSSOy3Ee34rm$QFLXYzI3Yn6hVo$QZ3'
