# third party imports
import os
from flask 				import Flask, render_template
from flask_bootstrap	import Bootstrap
from flask_sqlalchemy 	import SQLAlchemy
from flask_login 		import LoginManager
from flask_migrate		import Migrate
# from flask_json import FlaskJSON, JsonError, json_response, as_json
# import africastalking

# import from local files
from config import app_config

db = SQLAlchemy()

login_manager = LoginManager()

# africas = africastalking()

# create app
def create_app(config_name):

	if os.getenv('FLASK_ENV') == "production":
		app = Flask(__name__)
		app.config.update(
				SECRET_KEY=os.getenv('SECRET_KEY'),
				SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
			)
	else:
		app = Flask(__name__, instance_relative_config=True)
		app.config.from_object(config['production'])
		app.config.from_pyfile('config.py')


	Bootstrap(app)
	db.init_app(app)
	# FlaskJSON(app)


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

	from .bloggers import blog_user as user_blueprint
	app.register_blueprint(user_blueprint)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	@app.errorhandler(403)
	def error_403_forbidden(error):
		return render_template('errors/403.html', title='Forbidden'), 403

	@app.errorhandler(404)
	def error_404_not_found(error):
		return render_template('errors/404.html', title='Not Found'), 404

	app.errorhandler(500)
	def error_500_server_err(error):
		return render_template('errors/500.html', title='Server Error'), 500

	return app