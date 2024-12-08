from .flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def init_app(app):
    # for extension in (...):
    #     extension.init_app(app)

    db.init_app(app)
    with app.app_context():
        from app.models import User, Transaction # noqa
        db.create_all()
