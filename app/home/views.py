from __future__ import print_function
from flask import abort, render_template, jsonify
from flask_login import login_required, current_user

import africastalking

from . import home

# ============================================================
@home.route('/')
def call():
	username = "sandbox"
	api_key = ""

	africastalking.initialize(username,api_key)
	voice = africastalking.Voice

	call_from = "+254719166938"
	call_to = ["+254710701117"]

	try:
		# make call
		voice.call(call_from,call_to)
		print(result)
	except Exception as e:
		print ("Encountered an error while making the call:%s" %str(e))



# =============================================================
# @home.route('/')
# def homepage():
# 	"""
# 	template to be rendered
# 	"""
# 	return render_template('home/index.html', title='Welcome')

@home.route('/dashboard')
@login_required
def dashboard():
	"""
	template to render
	"""
	return render_template('home/index.html', title='Dashboard')

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
	if not current_user.is_admin:
		abort(403)

	return render_template('home/admin_dashboard.html', title='Admin Dashboard')
