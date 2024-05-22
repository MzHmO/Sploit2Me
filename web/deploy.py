import logging
from . import forms
from .database import Database
from .cards import view_cards
from .stats import view_stats, plot_png_route
from .telegram import view_telegram
from .profile import view_profile
from .changepass import view_changepass
from flask import Flask, url_for, redirect, request, render_template, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user


# DEPLOY CONFIG
from config import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# EXTERNAL ROUTES
app.add_url_rule('/cards', methods=['GET', 'POST'], view_func=view_cards)
app.add_url_rule('/telegram', methods=['GET', 'POST'], view_func=view_telegram)
app.add_url_rule('/stats', methods=['GET', 'POST'], view_func=view_stats)
app.add_url_rule('/profile', methods=['GET', 'POST'], view_func=view_profile)
app.add_url_rule('/changepass', methods=['GET', 'POST'], view_func=view_changepass)
app.add_url_rule('/plot.png', methods=['GET'], view_func=plot_png_route)

# INTERNAL ROUTES
@login_manager.user_loader
def load_user(user_id):
    return Database.get_user_by_id(user_id=user_id)


@app.route('/')
def home():
     if current_user.is_authenticated:
         return redirect(url_for('view_cards'))
     return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.is_submitted():
        username, password = form.username.data, form.password.data
        if Database.validate_login_by_username(username, password):
            user = Database.get_user_by_username(username)
            login_user(user)
            return redirect(url_for('view_cards'))
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

class WebServer:
    @staticmethod
    def start(host, port, debug):
        logging.warn(f"[*] Starting Web on {host}:{port} with debug mode in {debug}")
        app.run(host=host, port=port, debug=debug)
        