import unittest
from flask_testing import TestCase
import os
from flask import abort, url_for

from app import create_app, db
from app.models import Blogger, Post, Role


class TestBase(TestCase):


	def create_app(self):

		config_name = 'testing'
		app = create_app(config_name)
		app.config.update(
					SQLALCHEMY_DATABASE_URI = 'mysql://test_admin:CzolB8GG#12@localhost/test_db'
			)
		return app


	def setUp(self):
		"""
		Runs before every test
		"""

		db.create_all()


		# create admin
		admin = Blogger(username='tester', password_hash='tester@admin', is_admin=True)

		# create a blogger
		blogger = Blogger(username='test_user1', password_hash='1234567',)


		db.session.add(admin)
		db.session.add(blogger)
		db.session.commit()

	def tearDown(self):
		"""
		Runs after every test
		"""

		db.session.remove()
		db.drop_all()


class TestModels(TestBase):
	"""
	Test the models
	"""

	def test_blogger_model(self):
		"""
		chech the no of bloggers registered
		"""
		self.assertEqual(Blogger.query.count(), 2)

	def test_role_model(self):
		"""
		Create a test role and check no of 
		posts available
		"""
		role = Role(name='GM', description='General Manager incharge of Editorial')

		db.session.add(role)
		db.session.commit()
		
		self.assertEqual(Role.query.count(), 1)


	def test_post_model(self):
		"""
		add and check no of posts
		"""
		post = Post(title='My Time', post_body='Hello Iam Iam Iam')

		db.session.add(post)
		db.session.commit()

		self.assertEqual(Post.query.count(), 1)


class TestView(TestBase):
	"""
	Test the views for redirect and behaviour on auth
	"""

	def test_homepage_view(self):

		response = self.client.get(url_for('home.homepage'))
		self.assertEqual(response.status_code, 200)

	def test_login_view(self):

		response = self.client.get(url_for('auth.login'))
		self.assertEqual(response.status_code, 200)

	def test_dashboard_view(self):

		target_url = url_for('home.dashboard')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)

	def test_logout_view(self):

		target_url = url_for('auth.logout')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)


if __name__ == '__main__':
	unittest.main()