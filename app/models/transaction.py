from sqlalchemy import ForeignKey
from datetime import datetime, timezone

from app.extensions import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='waiting')
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired')
    ]

    def __repr__(self):
        return f"<Transaction {self.id} - Status: {self.status}>"
