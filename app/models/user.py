from sqlalchemy.orm import relationship

from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    commission_rate = db.Column(db.Float, nullable=False, default=0.0)
    webhook_url = db.Column(db.String(255), nullable=True)

    transactions = relationship('Transaction', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id} - Balance: {self.balance}>"
