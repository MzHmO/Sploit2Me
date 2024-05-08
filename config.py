import os

class FileSystem:
    @staticmethod
    def getvullistpath():
        current_dir = os.getcwd() 
        folder_name = "files"
        filename = VULNLISTFILENAME
        full_path = os.path.join(current_dir, folder_name, filename)
        return full_path

URL = "https://bdu.fstec.ru/files/documents/vullist.xlsx"
TELEGRAM_TOKEN = "AABBCCDD"

VULNLISTFILENAME = "vullist_temp.xlsx"
VULNLISTPATH = FileSystem.getvullistpath()