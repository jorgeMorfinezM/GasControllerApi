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
import logging
from datetime import datetime

import psycopg2
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.engine.reflection import Inspector

from db_controller import mvc_exceptions as mvc_exc
from logger_controller.logger_control import *
from utilities.Utility import *

from flask_bcrypt import Bcrypt

Base = declarative_base()
bcrypt = Bcrypt()

cfg_db = get_config_settings_db()
cfg_app = get_config_settings_app()

# logger = configure_logger(cfg_app.log_types[2].__str__())
logger = configure_logger('db')

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def create_engine_db():

    # For Test connection:

    engine = create_engine(cfg_db.Development.SQLALCHEMY_DATABASE_URI.__str__(),
                           client_encoding="utf8",
                           execution_options={"isolation_level": "REPEATABLE READ"})

    if not 'development' == cfg_app.flask_api_env:
        engine = create_engine(cfg_db.Production.SQLALCHEMY_DATABASE_URI.__str__(),
                               client_encoding="utf8",
                               execution_options={"isolation_level": "REPEATABLE READ"})

    logger.info("Engine Created by URL: {}".format(cfg_db.Development.SQLALCHEMY_DATABASE_URI.__str__()))

    return engine


def create_database_api(engine_session):

    if not database_exists(engine_session.url):
        logger.info("Create the Database...")
        create_database(engine_session.url, 'utf-8')

    logger.info("Database created...")


def create_bd_objects(engine_obj):
    inspector = Inspector.from_engine(engine_obj)

    table_names = list()

    table_names.append(cfg_db.gas_driver_table.__str__())
    table_names.append(cfg_db.gas_manager_vehicle_table.__str__())
    table_names.append(cfg_db.gas_vehicle_table.__str__())
    table_names.append(cfg_db.gas_odometer_vehicle_table.__str__())
    table_names.append(cfg_db.gas_document_vehicle_table.__str__())
    table_names.append(cfg_db.gas_service_vehicle_table.__str__())

    if not inspector.get_table_names():
        Base.metadata.create_all(bind=engine_obj)
        logger.info("Database objects created...")
    else:

        for table_name in inspector.get_table_names():

            logger.info('Table on database: %s', str(table_name))

            if table_name in table_names:

                logger.info('Table already created: %s', str(table_name))
            else:
                # Create tables
                Base.metadata.create_all(bind=engine_obj)

                logger.info("Database objects created...")

    # Base.metadata.create_all(bind=engine_obj)

    logger.info("Database objects created...")


def session_to_db(engine_se):
    r"""
    Get and manage the session connect to the database engine.

    :return connection: Object to connect to the database and transact on it.
    """

    session = None

    connection = None

    try:

        if engine_se:

            session_maker = sessionmaker(bind=engine_se, autocommit=True)

            connection = engine_se.connect()

            session = session_maker(bind=connection)

            logger.info("Connection and Session objects created...")

        else:
            logger.error("Database not created or some parameters with the connection to the database can't be read")

    except mvc_exc.DatabaseError as db_error:
        logger.exception("Can not connect to database, verify data connection", db_error, exc_info=True)
        raise mvc_exc.ConnectionError(
            'Can not connect to database, verify data connection.\nOriginal Exception raised: {}'.format(db_error)
        )

    return connection, session


def init_db_connection():
    engine_db = create_engine_db()

    create_database_api(engine_db)

    create_bd_objects(engine_db)

    connection, session = session_to_db(engine_db)

    return connection, session


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return "".join(k for k in input_string if k.isalnum())


def create_cursor(conn):
    r"""
    Create an object statement to transact to the database and manage his data.

    :param conn: Object to connect to the database.
    :return cursor: Object statement to transact to the database with the connection.

    """
    try:
        cursor = conn.cursor()

    except mvc_exc.ConnectionError as conn_error:
        logger.exception("Can not create the cursor object, verify database connection", conn_error, exc_info=True)
        raise mvc_exc.ConnectionError(
            'Can not connect to database, verify data connection.\nOriginal Exception raised: {}'.format(
                conn_error
            )
        )

    return cursor


def disconnect_from_db(conn):
    r"""
    Generate close session to the database through the disconnection of the conn object.

    :param conn: Object connector to close session.
    """

    if conn is not None:
        conn.close()


def close_cursor(cursor):
    r"""
    Generate close statement to the database through the disconnection of the cursor object.

    :param cursor: Object cursor to close statement.
    """

    if cursor is not None:
        cursor.close()


def get_current_date(session):
    # sql_current_date = 'SELECT CURDATE()'  # For MySQL
    sql_current_date = 'SELECT NOW()'  # For PostgreSQL

    current_date = session.execute(sql_current_date).one()

    logger.info('CurrentDate: %s', current_date)

    return current_date


def get_systimestamp_date(session):
    last_updated_date_column = session.execute('SELECT systimestamp from dual').scalar()

    logger.info('Timestamp from DUAL: %s', last_updated_date_column)

    return last_updated_date_column


def get_current_date_from_db(session, conn, cursor):
    r"""
    Get the current date and hour from the database server to set to the row registered or updated.

    :return last_updated_date: The current day with hour to set the date value.
    """

    last_updated_date = None

    try:

        # sql_current_date = 'SELECT CURDATE()'  # For MySQL
        sql_current_date = 'SELECT NOW()'  # For PostgreSQL

        cursor.execute(sql_current_date)

        result = cursor.fetchone()[0]

        print("NOW() :", result)

        if result is not None:
            # last_updated_date = datetime.datetime.strptime(str(result), "%Y-%m-%d %H:%M:%S")
            # last_updated_date = datetime.datetime.strptime(str(result), "%Y-%m-%d %I:%M:%S")
            last_updated_date = result

        cursor.close()

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database.".format(error)
        )
    finally:
        disconnect_from_db(conn)

    return last_updated_date


