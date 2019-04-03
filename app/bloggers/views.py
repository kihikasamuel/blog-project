from flask import abort, flash, redirect, render_template, url_for, jsonify
from flask_login import current_user, login_required

from . import blog_user
from forms import PostForm
from .. import db
from ..models import Post

def check_status():
	if not current_user.is_approved:
		abort(403)




@blog_user.route('/', methods=['GET', 'POST'])
def view_posts():
	"""
	View all posts here
	"""
	posts = Post.query.all()

	return render_template('home/index.html', posts=posts, title="All Posts")


@blog_user.route('/posts/add', methods=['GET', 'POST'])
@login_required
def add_post():
	"""
	users will be directed to the posting page
	"""
	check_status()
	
	add_post = True
	author_id = current_user.id

	form = PostForm()

	if form.validate_on_submit():
		post = Post(
					title=form.title.data,
					post_body=form.post_body.data,
					author_id=author_id
			)
		db.session.add(post)
		db.session.commit()
		flash('This blog post has been published successfuly, but will be made public once reviewed')
		# return redirect('blog_user.add_post')

	return render_template('bloguser/posts.html', add_post=add_post, form=form, title='Posts')



# web service testing
@blog_user.route('/service/web', methods=['GET'])
def view_posts():
	"""
	View all posts here
	"""
	posts = Post.query.all()

	return jsonify('posts':{'title': title, 'body': post_body})