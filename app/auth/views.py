from flask import flash, render_template, redirect, url_for
from flask_login import login_required,login_user, logout_user, current_user

from . import auth
from .forms import RegistrationForm, LoginForm
from .. import db
from ..models import Blogger

@auth.route('/register', methods=['GET', 'POST'])
def register():
	"""
	Handle request made to registration route
	Add user from the registration forms
	"""

	form = RegistrationForm()
	if form.validate_on_submit():
		blogger = Blogger(
							email=form.email.data,
							username=form.username.data,
							password=form.password.data
					)

		# add data to db
		db.session.add(blogger)
		db.session.commit()
		# on succcess
		flash('You have registered successfully!Redirecting to login.')

		return redirect(url_for('auth.login'))

	# always show registration form when on this route
	return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Handle login requests
	"""
	form = LoginForm()
	if form.validate_on_submit():
		blogger = Blogger.query.filter_by(email=form.email.data).first()

		if blogger is not None and blogger.verify_password(form.password.data):
			# login user and redirect
			login_user(blogger)

			if current_user.is_admin:
				return redirect(url_for('home.admin_dashboard'))
			else:
				return redirect(url_for('home.dashboard'))

			flash('You are now logged in as' + str(current_user.username))

		else:
			flash('Invalid user name or password!')
	# always show login form on this route
	return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
	"""
	When user clicks the button
	their session is clossed
	"""
	logout_user()
	flash('You have successfully logged out')

	return redirect(url_for('auth.login'))