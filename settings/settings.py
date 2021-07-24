# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.G04.5 ($Rev: 5 $)"

import os
from os.path import join, dirname
from dotenv import load_dotenv


class Constants:
    def __init__(self):
        # Create .env_temp file path.
        dotenv_path = join(dirname(__file__), '.env')

        # Load file from the path.
        load_dotenv(dotenv_path)

    class Development(object):
        """
        Development environment configuration
        """
        DEBUG = True
        TESTING = True
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    class Production(object):
        """
        Production environment configurations
        """
        DEBUG = False
        TESTING = False
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class AppConstants(Constants):

    log_file_apply = bool()
    log_types = list()
    log_file_extension = str()
    log_file_app_name = str()
    log_file_save_path = str()
    flask_api_debug = str()
    flask_api_env = str()
    flask_api_port = int()
    app_config = {}
    date_timezone = str()
    api_key = str()

    def __init__(self):
        super().__init__()

        app_config = {
            'development': Constants.Development,
            'production': Constants.Production,
        }

        self.log_file_apply = os.getenv('APPLY_LOG_FILE')
        self.log_types = os.getenv('LOGGER_TYPES')
        self.log_file_extension = os.getenv('FILE_LOG_EXTENSION')
        self.log_file_app_name = os.getenv('APP_FILE_LOG_NAME')
        self.log_file_save_path = os.getenv('DIRECTORY_LOG_FILES')
        self.app_config = app_config
        self.flask_api_debug = os.getenv('FLASK_DEBUG')
        self.flask_api_env = os.getenv('FLASK_ENV')
        self.flask_api_port = os.getenv('FLASK_PORT')
        self.date_timezone = os.getenv('TIMEZONE')
        self.api_key = os.getenv('API_KEY')


