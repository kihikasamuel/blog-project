# third party imports
from flask 				import Flask
from flask_bootstrap	import Bootstrap
from flask_sqlalchemy 	import SQLAlchemy
from flask_login 		import LoginManager
from flask_migrate		import Migrate

# import from local files
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()

# create app
def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')


	Bootstrap(app)
	db.init_app(app)

	# init login_manager, set login_manager message and set loginpath
	login_manager.init_app(app)
	login_manager.login_message = "You must be logged in to access this resource."
	login_manager.login_view = "auth.login"


	migrate = Migrate(app, db)

	from app import models

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	# from .bloggers import blog_user as user_blueprint
	# app.register_blueprint(user_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	return app