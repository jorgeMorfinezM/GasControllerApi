# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

import errno
import logging
import os
import sys
from utilities.Utility import *
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Possible values to LOGGER: DEBUG, INFO, WARN, ERROR, and CRITICAL
# LOG_LEVEL = logging.DEBUG


# Para LOG file de App principal
def configure_logging(log_name, path_to_log_directory, logger_type):
    """
    Configure logger

    :param logger_type: The type to write logger and setup on the modules of App
    :param log_name: Name of the log file saved
    :param path_to_log_directory: Path to directory to write log file in
    :return:
    """

    cfg = get_config_settings_app()

    _date_name = datetime.now().strftime('%Y-%m-%dT%H%M')
    log_filename = str(log_name + _date_name + cfg.log_file_extension)

    _importer_logger = logging.getLogger(logger_type)
    _importer_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - Module: %(module)s - Line No: %(lineno)s : %(name)s : %(levelname)s - '
                                  '%(message)s')
    if not os.path.exists(path_to_log_directory):
        fh = logging.FileHandler(filename=os.path.join(path_to_log_directory, log_filename), mode='a',
                                 encoding='utf-8', delay=False)
    else:
        fh = logging.FileHandler(filename=os.path.join(path_to_log_directory, log_filename), mode='w',
                                 encoding='utf-8', delay=False)

    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    _importer_logger.addHandler(fh)

    # For Testing logging - Comment
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    _importer_logger.addHandler(sh)

    create_directory_if_not_exists(_importer_logger, path_to_log_directory)

    return _importer_logger


# Para LOG console de App principal
def configure_logging_console(logger_type):
    """
    Configure logger

    :param logger_type: The type to write logger and setup on the modules of App
    :return _imoporter_log:
    """

    _date_name = datetime.now().strftime('%Y-%m-%dT%H%M')

    _importer_logger = logging.getLogger(logger_type)
    _importer_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - Module: %(module)s - Line No: %(lineno)s : %(name)s : %(levelname)s - '
                                  '%(message)s')

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    _importer_logger.addHandler(sh)

    return _importer_logger


def log_critical_error(logger, exc, message):
    """
    Logs the exception at ´CRITICAL´ log level

    :param logger: the logger
    :param exc:     exception to log
    :param message: description message to log details of where/why exc occurred
    """
    if logger is not None:
        logger.critical(message)
        logger.critical(exc)


def create_directory_if_not_exists(logger, path):
    """
    Creates 'path' if it does not exist
    If creation fails, an exception will be thrown
    :param logger: the logger
    :param path: the path to ensure it exists
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST and not os.path.isdir(path):
            log_critical_error(logger, exc, 'An error happened trying to create ' + path)
            raise


def configure_logger(logger_type):
    """
    Declare and validate existence of log directory; create and configure logger object

    :return: instance of configured logger object
    """

    cfg = get_config_settings_app()

    log_name = cfg.log_file_app_name
    log_dir = cfg.log_file_save_path

    logger = configure_logging(log_name, log_dir, logger_type)

    if logger is not None:
        return logger


def configure_console_logger(logger_type):
    """
    Declare and validate existence of log directory; create and configure logger object

    :param logger_type: The type to write logger and setup on the modules of App
    :return: instance of configured logger object
    """

    logger = configure_logging_console(logger_type)

    if logger is not None:
        return logger

