import os

class FileSystem:
    @staticmethod
    def getvullistpath(filename):
        current_dir = os.getcwd() 
        folder_name = "files"
        filename = filename
        full_path = os.path.join(current_dir, folder_name, filename)
        return full_path

URL = "https://bdu.fstec.ru/files/documents/vullist.xlsx"
TELEGRAM_TOKEN = "7136918933:AAE1cRDDMMsFs5IBTcBU9AtIDQk51mgOVoc"

VULNLISTFILENAME = "vullist_temp.xlsx"
VULNLISTPATH = FileSystem.getvullistpath(filename=VULNLISTFILENAME)

TESTFILE = "vullist_test.xlsx"
TESTFILEPATH = FileSystem.getvullistpath(filename=TESTFILE)