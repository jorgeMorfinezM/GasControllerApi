# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.G02.1 ($Rev: 2 $)"

from settings.settings import *
from datetime import datetime
import pytz


# Define y obtiene el configurador para las constantes generales del sistema
def get_config_settings_app():
    """
    Get the config object to charge the settings configurator.

    :return object: cfg object, contain the Match to the settings allowed in Constants file configuration.
    """

    settings_api = AppConstants()

    return settings_api


# Define y obtiene el configurador para las constantes de la base de datos
def get_config_settings_db():
    """
    Get the config object to charge the settings database configurator.

    :return object: cfg object, contain the Match to the settings allowed in Constants file configuration.
    """

    settings_db = DbConstants()

    return settings_db


# Cambia fecha-hora en datos a timezone UTC desde el dato y timezone definido
def set_utc_date_data(data_date, timezone_date):
    utc_date_convert = ""
    utc_hour_convert = ""

    date_on_utc = ""

    local_date = pytz.timezone(timezone_date)

    naive = datetime.strptime(data_date, "%Y-%m-%d %H:%M:%S")

    local_dt = local_date.localize(naive, is_dst=None)

    utc_dt = local_dt.astimezone(pytz.utc)

    print(utc_dt)

    date_on_utc = str(utc_dt).split()

    utc_date_convert = date_on_utc[0]
    utc_hour_convert = date_on_utc[1]

    return utc_date_convert, utc_hour_convert
