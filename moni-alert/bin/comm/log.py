#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

CRITICAL = 1
ERROR    = 2
WARNING  = 3
INFO     = 4
DEBUG    = 5


class Logger:

    def __init__(self, fileName, level=DEBUG):
        dictLevel = {
            CRITICAL: logging.CRITICAL,
            ERROR:    logging.ERROR,
            WARNING:  logging.WARNING,
            INFO:     logging.INFO,
            DEBUG:    logging.DEBUG
        }
        if level < CRITICAL or level > DEBUG:
            level = DEBUG
        logLevel = dictLevel[level]
        # mkdir
        abspath = os.path.abspath(fileName)
        dir = os.path.dirname(abspath)
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.logger = logging.getLogger(dir)
        self.logger.setLevel(logLevel)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        # 控制台日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(logLevel)
        # 文件日志
        fh = logging.handlers.RotatingFileHandler(fileName, maxBytes=50*1024*1024, backupCount=20)
        fh.setFormatter(fmt)
        fh.setLevel(logLevel)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == "__main__":
    logger = Logger('test.log', INFO)
    logger.debug('this is a debug message')
    logger.info('this is a info message')
    logger.warn('this is a warn message')

