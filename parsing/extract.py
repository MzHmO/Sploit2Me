import pandas as pd
import logging
import requests
import config
from botnotify.tg import BotService
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from time import sleep


class HttpService:
    @staticmethod
    def download(endpoint, localpath):
        try:
            logging.debug(f"[*] Start downloading from {endpoint} to {localpath}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
            }
            response = requests.get(endpoint, verify=False, headers=headers)
            with open(localpath, 'wb') as f:
                f.write(response.content)
        
        except Exception as e:
            logging.critical(f"[-] Failed to download file from {endpoint}\n{e}")
            
class ExcelService:
    @staticmethod
    def read_xlsx(file, usecols=None, nrows=None, skiprows=None):
        headers = []
        records = []
        try:
            logging.debug(f"[*] Start reading xlsx {file}")
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

    @staticmethod
    def start(timeout, use_debug_file=False):
        while True:
            file_path = config.TESTFILEPATH if use_debug_file else config.VULNLISTPATH
            Parser.process_file(file_path)
            sleep(timeout)

    @staticmethod
    def process_file(file_path):
        if (file_path != config.TESTFILEPATH):
            HttpService.download(endpoint=config.URL, localpath=file_path)
        headers, records = ExcelService.read_xlsx(file_path, skiprows=2)

        if records:
            sorted_records = ExcelService.sort_by_column_identifier(records=records, column_id=0) # sort by column "Идентификатор"
            latest_record = sorted_records[0]
            local_latest_id = Parser.extract_numeric_value(latest_record[0])

            if local_latest_id > Parser.latest_id:
                Parser.latest_id = local_latest_id
                logging.debug(f"[*] Found new vulnerability {latest_record[0]}")
                Parser.notify(latest_record)

    @staticmethod  
    def extract_numeric_value(identifier):
        try:
            parts = identifier.split(":")[1].split("-")
            year, num = parts[0], parts[1]
            numeric_value = int(year + num)
            return numeric_value
        except (IndexError, ValueError) as e:
            logging.critical(f"Error processing identifier: {identifier}. Error: {str(e)}")
            return None

    @staticmethod
    def notify(record):
        formatted_message = f"[!] Последняя уязвимость\
                                \nИдентификатор: {record[0]},\
                                \nНаименование: {record[1]},\
                                \nОписание уязвимости {record[2]},\
                                \nВендор ПО: {record[3]},\
                                \nНазвание ПО: {record[4]},\
                                \nВерсия ПО: {record[5]},\
                                \nДата выявления: {record[9]},\
                                \nУровень опасности: {record[12]},\
                                \nСтатус уязвимости: {record[14]},\
                                \nИсточник: {record[17]}"
        logging.debug(formatted_message)
        BotService.notify(formatted_message)