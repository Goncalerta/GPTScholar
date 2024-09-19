import logging

log = logging.getLogger("GPTscholar")

class Logger:
    def __init__(self):
        pass

    def info(self, message):
        log.info(message)

    def warn(self, message):
        log.warn(message)

    def error(self, message):
        log.error(message)
    
    def debug(self, message):
        log.debug(message)
