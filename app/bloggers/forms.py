from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from ..models import Post

class PostForm(FlaskForm):
	"""
	Bloggers whose account is active will add blog posts here
	"""
	title = StringField('Title', validators=[DataRequired()])
	post_body = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Publish')