import logging
from config import app
from flask import redirect, url_for, session, render_template, request
from flask_login import login_required
from parsing.parse import Parser
from .forms import ChangePasswordForm
from .database import Database

@login_required
def change_pass():
    try:
        if '_user_id' not in session:
            return redirect(url_for('login'))
        user = Database.get_user_by_id(session['_user_id'])
        username = user.username
        form = ChangePasswordForm()
        if form.is_submitted():
            old_password, password_1, password_2 = form.old_password.data, form.password_1.data, form.password_2.data
            if password_1 == password_2:
                message, success = Database.change_password(username, old_password, password_1)
                if success:
                    return redirect(url_for('view_cards'))
                return render_template('changepass.html', form=form)

        return render_template('changepass.html', form=form)



    except Exception as e:
        print(e)
        return render_template('statistics.html')