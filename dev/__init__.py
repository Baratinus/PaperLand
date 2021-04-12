import os
from flask import Flask

from .views import app
from . import db

db.init_app(app)