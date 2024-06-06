import logging
from config import app
from flask import redirect, url_for, session, render_template, request
from flask_login import login_required
from .database import Database

@login_required
def view_telegram():
    try:
        if '_user_id' not in session:
            return redirect(url_for('login'))
        
        user = Database.get_user_by_id(session['_user_id'])
        
        if request.method == "POST":
            telegram_login = request.form.get("telegram_login")
            filter_value = request.form.get("filter_value")
            logging.warn(f"[+] New telegram account {telegram_login} with filter {filter_value}")
            Database.apply_tg_filter(username=telegram_login.lower(), filter_value=filter_value.lower())

        return render_template('telegram.html', username=user.username)
    except Exception as e:
        print(e)
        return render_template('telegram.html', username=user.username)