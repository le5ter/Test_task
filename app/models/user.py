from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    commission_rate = db.Column(db.Float, nullable=False, default=0.0)
    webhook_url = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=True)  # должно быть поле username
    password = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), nullable=True, default='user')  # 'admin', 'user'

    transactions = relationship('Transaction', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id} - Balance: {self.balance}>"

    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
