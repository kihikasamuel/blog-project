from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Blogger, Role

class PostForm(FlaskForm):
	"""
	Forms for editing, deleting and updtaing posts
	"""
	title = StringField('Title', validators=[DataRequired()])
	post_body = TextField('Body', validators=[DataRequired()])
	submit = SubmitField('Publish')


class RoleForm(FlaskForm):
	"""
	Forms for adding, editing, assigning and deleting roles
	"""
	name = StringField('Role', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Add')



class BloggerStatusForm(FlaskForm):
	"""
	view, edit, delete, and deactivate bloggers
	""" 
	is_approved = BooleanField('Status')
	submit = SubmitField('Commit Change')



class AssignBloggersForm(FlaskForm):
	"""
	Assign roles to bloggers
	"""
	role = QuerySelectField(query_factory=lambda:Role.query.all(), get_label='name')
	submit = SubmitField('Assign Role')