# -*- coding: utf-8 -*-

"""
netease-dl.logger
~~~~~~~~~~~~~~~~

This module provides a logger.
"""
import os
import logging

from .config import conf_dir, log_path


if not os.path.isdir(conf_dir):
    os.mkdir(conf_dir)


with open(log_path, 'a+') as f:
    f.write('#' * 80)
    f.write('\n')


def get_logger(name):
    """Return a logger with a file handler."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # File output handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(name)12s %(levelname)8s %(lineno)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
