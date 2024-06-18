import logging
from config import app
from flask import redirect, url_for, session, render_template, request
from flask_login import login_required
from parsing.parse import Parser
from .database import Database

@login_required
def view_cards():
    try:
        if '_user_id' not in session:
            return redirect(url_for('login'))

        user = Database.get_user_by_id(session['_user_id'])

        page = request.args.get('page', 1, type=int)
        per_page = 12

        all_cards = Parser.get_card_vuln()
        
        filter_value = request.form.get('filter_value')
        
        if filter_value:
            filter_value = filter_value.lower()
            all_cards = [
                card for card in all_cards 
                if any(filter_value in str(record_value).lower() for i, record_value in enumerate(card['all']) if i != 17)
            ]

        total_cards = len(all_cards)
        total_pages = (total_cards + per_page - 1) // per_page

        start = (page - 1) * per_page
        end = start + per_page

        cards = all_cards[start:end]

        if page > total_pages or page < 1:
            return render_template('cards.html', username=user.username, cards=[], total_pages=total_pages, current_page=1)

        return render_template('cards.html', username=user.username, cards=cards, total_pages=total_pages, current_page=page)
    except Exception as e:
        print(e)
        return render_template('cards.html', username=user.username, cards=[], total_pages=1, current_page=1)
