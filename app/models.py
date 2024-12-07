from datetime import datetime, timezone
from sqlalchemy import Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True)
    balance = mapped_column(Float, nullable=False, default=0.0)
    commission_rate = mapped_column(Float, nullable=False, default=0.0)  # Ставка комиссии (например, в процентах)
    webhook_url = mapped_column(String(255), nullable=True)

    transactions = relationship('Transaction', backref='user', lazy=True)  # Связь с транзакциями

    def __repr__(self):
        return f"<User {self.id} - Balance: {self.balance}>"


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = mapped_column(Integer, primary_key=True)
    amount = mapped_column(Float, nullable=False)  # Сумма транзакции
    commission = mapped_column(Float, nullable=False)  # Комиссия за транзакцию
    status = mapped_column(String(20), nullable=False, default='waiting')  # Статус транзакции
    created_at = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Transaction {self.id} - Status: {self.status}>"
