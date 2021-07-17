# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.G02.1 ($Rev: 2 $)"

import json
from flask import Flask, jsonify, request
from werkzeug import exceptions
# import api_config

app = Flask(__name__)


class ResponsesHandler(exceptions.HTTPException):

    @app.errorhandler(200)
    def response_success(self, data, msg):

        if bool(data):
            data_msg = json.loads(data)
        else:
            data_msg = data

        message = {
            'message': msg,
            'data': data_msg
        }

        resp = jsonify(message)
        status_code = 200

        return resp, status_code

    @app.errorhandler(201)
    def response_resource_created(self, data, msg):

        if bool(data):
            data_msg = json.loads(data)
        else:
            data_msg = data

        message = {
            'message': msg,
            'data': data_msg
        }

        resp = jsonify(message)
        status_code = 201

        return resp, status_code

    @app.errorhandler(400)
    def bad_request(self, msg):
        message = {
            'message': msg + request.url,
            'data': {}
        }

        resp = jsonify(message)
        status_code = 400

        return resp, status_code

    @app.errorhandler(401)
    def request_unauthorized(self, msg):
        message = {
            'message': msg + request.url,
            'data': {}
        }

        resp = jsonify(message)
        status_code = 401

        return resp, status_code

    @app.errorhandler(404)
    def request_not_found(self, msg):
        message = {
            'message': msg + request.url,
            'data': {}
        }

        resp = jsonify(message)
        status_code = 404

        return resp, status_code

    @app.errorhandler(405)
    def request_method_not_allowed(self, msg):
        message = {
            'message': msg + request.url,
            'data': {}
        }

        resp = jsonify(message)
        status_code = 405

        return resp, status_code

    @app.errorhandler(409)
    def request_conflict(self, msg):
        message = {
            'message': msg + request.url,
            'data': {}
        }

        resp = jsonify(message)
        status_code = 409

        return resp, status_code

    @app.errorhandler(500)
    def internal_server_error(self, msg):
        message = {
            'message': msg + request.url,
            'data': {}
        }

        resp = jsonify(message)
        status_code = 500

        return resp, status_code

    @app.errorhandler(503)
    def service_unavailable(self, msg):
        message = {
            'message': msg + request.url,
            'data': {}
        }

        resp = jsonify(message)
        status_code = 503

        return resp, status_code
