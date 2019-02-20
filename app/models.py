"""metadata"""
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Blogger(UserMixin, db.Model):
	"""
	Create bloggers table
	1 blogger can have many posts
	"""

	__tablename__ = 'bloggers'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	is_admin = db.Column(db.Boolean, default=False)
	is_approved = db.Column(db.Boolean, default=False)
	posts = db.relationship('Post', backref='blogger', lazy='dynamic')

	@property
	def password(self):
		"""
		Set to private
		"""
		raise AttributeError('password is not readable')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)


	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

		
	def __repr__(self):
		"""
		Wrap username to blogger
		"""
		return "<Blogger: {}>".format(self.username)


# set how users are to be loaded
@login_manager.user_loader
def load_user(user_id):
	return Blogger.query.get(int(user_id))


class Post(db.Model):
	"""
	Create posts table
	"""
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), unique=True)
	post_body = db.Column(db.Text)
	created_on = db.Column(db.DateTime(timezone=True), default=func.now())
	author_id = db.Column(db.Integer, db.ForeignKey('bloggers.id'))

	def __repr__(self):
		"""
		Wrap posts title
		"""
		return '<Post: {}>'.format(self.title)



class Role(db.Model):
	"""
	Create roles table
	1 role can have many bloggers
	"""
	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))
	bloggers = db.relationship('Blogger', backref='blogger', lazy='dynamic')

	def __repr__(self):
		"""
		Wrap role name to Role
		"""
		return '<Role: {}>'.format(self.name)