"""Def diff application envs"""

class Config(object):
	"""
	Common config to all envs
	"""

	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
	"""
	Configs for development env
	"""
	SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
	"""
	Configs for production env
	"""
	DEBUG = False

class TestingConfig(Config):
	"""
	Configs for Test env
	"""
	TESTING = True


app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'testing': TestingConfig
}