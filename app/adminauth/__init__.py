from flask import Blueprint

adminauth = Blueprint('adminauth', __name__)

from . import views