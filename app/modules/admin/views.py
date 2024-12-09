from datetime import date

from sqlalchemy import func
from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from app.extensions import db
from app.models import User, Transaction
from .forms import TransactionForm, CreateUserForm, EditUserForm


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class SecureDashboardView(BaseView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin():
            return redirect(url_for('index'))  # Перенаправляем на главную страницу
        return self.render('admin/dashboard.html')


class DashboardView(SecureDashboardView):
    @expose('/')
    def index(self):
        if not current_user.is_admin():
            return redirect(url_for('index'))  # Ограничиваем доступ для обычных пользователей

        user_count = db.session.query(func.count(User.id)).scalar()
        transaction_count = db.session.query(func.count(Transaction.id)).scalar()
        today_transactions = (
                db.session.query(func.sum(Transaction.amount))
                .filter(func.date(Transaction.created_at) == date.today())
                .scalar() or 0.0
        )

        recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(10).all()

        return self.render(
            'admin/dashboard.html',
            user_count=user_count,
            transaction_count=transaction_count,
            today_transactions=today_transactions,
            recent_transactions=recent_transactions
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def is_visible(self):
        return current_user.is_authenticated and current_user.is_admin()


class UserModelView(SecureModelView):
    column_list = ('id', 'username', 'balance', 'commission_rate', 'webhook_url', 'transactions')
    column_searchable_list = ('id', 'webhook_url')

    def get_create_form(self):
        return CreateUserForm

    def get_edit_form(self):
        return EditUserForm

    def on_model_change(self, form, model, is_created):
        if form.password.data and is_created:
            model.set_password(form.password.data)

        if not model.role:
            model.role = 'user'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()


class TransactionModelView(SecureModelView):
    column_list = ('id', 'amount', 'commission', 'status', 'created_at', 'user_id')
    column_filters = ('status', 'created_at', 'user_id')
    form_columns = ('status',)
    form = TransactionForm

    def is_accessible(self):
        return current_user.is_authenticated

    def get_query(self):
        if not current_user.is_admin():
            return super().get_query().filter(Transaction.user_id == current_user.id)
        return super().get_query()

    def get_count_query(self):
        if not current_user.is_admin():
            return super().get_count_query().filter(Transaction.user_id == current_user.id)
        return super().get_count_query()

    def on_form_prefill(self, form, id): # noqa
        transaction = Transaction.query.get(id)
        if transaction and transaction.status != 'waiting':
            raise ValueError("Статус может быть изменен только для транзакции в статусе 'waiting'.")

    def on_model_change(self, form, model, is_created):
        if not current_user.is_admin():
            raise PermissionError("Вы не можете создавать или изменять записи")
        return super().on_model_change(form, model, is_created)

    def on_model_delete(self, model):
        if not current_user.is_admin():
            raise PermissionError("Вы не можете удалять записи")
        return super().on_model_delete(model)
