import os
from flask import Flask
from flask_login import LoginManager

class FileSystem:
    @staticmethod
    def getvullistpath(filename):
        current_dir = os.getcwd()
        folder_name = "files"
        filename = filename
        full_path = os.path.join(current_dir, folder_name, filename)
        return full_path


app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY", "your_secret_key_here"),
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///your_database.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


URL = "https://bdu.fstec.ru/files/documents/vullist.xlsx"
VULNLISTFILENAME = "vullist_temp.xlsx"
VULNLISTPATH = FileSystem.getvullistpath(filename=VULNLISTFILENAME)
TESTFILE = "vullist_test.xlsx"
TESTFILEPATH = FileSystem.getvullistpath(filename=TESTFILE)
