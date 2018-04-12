"""
Creates a Flask app instance and registers the database object
"""

from flask import Flask
from remembrallapi.api import api
from remembrallapi.models import db


def create_app(app_name="REMEMBRALL_API"):
    app = Flask(app_name)
    app.config.from_object("remembrallapi.config.BaseConfig")

    app.register_blueprint(api, url_prefix="/api")
    db.init_app(app)

    return app