'''
class UsersAuth(Base):
    r"""
    Class to instance User data to authenticate the API.
    Transactions:
     - Insert: Add user_role data to the database if not exists.
     - Update: Update user_role data on the database if exists.
    """

    cfg_db = get_config_constant_file()

    __tablename__ = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    user_id = Column(cfg['DB_AUTH_COLUMNS_DATA']['USER_AUTH']['USER_ID'], Numeric, primary_key=True)
    user_name = Column(cfg['DB_AUTH_COLUMNS_DATA']['USER_AUTH']['USER_NAME'], String, primary_key=True)
    user_password = Column(cfg['DB_AUTH_COLUMNS_DATA']['USER_AUTH']['USER_PASSWORD'], String)
    password_hash = Column(cfg['DB_AUTH_COLUMNS_DATA']['USER_AUTH']['PASSWORD_HASH'], String)
    last_update_date = Column(cfg['DB_AUTH_COLUMNS_DATA']['USER_AUTH']['LAST_UPDATE_DATE'], String)

    @staticmethod
    def manage_user_authentication(user_id, user_name, user_password, password_hash):

        try:

            user_verification = validate_user_exists(user_name)

            # insert validation
            if user_verification[0]:

                # update method
                update_user_password_hashed(user_name, password_hash)

            else:
                # insert

                insert_user_authenticated(user_id, user_name, user_password, password_hash)

        except SQLAlchemyError as e:
            logger.exception('An exception was occurred while execute transactions: %s', e)
            raise mvc_exc.ItemNotStored(
                'Can\'t insert user_id: "{}" with user_name: {} because it\'s not stored in "{}"'.format(
                    user_id, user_name, UsersAuth.__tablename__
                )
            )


# Transaction to looking for a user_role on db to authenticate
def validate_user_exists(user_name):
    r"""
    Looking for a user_role by name on the database to valid authentication.

    :param user_name: The user_role name to valid authentication on the API.
    :return result: Boolean to valid if the user_role name exists to authenticate the API.
    """

    cfg = get_config_constant_file()

    conn = session_to_db()

    cursor = create_cursor(conn)

    table_name = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    sql_check = "SELECT EXISTS(SELECT 1 FROM {} WHERE username = {} LIMIT 1)".format(table_name, "'" + user_name + "'")

    cursor.execute(sql_check)

    result = cursor.fetchone()

    close_cursor(cursor)
    disconnect_from_db(conn)

    return result


# Transaction to update user_role' password  hashed on db to authenticate
def update_user_password_hashed(user_name, password_hash):
    r"""
    Transaction to update password hashed of a user_role to authenticate on the API correctly.

    :param user_name: The user_role name to update password hashed.
    :param password_hash: The password hashed to authenticate on the API.
    """

    cfg = get_config_constant_file()

    conn = session_to_db()

    cursor = create_cursor(conn)

    last_update_date = get_datenow_from_db()

    table_name = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    # update row to database
    sql_update_user = "UPDATE {} SET password_hash = %s, last_update_date = %s WHERE username = %s".format(
        table_name
    )

    cursor.execute(sql_update_user, (password_hash, last_update_date, user_name,))

    conn.commit()

    close_cursor(cursor)
    disconnect_from_db(conn)


def insert_user_authenticated(user_id, user_name, user_password, password_hash):
    r"""
    Transaction to add a user_role data to authenticate to API, inserted on the db.

    :param user_id: The Id of the user_role to add on the db.
    :param user_name: The user_role name of the user_role to add on the db.
    :param user_password:  The password od the user_role to add on the db.
    :param password_hash: The password hashed to authenticate on the API.
    """

    cfg = get_config_constant_file()

    conn = session_to_db()

    cursor = create_cursor(conn)

    last_update_date = get_datenow_from_db()

    table_name = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    data = (user_id, user_name, user_password, password_hash,)

    sql_user_insert = 'INSERT INTO {} (user_id, username, password, password_hash) ' \
                      'VALUES (%s, %s, %s, %s)'.format(table_name)

    cursor.execute(sql_user_insert, data)

    conn.commit()

    logger.info('Usuario insertado %s', "{0}, User_Name: {1}".format(user_id, user_name))

    close_cursor(cursor)
    disconnect_from_db(conn)


# Function not used.
# Deprecated
def get_data_user_authentication(session, table_name, user_name):
    user_auth = []

    user_auth_data = {}

    try:
        sql_user_data = " SELECT user_name, user_password, password_hash, last_update_date " \
                        " FROM {} " \
                        " WHERE user_name = {} ".format(table_name, "'" + user_name + "'")

        user_auth_db = session.execute(sql_user_data)

        for user_role in user_auth_db:
            if user_role is not None:

                user_name_db = user_role['username']
                user_password_db = user_role['password']
                password_hash = user_role['password_hash']
                last_update_date = datetime.strptime(str(user_role['last_update_date']), "%Y-%m-%d")

                user_auth += [{
                    "username": user_name_db,
                    "password": user_password_db,
                    "password_hash": password_hash,
                    "date_updated": last_update_date
                }]

            else:
                logger.error('Can not read the recordset, beacause is not stored')
                raise SQLAlchemyError(
                    "Can\'t read data because it\'s not stored in table {}. SQL Exception".format(table_name)
                )

        user_auth_data = json.dumps(user_auth)

        user_auth_db.close()

    except SQLAlchemyError as sql_exec:
        logger.exception(sql_exec)
    finally:
        session.close()

    return user_auth_data

'''