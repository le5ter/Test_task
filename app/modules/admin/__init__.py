from flask_admin import Admin

from app.extensions import db
from app.models import User, Transaction
from . import views
from .resources import init_routes
from .utils import init_utils


def init_app(app):
    admin = Admin(app, name='Админка', template_mode='bootstrap4', index_view=views.MyAdminIndexView())
    admin._menu = admin._menu[1:]

    admin.add_view(views.DashboardView(name='Дашборд', endpoint='dashboard'))
    admin.add_view(views.UserModelView(User, db.session, name='Пользователи'))
    admin.add_view(views.TransactionModelView(Transaction, db.session, name='Транзакции'))

    init_routes(app)
    init_utils(app)
