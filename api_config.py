# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.G02.1 ($Rev: 2 $)"

import threading
import time
from flask import Flask
from flask_jwt_extended import JWTManager
from apps.api_authentication.view_endpoints import authorization_api
from apps.bancos.view_endpoints import bancos_api
from apps.credenciales.view_endpoints import credenciales_api
from apps.vehicle.view_endpoints import inversiones_api
from apps.robot_bancario.view_endpoints import robot_api
# from db_controller.database_backend import *
from utilities.Utility import *

cfg_db = get_config_settings_db()
cfg_app = get_config_settings_app()


def create_app():
    app_api = Flask(__name__, static_url_path='/static')

    app_api.config['JWT_SECRET_KEY'] = '4p1/g4s_$v3h1cl3&#m4n4g3r%$=2021-07-16/'
    app_api.config['JWT_BLACKLIST_ENABLED'] = False
    app_api.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app_api.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
    app_api.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
    app_api.config['PROPAGATE_EXCEPTIONS'] = True

    if not 'development' == cfg_app.flask_api_env:
        app_api.config['SQLALCHEMY_DATABASE_URI'] = cfg_db.Production.SQLALCHEMY_DATABASE_URI.__str__()

    app_api.config['SQLALCHEMY_DATABASE_URI'] = cfg_db.Development.SQLALCHEMY_DATABASE_URI.__str__()

    # USER URL
    app_api.register_blueprint(authorization_api, url_prefix='/api/v1/manager/user/')

    # CREDENCIALES URL
    app_api.register_blueprint(credenciales_api, url_prefix='/api/v1/bancos/<int:IdBanco>/credenciales/')

    # INVERSIONES URL
    app_api.register_blueprint(inversiones_api, url_prefix='/api/v1/vehicle/')
    app_api.register_blueprint(inversiones_api, url_prefix='/api/v1/vehicle/flujo/datos/')

    # # ROBOT CONFIGURATION URL
    app_api.register_blueprint(robot_api, url_prefix='/api/v1/bancos/<int:IdBanco>/robot/configuraciones/')

    jwt = JWTManager(app_api)

    jwt.init_app(app_api)

    return app_api