class DbConstants(Constants):

    gas_vehicle_table = str()          # GAS_VEHICULO
    gas_driver_table = str()           # GAS_CONDUCTOR
    gas_document_vehicle_table = str() # GAS_DOCUMENTO_VEHICULO
    gas_service_vehicle_table = str()  # GAS_SERVICIO_VEHICULO
    gas_odometer_vehicle_table = str() # GAS_ODOMETRO_VEHICULO
    gas_manager_vehicle_table = str()  # GAS_GASOLINA_VEHICULO
    gas_user_role_table = str()        # GAS_USER_ROLE

    def __init__(self):
        super().__init__()

        self.gas_vehicle_table = os.getenv('GAS_VEHICULO').__str__()
        self.gas_driver_table = os.getenv('GAS_CONDUCTOR').__str__()
        self.gas_document_vehicle_table = os.getenv('GAS_DOCUMENTO_VEHICULO').__str__()
        self.gas_service_vehicle_table = os.getenv('GAS_SERVICIO_VEHICULO').__str__()
        self.gas_odometer_vehicle_table = os.getenv('GAS_ODOMETRO_VEHICULO').__str__()
        self.gas_manager_vehicle_table = os.getenv('GAS_GASOLINA_VEHICULO').__str__()
        self.gas_user_role_table = os.getenv('GAS_USER_ROLE').__str__()

    class GasVehicle:

        vehiculo_id = int()                # VEHICULO_ID
        vehiculo_fabricante = str()        # VEHICULO_FABRICANTE
        vehiculo_modelo = str()            # VEHICULO_MODELO
        vehiculo_marca = str()             # VEHICULO_MARCA
        vehiculo_matricula = str()         # VEHICULO_MATRICULA
        vehiculo_numero_asientos = int()   # VEHICULO_NUM_ASIENTOS
        vehiculo_numero_puertas = int()    # VEHICULO_NUM_PUERTAS
        vehiculo_color = str()             # VEHICULO_COLOR
        vehiculo_anio_modelo = int()       # VEHICULO_ANIO_MODELO
        vehiculo_modelo_motor = str()      # VEHICULO_MOTOR_MODELO
        vehiculo_anio_motor = int()        # VEHICULO_MOTOR_ANIO
        vehiculo_numero_chasis = str()     # VEHICULO_NUMERO_CHASIS
        vehiculo_transmision = str()       # VEHICULO_TRANSMISION
        vehiculo_tipo_combustible = str()  # VEHICULO_TIPO_COMBUSTIBLE
        vehiculo_emisiones_co2 = float()   # VEHICULO_EMISIONES_CO2
        vehiculo_caballos_fuerza = int()   # VEHICULO_CABALLOS_FUERZA
        vehiculo_potencia = int()          # VEHICULO_POTENCIA
        vehiculo_descripcion = str()       # VEHICULO_DESCRIPCION
        vehiculo_costo_catalogo = float()  # VEHICULO_VALOR_CATALOGO
        vehiculo_costo_compra = float()    # VEHICULO_VALOR_COMPRA
        vehiculo_costo_impuesto = int()    # VEHICULO_IMPUESTO_APLICADO
        vehiculo_fecha_registro = str()    # VEHICULO_FECHA_REGISTRO
        vehiculo_fecha_baja = str()        # VEHICULO_FECHA_BAJA

        def __init__(self):

            self.vehiculo_id = os.getenv('VEHICULO_ID').__str__()
            self.vehiculo_fabricante = os.getenv('VEHICULO_FABRICANTE').__str__()
            self.vehiculo_modelo = os.getenv('VEHICULO_MODELO').__str__()
            self.vehiculo_marca = os.getenv('VEHICULO_MARCA').__str__()
            self.vehiculo_matricula = os.getenv('VEHICULO_MATRICULA').__str__()
            self.vehiculo_numero_asientos = os.getenv('VEHICULO_NUM_ASIENTOS').__str__()
            self.vehiculo_numero_puertas = os.getenv('VEHICULO_NUM_PUERTAS').__str__()
            self.vehiculo_color = os.getenv('VEHICULO_COLOR').__str__()
            self.vehiculo_anio_modelo = os.getenv('VEHICULO_ANIO_MODELO').__str__()
            self.vehiculo_modelo_motor = os.getenv('VEHICULO_MOTOR_MODELO').__str__()
            self.vehiculo_anio_motor = os.getenv('VEHICULO_MOTOR_ANIO').__str__()
            self.vehiculo_numero_chasis = os.getenv('VEHICULO_NUMERO_CHASIS').__str__()
            self.vehiculo_transmision = os.getenv('VEHICULO_TRANSMISION').__str__()
            self.vehiculo_tipo_combustible = os.getenv('VEHICULO_TIPO_COMBUSTIBLE').__str__()
            self.vehiculo_emisiones_co2 = os.getenv('VEHICULO_EMISIONES_CO2').__str__()
            self.vehiculo_caballos_fuerza = os.getenv('VEHICULO_CABALLOS_FUERZA').__str__()
            self.vehiculo_potencia = os.getenv('VEHICULO_POTENCIA').__str__()
            self.vehiculo_descripcion = os.getenv('VEHICULO_DESCRIPCION').__str__()
            self.vehiculo_costo_catalogo = os.getenv('VEHICULO_VALOR_CATALOGO').__str__()
            self.vehiculo_costo_compra = os.getenv('VEHICULO_VALOR_COMPRA').__str__()
            self.vehiculo_costo_impuesto = os.getenv('VEHICULO_IMPUESTO_APLICADO').__str__()
            self.vehiculo_fecha_registro = os.getenv('VEHICULO_FECHA_REGISTRO').__str__()
            self.vehiculo_fecha_baja = os.getenv('VEHICULO_FECHA_BAJA').__str__()

    class GasDriver:

        driver_id = int()               # CONDUCTOR_ID
        driver_name = str()             # CONDUCTOR_NOMBRE
        driver_last_name = str()        # CONDUCTOR_APELLIDO_PAT
        driver_last_name_last = str()   # CONDUCTOR_APELLIDO_MAT
        driver_address = str()          # CONDUCTOR_DOMICILIO
        driver_date_assignment = str()  # CONDUCTOR_DATE_ASSIGNMENT
        driver_status = str()           # CONDUCTOR_ESTATUS
        driver_vehicle_id = int()       # CONDUCTOR_VEHICULO_ID
        driver_role_id = int()          # CONDUCTOR_USUARIO_ROL

        def __init__(self):

            self.driver_id = os.getenv('CONDUCTOR_ID').__str__()
            self.driver_name = os.getenv('CONDUCTOR_NOMBRE').__str__()
            self.driver_last_name = os.getenv('CONDUCTOR_APELLIDO_PAT').__str__()
            self.driver_last_name_last = os.getenv('CONDUCTOR_APELLIDO_MAT').__str__()
            self.driver_address = os.getenv('CONDUCTOR_DOMICILIO').__str__()
            self.driver_date_assignment = os.getenv('CONDUCTOR_DATE_ASSIGNMENT').__str__()
            self.driver_status = os.getenv('CONDUCTOR_ESTATUS').__str__()
            self.driver_vehicle_id = os.getenv('CONDUCTOR_VEHICULO_ID').__str__()
            self.driver_role_id = os.getenv('CONDUCTOR_USUARIO_ROL').__str__()

    class GasDocument:

        document_id = int()               # DOCUMENTO_ID
        document_name = str()             # DOCUMENTO_NOMBRE
        document_start_date = str()       # DOCUMENTO_FECHA_INICIO
        document_expiration_date = str()  # DOCUMENTO_FECHA_FIN
        document_provider = str()         # DOCUMENTO_PROVEEDOR
        document_cost = float()           # DOCUMENTO_COSTO
        document_tax_rate = int()         # DOCUMENTO_COSTO_IMPUESTO
        document_frecuency_date = str()   # DOCUMENTO_FECHA_FRECUENCIA
        document_status = str()           # DOCUMENTO_ESTATUS
        document_file = bytes()           # DOCUMENTO_ARCHIVO
        document_driver_id = int()        # DOCUMENTO_CONDUCTOR_ID
        document_vehicle_id = int()       # DOCUMENTO_VEHICULO_ID

        def __init__(self):

            self.document_id = os.getenv('DOCUMENTO_ID').__str__()
            self.document_name = os.getenv('DOCUMENTO_NOMBRE').__str__()
            self.document_start_date = os.getenv('DOCUMENTO_FECHA_INICIO').__str__()
            self.document_expiration_date = os.getenv('DOCUMENTO_FECHA_FIN').__str__()
            self.document_provider = os.getenv('DOCUMENTO_PROVEEDOR').__str__()
            self.document_cost = os.getenv('DOCUMENTO_COSTO').__str__()
            self.document_tax_rate = os.getenv('DOCUMENTO_COSTO_IMPUESTO').__str__()
            self.document_frecuency_date = os.getenv('DOCUMENTO_FECHA_FRECUENCIA').__str__()
            self.document_status = os.getenv('DOCUMENTO_ESTATUS').__str__()
            self.document_file = os.getenv('DOCUMENTO_ARCHIVO').__str__()
            self.document_driver_id = os.getenv('DOCUMENTO_CONDUCTOR_ID').__str__()
            self.document_vehicle_id = os.getenv('DOCUMENTO_VEHICULO_ID').__str__()

    class GasService:

        service_id = int()           # SERVICIO_ID
        service_name = str()         # SERVICIO_NOMBRE
        service_description = str()  # SERVICIO_DESCRIPCION
        service_start_date = str()   # SERVICIO_FECHA_INICIO
        service_end_date = str()     # SERVICIO_FECHA_FIN
        service_type = str()         # SERVICIO_TIPO
        service_provider = str()     # SERVICIO_PROVEEDOR
        service_notes = str()        # SERVICIO_NOTAS
        service_cost = float()       # SERVICIO_COSTO
        service_tax_rate = int()     # SERVICIO_COSTO_IMPUESTO
        service_status = str()       # SERVICIO_ESTATUS
        service_driver_id = int()    # SERVICIO_CONDUCTOR_ID
        service_vehicle_id = int()   # SERVICIO_VEHICULO_ID

        def __init__(self):

            self.service_id = os.getenv('SERVICIO_ID').__str__()
            self.service_name = os.getenv('SERVICIO_NOMBRE').__str__()
            self.service_description = os.getenv('SERVICIO_DESCRIPCION').__str__()
            self.service_start_date = os.getenv('SERVICIO_FECHA_INICIO').__str__()
            self.service_end_date = os.getenv('SERVICIO_FECHA_FIN').__str__()
            self.service_type = os.getenv('SERVICIO_TIPO').__str__()
            self.service_provider = os.getenv('SERVICIO_PROVEEDOR').__str__()
            self.service_notes = os.getenv('SERVICIO_NOTAS').__str__()
            self.service_cost = os.getenv('SERVICIO_COSTO').__str__()
            self.service_tax_rate = os.getenv('SERVICIO_COSTO_IMPUESTO').__str__()
            self.service_status = os.getenv('SERVICIO_ESTATUS').__str__()
            self.service_driver_id = os.getenv('SERVICIO_CONDUCTOR_ID').__str__()
            self.service_vehicle_id = os.getenv('SERVICIO_VEHICULO_ID').__str__()

    class GasOdometer:

        odometer_id = int()             # ODOMETRO_ID
        odometer_register_date = str()  # ODOMETRO_FECHA_REGISTRO
        odometer_value = str()          # ODOMETRO_VALOR
        odometer_unit_mesure = str()    # ODOMETRO_UNIDAD_MEDIDA
        odometer_driver_id = int()      # ODOMETRO_CONDUCTOR_ID
        odometer_vehicle_id = int()     # ODOMETRO_VEHICULO_ID

        def __init__(self):

            self.odometer_id = os.getenv('ODOMETRO_ID').__str__()
            self.odometer_register_date = os.getenv('ODOMETRO_FECHA_REGISTRO').__str__()
            self.odometer_value = os.getenv('ODOMETRO_VALOR').__str__()
            self.odometer_unit_mesure = os.getenv('ODOMETRO_UNIDAD_MEDIDA').__str__()
            self.odometer_driver_id = os.getenv('ODOMETRO_CONDUCTOR_ID').__str__()
            self.odometer_vehicle_id = os.getenv('ODOMETRO_VEHICULO_ID').__str__()

    class GasManager:

        gas_registro_id = int()           # GASOLINA_REGISTRO_ID
        gas_registro_date = str()         # GASOLINA_REGISTRO_FECHA
        gas_registro_hour = str()         # GASOLINA_REGISTRO_HORA
        gas_registro_liters = float()     # GASOLINA_REGISTRO_LITROS
        gas_registro_cost = float()       # GASOLINA_REGISTRO_COSTO
        gas_registro_tax_rate = int()     # GASOLINA_REGISTRO_IMPUESTO
        gas_registro_unit_cost = float()  # GASOLINA_REGISTRO_UNIT_COST
        gas_gasolinera_name = str()       # GASOLINA_NOMBRE_GASOLINERA
        gas_gasolinera_address = str()    # GASOLINA_UBICACION_GASOLINERA
        gas_driver_id = int()             # GASOLINA_CONDUCTOR_ID
        gas_vehicle_id = int()            # GASOLINA_VEHICULO_ID
        gas_document_id = int()           # GASSOLINA_DOCUMENTO_ID

        def __init__(self):

            self.gas_registro_id = os.getenv('GASOLINA_REGISTRO_ID').__str__()
            self.gas_registro_date = os.getenv('GASOLINA_REGISTRO_FECHA').__str__()
            self.gas_registro_hour = os.getenv('GASOLINA_REGISTRO_HORA').__str__()
            self.gas_registro_liters = os.getenv('GASOLINA_REGISTRO_LITROS').__str__()
            self.gas_registro_cost = os.getenv('GASOLINA_REGISTRO_COSTO').__str__()
            self.gas_registro_tax_rate = os.getenv('GASOLINA_REGISTRO_IMPUESTO').__str__()
            self.gas_registro_unit_cost = os.getenv('GASOLINA_REGISTRO_UNIT_COST').__str__()
            self.gas_gasolinera_name = os.getenv('GASOLINA_NOMBRE_GASOLINERA').__str__()
            self.gas_gasolinera_address = os.getenv('GASOLINA_UBICACION_GASOLINERA').__str__()
            self.gas_driver_id = os.getenv('GASOLINA_CONDUCTOR_ID').__str__()
            self.gas_vehicle_id = os.getenv('GASOLINA_VEHICULO_ID').__str__()
            self.gas_document_id = os.getenv('GASSOLINA_DOCUMENTO_ID').__str__()

    class UserRole:

        user_role_id = int()      # ROL_USUARIO_ID
        user_role_name = str()    # ROL_USUARIO_NOMBRE
        user_role_status = str()  # ROL_USUARIO_ESTATUS

        def __init__(self):
            self.user_role_id = os.getenv('ROL_USUARIO_ID').__str__()
            self.user_role_name = os.getenv('ROL_USUARIO_NOMBRE').__str__()
            self.user_role_status = os.getenv('ROL_USUARIO_ESTATUS').__str__()
