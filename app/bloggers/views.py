from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import blog_user
from .. import db
from forms import PostForm
from ..models import Post

def check_status():
	if not current_user.is_approved:
		abort(403)



@blog_user.route('/blogger/post/', methods=['GET', 'POST'])
@login_required()
def add_post():
	"""
	users will be directed to the posting page
	"""
	check_status()

	post = Post.query.all()

	form = PostForm()
	if form.validate_on_submit():
		post = Post(
					title=form.title.data,
					post_body=form.post_body.data
					author_id=form.author_id.data
			)
		db.session.add(post)
		db.session.commit()
		flash('This blog post has been published successfuly, but will be made public once reviewed')

		return redirect('')
		anything 