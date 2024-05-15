import logging
from . import forms
from .database import Database
from flask import Flask, url_for, redirect, request, render_template, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

# DEPLOY CONFIG
from config import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# EXTERNAL ROUTES
# app.add_url_rule('/files', methods=['GET', 'POST'], view_func=file_handling)
# app.add_url_rule('/download/<filename>', view_func=download_file)
# app.add_url_rule('/delete/<filename>', methods=['GET', 'POST'], view_func=delete_file)


# INTERNAL ROUTES
@login_manager.user_loader
def load_user(user_id):
    return Database.get_user_by_id(user_id=user_id)


@app.route('/')
def home():
     if current_user.is_authenticated:
         return redirect(url_for('file_handling'))
     return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.is_submitted():
        username, password = form.username.data, form.password.data
        if Database.validate_login_by_username(username, password):
            user = Database.get_user_by_username(username)
            login_user(user)
            return redirect(url_for('file_handling'))
        else:
            flash('Неверное имя пользователя или пароль')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''

    form = forms.RegistrationForm()
    if form.is_submitted():
        username, email, password_1, password_2 = form.username.data, form.email.data, form.password_1.data, form.password_2.data
        if password_1 == password_2:
            message, success = Database.register_user(username, password_1, email)
            if success:
                return redirect(url_for('login'))
            else:
                error = message
        else:
            error = "Пароли не совпадают"

    return render_template('register.html', form=form, error=error)


# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#     profile = {
#         "name": "Имя",
#         "surname": "Фамилия",
#         "otchestvo": "Отчество",
#
#     }
#     return render_template('profile.html', profile=profile)
#
#
# @app.route('/change_password', methods=['GET', 'POST'])
# def change_password():
#     error = ''
#     username = current_user.username
#     form = forms.ChangePasswordForm()
#     if form.is_submitted():
#         old_password, password_1, password_2 = form.old_password.data, form.password_1.data, form.password_2.data
#         if password_1 == password_2:
#             message, success = Database.change_password(username, old_password, password_1)
#             if success:
#                 return redirect(url_for('profile'))
#             else:
#                 error = message
#         else:
#             error = "Пароли не совпадают"
#
#     return render_template('change_password.html', form=form, error=error)


class WebServer:
    @staticmethod
    def start(host, port, debug):
        logging.warn(f"[*] Starting Web on {host}:{port} with debug mode in {debug}")
        app.run(host=host, port=port, debug=debug)
        