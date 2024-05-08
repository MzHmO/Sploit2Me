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
from web.deploy import deploy_web
from parsing.extract import Parse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    add_help=True,
                    description=
                        "Sploit2Me - a project for notification of users about new vulnerabilities that appear on the \"БДУ ФСТЭК\"")
    parser.add_argument("-debug", action="store_true", help='Turn Debug output ON')
    parser.add_argument("-port", action="store", help="From 1 to 65536 port value on which web server will be started", default=80)
    parser.add_argument("-host", action="store", help="IP of network interface on which deploy web app on", default="127.0.0.1")

    options = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

    deploy_web(host=options.host, port=options.port, debug=options.debug)
    Parse.start()