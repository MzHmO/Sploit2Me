import os
from flask import redirect, send_from_directory, url_for, session, render_template, request
from flask_login import login_required
from werkzeug.utils import secure_filename
from backend.database import Database
from config import app

@login_required
def file_handling():
    try:
        if '_user_id' not in session:
            return redirect(url_for('login'))

        user = Database.get_user_by_id(session['_user_id'])
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user.id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                extension = filename.split('.')[-1].lower()
                allowed_extensions = ["png", "jpg", "jpeg", "txt", "mkv"]
                if extension in allowed_extensions:
                    if len(filename) > 15:
                        filename = filename[:15] + '.' + extension
                    file.save(os.path.join(user_folder, filename))
                    size = round(os.path.getsize(os.path.join(user_folder, filename)) / 1024 ** 2, 2)
                    if size > 100:
                        os.remove(os.path.join(user_folder, filename))
                        return render_template('files.html', files=[], username=user.username, error="Файл не должен превышать 100MB.")
                    return redirect(url_for('file_handling'))
                else:
                    error_message = "Допускаются только файлы с расширениями: " + ', '.join(allowed_extensions) + "."
                    return render_template('files.html', files=[], username=user.username, error=error_message)
        
        elif request.method == 'GET':
            files = [f for f in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, f))]
            return render_template('files.html', files=files, username=user.username)
    except Exception as e:
        print(e)
        return render_template('files.html', files=[], username=user.username, error=str(e))


        
@login_required
def download_file(filename):
    return send_from_directory(str(app.config['UPLOAD_FOLDER'] + "\\" + session['_user_id']),filename, as_attachment=True)

@login_required
def delete_file(filename):
    path = app.config['UPLOAD_FOLDER'] + "\\" + session['_user_id']
    os.remove(os.path.join(path, filename))
    return redirect(url_for('file_handling'))