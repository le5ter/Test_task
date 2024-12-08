from flask_admin import Admin

from app.extensions import db
from app.models import User, Transaction
from . import resources


def init_app(app):
    admin = Admin(app, name='Админка', template_mode='bootstrap4')
    admin._menu = admin._menu[1:]

    admin.add_view(resources.DashboardView(name='Дашборд', endpoint='dashboard'))
    admin.add_view(resources.UserAdmin(User, db.session, name='Пользователи'))
    admin.add_view(resources.TransactionAdmin(Transaction, db.session, endpoint="transaction", name='Транзакции'))
