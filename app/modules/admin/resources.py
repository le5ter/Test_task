from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from app.models import User


def init_routes(app: Flask):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))

        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username']).first()
            if user and check_password_hash(user.password, request.form['password']):
                login_user(user)
                return redirect(url_for('admin.index'))
            else:
                flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))
