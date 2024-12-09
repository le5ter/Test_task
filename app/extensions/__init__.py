from .flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from . import api, celery # noqa

from flask_migrate import Migrate # noqa
migrate = Migrate()


def init_app(app):
    for extension in (db, api, celery):
        extension.init_app(app)

    with app.app_context():
        from app.models import User, Transaction # noqa
        db.create_all()

    migrate.init_app(app, db)
