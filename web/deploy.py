import logging


class WebServer:
    @staticmethod
    def start(host, port, debug):
        logging.warn(f"[*] Starting web server on {host}:{port} with debug mode in state:{True if debug else False}")
        