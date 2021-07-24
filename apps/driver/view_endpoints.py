# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.G02.1 ($Rev: 2 $)"

from flask import Blueprint, json, request
# from flask_jwt_extended import jwt_required
from db_controller.database_backend import *
from .DriverModel import DriverModel
from handler_controller.ResponsesHandler import ResponsesHandler as HandlerResponse
from handler_controller.messages import SuccessMsg, ErrorMsg
from logger_controller.logger_control import *
from utilities.Utility import *
from datetime import datetime

cfg_app = get_config_settings_app()
driver_api = Blueprint('driver_api', __name__)
# jwt = JWTManager(bancos_api)
logger = configure_logger('ws')


@driver_api.route('/', methods=['POST', 'PUT', 'GET', 'DELETE'])
# @jwt_required
def endpoint_manage_driver_data():
    conn_db, session_db = init_db_connection()

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return HandlerResponse.request_unauthorized(ErrorMsg.ERROR_REQUEST_UNAUTHORIZED, auth)
    else:

        if request.method == 'POST':

            data = request.get_json(force=True)

            driver_model = DriverModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Driver to Manage on DB: %s', str(data))

            driver_response = driver_model.insert_data(session_db, data)

            logger.info('Data Driver to Register on DB: %s', str(data))

            if not driver_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, driver_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_CREATED_RECORD, driver_response)

        elif request.method == 'GET':
            data = dict()
            drivers_on_db = None

            driver_model = DriverModel(data)

            drivers_on_db = driver_model.get_all_drivers(session_db)

            if not bool(drivers_on_db) or not drivers_on_db or "[]" == drivers_on_db:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, drivers_on_db)

            return HandlerResponse.response_success(SuccessMsg.MSG_GET_RECORD, drivers_on_db)

        elif request.method == 'PUT':

            data = request.get_json(force=True)

            driver_model = DriverModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Driver to Manage on DB: %s', str(data))

            driver_response = driver_model.update_data(session_db, data)

            logger.info('Data Driver to Update on DB: %s', str(data))

            if not driver_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, driver_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_UPDATED_RECORD, driver_response)

        elif request.method == 'DELETE':

            data = request.get_json(force=True)

            driver_model = DriverModel(data)

            if not data or str(data) is None:
                return HandlerResponse.request_conflict(ErrorMsg.ERROR_REQUEST_DATA_CONFLICT, data)

            logger.info('Data Json Driver to Manage on DB: %s', str(data))

            driver_response = driver_model.update_data(session_db, data)

            logger.info('Data Driver to Update on DB: %s', str(data))

            if not driver_response:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, driver_response)

            return HandlerResponse.response_resource_created(SuccessMsg.MSG_DELETED_RECORD, driver_response)

        else:
            return HandlerResponse.request_not_found(ErrorMsg.ERROR_METHOD_NOT_ALLOWED)


@driver_api.route('/filter', methods=['GET'])
def get_looking_for_driver():
    conn_db, session_db = init_db_connection()

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return HandlerResponse.request_unauthorized(ErrorMsg.ERROR_REQUEST_UNAUTHORIZED, auth)
    else:
        data = dict()

        query_string = request.query_string.decode('utf-8')

        if request.method == 'GET':
            # To GET ALL Data of the Driver:

            driver_on_db = None

            filter_spec = []

            if 'nombre_conductor' in query_string:
                driver_name = request.args.get('nombre_conductor')

                data['nombre_conductor'] = driver_name

                # filter_spec.append({'field': 'driver_name', 'op': '==', 'value': driver_name})
                filter_spec.append({'field': 'driver_name', 'op': 'ilike', 'value': driver_name})

            if 'fecha_registro' in query_string:
                fecha_registro = request.args.get('fecha_registro')

                fecha_filter = datetime.strptime(str(fecha_registro), "%Y-%m-%d")

                data['fecha_registro'] = fecha_filter

                filter_spec.append({'field': 'driver_registered', 'op': '==', 'value': fecha_filter})

            if 'estatus_conductor' in query_string:
                driver_status = request.args.get('estatus_conductor')

                data['estatus_conductor'] = driver_status

                filter_spec.append({'field': 'driver_status', 'op': 'ilike', 'value': driver_status})

            if 'vehiculo_fabricante' in query_string:
                vehicle_manufacturer = request.args.get('vehiculo_fabricante')

                data['vehiculo_fabricante'] = vehicle_manufacturer

            driver_model = DriverModel(data)

            driver_on_db = driver_model.get_driver_by_filters(session_db, data, filter_spec)

            if not bool(driver_on_db) or not driver_on_db or "[]" == driver_on_db:
                return HandlerResponse.response_success(ErrorMsg.ERROR_DATA_NOT_FOUND, driver_on_db)

            return HandlerResponse.response_success(SuccessMsg.MSG_GET_RECORD, driver_on_db)

        else:
            return HandlerResponse.request_not_found(ErrorMsg.ERROR_METHOD_NOT_ALLOWED)
