# -*- coding: utf-8 -*-
"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ """
__version__ = "1.1.A19.1 ($Rev: 1 $)"

from apps.api_authentication.UsersAuthModel import UsersAuthModel
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from logger_controller.logger_control import *
from db_controller.database_backend import *
# import uuid
# from handler_controller.ResponsesHandler import ResponsesHandler
# from handler_controller.messages.ErrorMsg import *
# from handler_controller.messages.SuccessMsg import *


cfg_app = get_config_settings_app()
logger_type = 'ws'
log = configure_logger(logger_type)


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hash_passwd):
    return sha256.verify(password, hash_passwd)


def user_registration(session, data):
    user_process_reponse = None
    response_login = None

    password_hash = generate_hash(data.get('password'))

    try:

        if verify_hash(data.get('password'), password_hash):

            access_token = create_access_token(identity=data.get('username'))

            refresh_token = create_refresh_token(identity=data.get('username'))

            # id_user = uuid.uuid1()

            user_process_reponse = UsersAuthModel(data).manage_user_authentication(session, data)

            # UsersAuth.manage_user_authentication('', user_name, user_password, password_hash)

            log.info('User inserted/updated in database: %s',
                     ' User_Name: "{}", Password_Hash: "{}" '.format(data.get('username'),
                                                                     password_hash))
            response_login = json.dumps({
                'message_login': 'Logged in as {}'.format(data.get('username')),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'data': user_process_reponse
            })

        else:
            response_login = json.dumps({'message_login': 'Wrong credentials'})

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                data.get('username'), 'user_auth', 'user_auth', error
            )
        )

    return response_login
