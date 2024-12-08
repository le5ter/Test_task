from .flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from . import api # noqa


def init_app(app):
    for extension in (db, api):
        extension.init_app(app)

    with app.app_context():
        from app.models import User, Transaction # noqa
        db.create_all()
