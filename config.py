import os

from flask import Flask


class FileSystem:
    @staticmethod
    def getvullistpath(filename):
        current_dir = os.getcwd()
        folder_name = "files"
        filename = filename
        full_path = os.path.join(current_dir, folder_name, filename)
        return full_path

URL = "https://bdu.fstec.ru/files/documents/vullist.xlsx"

VULNLISTFILENAME = "vullist_temp.xlsx"
VULNLISTPATH = FileSystem.getvullistpath(filename=VULNLISTFILENAME)

TESTFILE = "vullist_test.xlsx"
TESTFILEPATH = FileSystem.getvullistpath(filename=TESTFILE)

app = Flask(__name__, template_folder=os.getcwd() + '\\templates', static_folder=os.getcwd() + '\\static')
#app.secret_key = !@%#@!%$#&!@$&#$^%@!&#%@!^&#%!@
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')