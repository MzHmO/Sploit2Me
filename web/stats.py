import logging
from config import app
from flask import redirect, url_for, session, render_template, request, make_response
from flask_login import login_required
import matplotlib.pyplot as plt
import io
import difflib
import time
from collections import Counter
from .database import Database
from parsing.parse import Parser

plt.switch_backend('Agg')

@login_required
def plot_bar_route():
    systems = Parser.getsystems()    

    def find_closest_label(label, labels, threshold=0.8):
        for existing_label in labels:
            similarity = difflib.SequenceMatcher(None, label, existing_label).ratio()
            if similarity >= threshold:
                return existing_label
        return label

    systems_counter = Counter(systems)
    similar_name_groups = {}

    for label, size in systems_counter.items():
        closest_label = find_closest_label(label, similar_name_groups.keys())
        if closest_label in similar_name_groups:
            similar_name_groups[closest_label] += size
        else:
            similar_name_groups[closest_label] = size

    labels = list(similar_name_groups.keys())
    sizes = list(similar_name_groups.values())

    total = sum(sizes)
    percentages = [(size / total) * 100 for size in sizes]
    sorted_data = sorted(zip(labels, sizes, percentages), key=lambda x: -x[2])

    other_size = 0
    other_percentage = 0
    filtered_labels = []
    filtered_sizes = []

    for label, size, perc in sorted_data:
        if perc < 1:
            other_size += size
            other_percentage += perc
        else:
            filtered_labels.append(label)
            filtered_sizes.append(size)

    if other_size > 0:
        filtered_labels.append('Другие')
        filtered_sizes.append(other_size)

    bar_chart_img = io.BytesIO()
    fig, ax = plt.subplots()
    ax.bar(filtered_labels, filtered_sizes, color='skyblue')
    plt.title('Количество уязвимостей по ПО')
    plt.xlabel('ПО')
    plt.ylabel('Количество уязвимостей')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(bar_chart_img, format='png', dpi=150)
    bar_chart_img.seek(0)
    
    response = make_response(bar_chart_img.getvalue())
    response.mimetype = 'image/png'
    return response

@login_required
def plot_png_route():
    time.sleep(0.75)
    systems = Parser.getsystems()

    def find_closest_label(label, labels, threshold=0.8):
        for existing_label in labels:
            similarity = difflib.SequenceMatcher(None, label, existing_label).ratio()
            if similarity >= threshold:
                return existing_label
        return label

    systems_counter = Counter(systems)
    similar_name_groups = {}

    for label, size in systems_counter.items():
        closest_label = find_closest_label(label, similar_name_groups.keys())
        if closest_label in similar_name_groups:
            similar_name_groups[closest_label] += size
        else:
            similar_name_groups[closest_label] = size

    labels = list(similar_name_groups.keys())
    sizes = list(similar_name_groups.values())

    total = sum(sizes)
    percentages = [(size / total) * 100 for size in sizes]
    sorted_data = sorted(zip(labels, sizes, percentages), key=lambda x: -x[2])

    other_size = 0
    other_percentage = 0
    filtered_labels = []
    filtered_sizes = []

    for label, size, perc in sorted_data:
        if perc < 1.8:
            other_size += size
            other_percentage += perc
        else:
            filtered_labels.append(label)
            filtered_sizes.append(size)

    if other_size > 0:
        filtered_labels.append('Другие')
        filtered_sizes.append(other_size)

    pie_chart_img = io.BytesIO()
    fig, ax = plt.subplots()
    ax.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Наиболее уязвимое ПО')
    plt.savefig(pie_chart_img, format='png', dpi=150)
    pie_chart_img.seek(0)
    
    response = make_response(pie_chart_img.getvalue())
    response.mimetype = 'image/png'
    return response


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