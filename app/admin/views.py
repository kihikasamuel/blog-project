from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import AssignBloggersForm, BloggerStatusForm, PostForm, RoleForm
from .. import db
from ..models import Blogger, Post, Role

def check_role():
	if not current_user.is_admin:
		abort(403)

"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
								Post Views
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

@admin.route('/posts', methods=['GET', 'POST'])
@login_required
def show_posts():
	"""
	View all posts from here.
	"""
	check_role()

	#view all
	posts = Post.query.all()

	return render_template('admin/posts/posts.html', posts=posts, title="Blog Posts")

@admin.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_posts(id):
	"""
	Edit posts for errors
	"""
	check_role()

	add_posts = False
	posts = Post.query.get_or_404(id)
	form = PostForm(obj=posts)
	if form.validate_on_submit():
		posts.title = form.title.data
		posts.post_body = form.post_body.data

		db.session.commit()
		flash('Post updated')

		return redirect(url_for('admin.show_posts'))


	return render_template('admin/posts/post.html', action='Edit', add_posts=add_posts, form=form, posts=posts, title='Edit Posts')

@admin.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_posts(id):
	"""
	Delete posts
	"""
	check_role()

	posts = Post.query.get_or_404(id)
	db.session.delete(posts)
	db.session.commit()
	flash('You deleted one post')

	return redirect(url_for('admin.show_posts'))

	return render_template(title='Delete Post')
"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
								Role Views
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

@admin.route('/roles/', methods=['GET', "POST"])
@login_required
def list_roles():
	"""
	Check privilege
	List all roles
	"""

	check_role()

	roles= Role.query.all()
	
	return render_template('admin/roles/roles.html', roles=roles, title='Roles')

"""
"""
@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_roles():
	"""
	"""
	check_role()

	add_roles = True

	form = RoleForm()
	if form.validate_on_submit():
		role = Role(
						name=form.name.data,
						description=form.description.data
			)

		try:
			db.session.add(role)
			db.session.commit()
			flash('Role added successfully!')
		except:
			flash('Error: Role name already exist!')

		return redirect(url_for('admin.list_roles'))

	return render_template('admin/roles/role.html', action='Add', add_roles=add_roles, form=form, title='Add Roles')


""""""
@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_roles(id):
	"""
	"""
	check_role()

	add_roles = False

	role = Role.query.get_or_404(id)
	form = RoleForm(obj=role)

	if form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data

		db.session.commit()
		flash("You have edited role successfully")
		return redirect(url_for('admin.list_roles'))

	return render_template('admin/roles/role.html', action='Edit', add_roles=add_roles, form=form, title='Edit Roles')


""""""
@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_roles(id):
	"""
	"""
	check_role()

	role = Role.query.get_or_404(id)
	db.session.delete(role)
	db.session.commit()
	flash('One role has been removed from list')

	return redirect(url_for('admin.list_roles'))

	return render_template(title='Delete Roles')


"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
								Blogger Views
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
@admin.route('/bloggers', methods=['GET', 'POST'])
@login_required
def view_bloggers():
	"""
	views all registered bloggers
	"""
	check_role()

	bloggers = Blogger.query.all()

	return render_template('admin/bloggers/bloggers.html', bloggers = bloggers, title="Bloggers")

""""""
@admin.route('/bloggers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blogger(id):
	"""
	activate/deactivate blogger
	"""
	check_role()
	
	blogger = Blogger.query.get_or_404(id)
	form = BloggerStatusForm(obj=blogger)

	if form.validate_on_submit():
		blogger.is_approved = form.is_approved.data

		db.session.commit()
		flash('Status Changed successfully')

		return redirect(url_for('admin.view_bloggers'))

	""""""
	return render_template('admin/bloggers/blogger.html', form=form, blogger=blogger, title="Edit Blogger")


@admin.route('/blogger/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blogger(id):
	"""
	Remove blogger
	"""
	check_role()

	blogger = Blogger.query.get_or_404(id)
	db.session.delete(blogger)
	db.session.commit()
	flash('Deleted successfully')
	return redirect(url_for('admin.view_bloggers'))

	return render_template(title='Delete Blogger')


# give roles to bloggers
@admin.route('/bloggers/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_roles(id):
	"""
	Assign a role
	"""
	check_role()

	blogger = Blogger.query.get_or_404(id)

	# Do not assign roles to Admin
	if blogger.is_admin:
		abort(403)

	#
	form = AssignBloggersForm(obj=blogger)
	if form.validate_on_submit():
		blogger.role = form.role.data
		db.session.add(blogger)
		db.session.commit()
		
		flash('Assigned role to %s' % str(blogger.username))
		return redirect(url_for('admin.view_bloggers'))

	return render_template('admin/bloggers/assignRole.html', form=form, blogger=blogger, title='Assign Roles')
