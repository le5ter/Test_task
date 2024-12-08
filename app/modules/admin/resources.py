from datetime import date
from sqlalchemy import func
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView

from app.extensions import db
from app.models import User, Transaction
from .forms import TransactionForm


class DashboardView(BaseView):
    @expose('/')
    def index(self):
        users_count = db.session.query(func.count(User.id)).scalar()
        transactions_count = db.session.query(func.count(Transaction.id)).scalar()
        total_sum = (
                db.session.query(func.sum(Transaction.amount))
                .filter(func.date(Transaction.created_at) == date.today())
                .scalar()
                or 0
        )
        recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(10).all()

        return self.render(
            'admin/dashboard.html',
            users_count=users_count,
            transactions_count=transactions_count,
            total_sum=total_sum,
            recent_transactions=recent_transactions,
        )


class UserAdmin(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ('id', 'balance', 'commission_rate', 'webhook_url', 'transactions')
    form_columns = ('balance', 'commission_rate', 'webhook_url')
    column_searchable_list = ('id', 'webhook_url')


class TransactionAdmin(ModelView):
    can_create = False
    can_edit = True
    can_delete = False
    column_list = ('id', 'amount', 'commission', 'status', 'created_at', 'user')
    column_filters = ('status', 'created_at')
    form_columns = ('status',)

    form = TransactionForm

    def on_form_prefill(self, form, id): # noqa
        transaction = Transaction.query.get(id)
        if transaction and transaction.status != 'waiting':
            raise ValueError("Статус может быть изменен только для транзакции в статусе 'waiting'.")
