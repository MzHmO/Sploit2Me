# ------------------------------------------------------
#   Link2Work Project Start File
#   Urfu Project Digital Portfolio
# ------------------------------------------------------
#  
# Description:
#   File with logic for extracting information from
#   the "БДУ ФСТЭК" information resource
#
#
# Author:
#   Team «Мы»


import requests
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pandas as pd
import logging
from time import sleep
import config


class Http:
    @staticmethod
    def download(endpoint):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
            }
            response = requests.get(endpoint, verify=False, headers=headers)
            with open(config.VULNLISTPATH, 'wb') as f:
                f.write(response.content)
        
        except Exception as e:
            logging.critical(f"[-] Failed to download file from {endpoint}\n{e}")
            
class Excel:
    @staticmethod
    def read_xlsx(file, usecols=None, nrows=None):
        try:
            df = pd.read_excel(file, usecols=usecols, nrows=nrows)
            header = df.columns.tolist()
            records = df.values.tolist()
            return header, records
        except Exception as e:
            logging.critical(f"[-] Failed to read xlsx file {file}\n{e}")


    @staticmethod
    def sort_by_column_identifier(records, id):
        return sorted(records, key=lambda x: x[id], reverse=True)


class Parse:
    @staticmethod
    def start(timeout=5):
        logging.debug(f"[*] Started parsing using {timeout} seconds timeout")

        while True:
            Http.download(config.URL)
            Excel.read_xlsx(config.VULNLISTPATH)
