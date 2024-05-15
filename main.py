# ------------------------------------------------------
#   Link2Work Project Start File
#   Urfu Project Digital Portfolio
# ------------------------------------------------------
#  
# Description:
# Entrypoint file to run project
#
#
# Author:
#   Team «Мы»


import logging
import argparse
import threading
from web.deploy import WebServer
from parsing.parse import Parser
from botnotify.tg import BotService
from web.database import Database


def start_web_server(options):
    WebServer.start(host=options.host, port=options.port, debug=options.debug)


def start_bot_service(options):
    BotService.start(bot_token=options.token)


def start_parser(options):
    Parser.start(timeout=5, use_debug_file=options.testfile)

def start_db():
    Database.setup_db()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        add_help=True,
        description=
        "Sploit2Me - a project for notification of users about new vulnerabilities that appear on the \"БДУ ФСТЭК\"")
    parser.add_argument("-debug", action="store_true", help='Turn Debug output ON', default=False)
    parser.add_argument("-warn", action="store_true", help="Turn WARN output ON", default=False)
    parser.add_argument("-testfile", action="store_true", help="Use test file for getting information about vulns",
                        default=False)
    parser.add_argument("-host", action="store", help="IP of network interface on which deploy web app on",
                        default="127.0.0.1")
    parser.add_argument("-token", action="store", help="Telegram bot token for sending messages to user's", default="")
    parser.add_argument("-port", action="store", help="From 1 to 65536 port value on which web server will be started",
                        default=8000)

    options = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    elif options.warn:
        logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

    database_thread = threading.Thread(target=start_db)
    web_server_thread = threading.Thread(target=start_web_server, args=(options,))
    bot_service_thread = threading.Thread(target=start_bot_service, args=(options,))
    parser_thread = threading.Thread(target=start_parser, args=(options,))
    database_thread.start()
    web_server_thread.start()
    bot_service_thread.start()
    parser_thread.start()

    database_thread.join()
    web_server_thread.join()
    bot_service_thread.join()
    parser_thread.join()