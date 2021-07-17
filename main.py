# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.G02.1 ($Rev: 2 $)"

import api_config
from utilities.Utility import *
# from db_controller.database_backend import *
from logger_controller.logger_control import *


cfg_db = get_config_settings_db()
cfg_app = get_config_settings_app()


if __name__ == '__main__':

    app = api_config.create_app()

    logger_type = 'api'

    # Can contains the next values: ['development', 'production']
    app_constants = cfg_app.app_config.get('development')

    if cfg_app.log_file_apply:
        logger = configure_logger(logger_type)
    else:
        logger = configure_console_logger(logger_type)

    port = cfg_app.flask_api_port

    app.debug = app_constants.DEBUG

    app.run(host='127.0.0.1', port=port)
