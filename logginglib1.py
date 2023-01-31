"""Custom logging"""
import logging
import sys
import configparser
from datetime import datetime


class Log:
    """My castom logger class"""
    def __init__(self, config_file, log_lvl):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.formatter = logging.Formatter("%(asctime)s [%(name)s | %(levelname)s] %(message)s")
        if log_lvl == "DEBUG":
            date = datetime.now()
            start_id = date.strftime("%Y%m%d-%H%M%S")
            self.log_file = start_id + '-' + log_lvl + '-' + self.config.get('Logging', 'logfile')
        else:
            self.log_file = self.config.get('Logging', 'logfile')
        self.log_level = log_lvl

    def get_console_handler(self):
        """Console handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self):
        """File handler"""
        file_handler = logging.FileHandler(self.log_file, mode='a',
                        encoding='utf-8', delay=False, errors=None)
        file_handler.setFormatter(self.formatter)
        return file_handler

    def get_logger(self, logger_name):
        """Create logger"""
        logger = logging.getLogger(logger_name)
        logger.setLevel(self.log_level) # лучше иметь больше логов, чем их нехватку
        if not logger.handlers:
            logger.addHandler(self.get_console_handler())
            logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger
