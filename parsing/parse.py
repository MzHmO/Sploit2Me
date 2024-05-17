import pandas as pd
import logging
import requests
import config
from random import choice
from botnotify.tg import BotService, async_notify
from time import sleep
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HttpService:
    @staticmethod
    def download(endpoint, localpath):
        try:
            logging.warn(f"[*] Start downloading from {endpoint} to {localpath}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
            }
            response = requests.get(endpoint, verify=False, headers=headers)
            with open(localpath, 'wb') as f:
                f.write(response.content)
        
        except Exception as e:
            logging.warn(f"[-] Failed to download file from {endpoint}\n{e}")
            
class ExcelService:
    @staticmethod
    def read_xlsx(file, usecols=None, nrows=None, skiprows=None):
        headers = []
        records = []
        try:
            logging.warn(f"[*] Start reading xlsx {file}")
            df = pd.read_excel(file, usecols=usecols, nrows=nrows, skiprows=skiprows)
            headers = df.columns.tolist()
            records = df.values.tolist()
        except Exception as e:
            logging.critical(f"[-] Failed to read xlsx file {file}\n{e}")
        return headers,records

    @staticmethod
    def sort_by_column_identifier(records, column_id):
        return sorted(records, key=lambda x: x[column_id], reverse=True)


class Parser:
    latest_id = 0
    headers = []
    records = []
    sorted_records = []

    @staticmethod
    def getsystems():
        while (len(Parser.records) == 0):
            sleep(5)
        column_index = 4 # Название ПО
        return [record[column_index].split(' ')[0] for record in Parser.records]

    @staticmethod
    def start(timeout, use_debug_file=False):
        while True:
            file_path = config.TESTFILEPATH if use_debug_file else config.VULNLISTPATH
            Parser.headers, Parser.records = Parser.get_bdu(file_path=file_path)
            
            if use_debug_file:
                record = Parser.find_new_vuln(records=Parser.records, column=choice([i for i in range(0,10) if i not in [7]])) # simulate new vulns
            else:
                record = Parser.find_new_vuln(records=Parser.records, column=0) # sort by column "Идентификатор"
            if (record != ""):
                Parser.notify(record)
            sleep(int(timeout))

    @staticmethod
    def get_bdu(file_path):
        if (file_path != config.TESTFILEPATH):
            HttpService.download(endpoint=config.URL, localpath=file_path)
        return ExcelService.read_xlsx(file_path, skiprows=2)        


    @staticmethod
    def find_new_vuln(records, column):
        Parser.sorted_records = ExcelService.sort_by_column_identifier(records=records, column_id=column)
        latest_record = Parser.sorted_records[0]
        local_latest_id = Parser.extract_numeric_value(latest_record[0])

        if local_latest_id > Parser.latest_id:
            #Parser.latest_id = local_latest_id # UNCOMMENT IT IN PROD
            logging.warn(f"[*] Found new vulnerability {latest_record[0]}")
            return latest_record
        return ""
            
    @staticmethod  
    def extract_numeric_value(identifier):
        try:
            parts = identifier.split(":")[1].split("-")
            year, num = parts[0], parts[1]
            numeric_value = int(year + num)
            return numeric_value
        except (IndexError, ValueError) as e:
            logging.warn(f"[*] Error processing identifier: {identifier}. Error: {str(e)}")
            return None

    @staticmethod
    def notify(record):
        formatted_message = (
        "❗️❗️❗️Последняя уязвимость❗️❗️❗️\n\n"
            f"🪪 Идентификатор: {record[0]},\n\n"
            f"🏷 Наименование: {record[1]},\n\n"
            f"📋 Описание уязвимости: {record[2]},\n\n"
            f"- Вендор ПО: {record[3]},\n\n"
            f"- Название ПО: {record[4]},\n\n"
            f"- Версия ПО: {record[5]},\n\n"
            f"📆 Дата выявления: {record[9]},\n\n"
            f"📊 Уровень опасности: {record[12]},\n\n"
            f"✅ Статус уязвимости: {record[14]},\n\n"
            f"📬 Источник: {record[17]}"
        )
        # logging.warn(formatted_message)
        async_notify(formatted_message)
