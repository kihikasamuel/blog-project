from flask import Blueprint

blog_user = Blueprint('blog_user', __name__)

from . import views