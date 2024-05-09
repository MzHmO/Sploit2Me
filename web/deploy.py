import logging

def deploy_web(host, port, debug):
    
    logging.debug(f"[*] Starting web server on {host}:{port} with debug mode in state:{True if debug else False}")
    pass