from flask import Flask

from config import Config
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from . import extensions
    extensions.init_app(app)

    from . import modules
    modules.init_app(app)

    return app
