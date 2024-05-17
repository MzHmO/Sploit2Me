import logging
from config import app
from flask import redirect, url_for, session, render_template, request, make_response
from flask_login import login_required
import matplotlib.pyplot as plt
import io
from collections import Counter
from .database import Database
from parsing.parse import Parser

@login_required
def plot_png_route():
    
    #labels = ['Система 1', 'Система 2', 'Система 3', 'Система 4']
    #sizes = [30, 20, 25, 25]
    
    systems = Parser.getsystems()
    systems_counter = Counter(systems)
    labels = list(systems_counter.keys())
    sizes = list(systems_counter.values())
    colors = plt.cm.tab20.colors

    fig, ax = plt.subplots()
    
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=200)
    ax.axis('equal')
    plt.title('Наиболее уязвимое ПО')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return make_response(img.read())

@login_required
def view_stats():
    try:
        if '_user_id' not in session:
            return redirect(url_for('login'))
        user = Database.get_user_by_id(session['_user_id'])
        return render_template('statistics.html', username=user.username)
    except Exception as e:
        print(e)
        return render_template('statistics.html', username=user.username)