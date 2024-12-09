import click
from flask import Flask
from flask_login import LoginManager

from app.extensions import db
from app.models import User


def init_utils(app: Flask):
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.cli.command('create-admin')
    @click.argument('username')
    @click.argument('password')
    @click.option('--role', default='admin', help='Role of the user: admin or user')
    def create_admin(username, password, role):
        if User.query.filter_by(username=username).first():
            print(f'Пользователь с именем {username} уже существует!')
            return
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f'Админ с именем {username} успешно создан с ролью {role}.')
