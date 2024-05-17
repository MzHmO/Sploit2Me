import logging
from config import app
from flask import redirect, url_for, session, render_template, request
from flask_login import login_required
from .database import Database

@login_required
def view_cards():
    try:
        if '_user_id' not in session:
            return redirect(url_for('login'))

        user = Database.get_user_by_id(session['_user_id'])
        return render_template('cards.html', username=user.username)
    except Exception as e:
        print(e)
        return render_template('cards.html', username=user.username)