from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email


from ..models import Blogger


class RegistrationForm(FlaskForm):
	"""
	Registration form fields
	"""

	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')
	submit = SubmitField('Register')


	def validate_email(self, field):
		if Blogger.query.filter_by(email=field.data).first():
			raise ValidationError('This email is already registered!')


	def validate_username(self, field):
		if Blogger.query.filter_by(username=field.data).first():
			raise ValidationError('This username is already in use!')



class LoginForm(FlaskForm):
	"""
	Users log in here
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')