# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later


PostgreSQL DB backend.

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:
    About the Users data on the database to generate CRUD operations from endpoint of the API:
    - Insert data
    - Update data
    - Search data

"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2021"
__license__ = ""
__history__ = """ """
__version__ = "1.21.F21.1 ($Rev: 1 $)"

import json
import logging
from datetime import datetime
from pytz import timezone
from sqlalchemy_filters import apply_filters
from sqlalchemy import Column, Boolean, Integer, String, Date, Time, Sequence
from db_controller.database_backend import *
from db_controller import mvc_exceptions as mvc_exc

cfg_db = get_config_settings_db()

USERS_ID_SEQ = Sequence('users_seq')  # define sequence explicitly


class UsersAuthModel(Base):
    r"""
    Class to instance User data to authenticate the API.
    Transactions:
     - Insert: Add user_role data to the database if not exists.
     - Update: Update user_role data on the database if exists.
    """

    __tablename__ = cfg_db.user_auth_table

    user_id = Column('user_id', Integer, USERS_ID_SEQ, primary_key=True, server_default=USERS_ID_SEQ.next_value())
    user_name = Column('user_name', String, nullable=False)
    password = Column('password_hash', String, nullable=False)
    is_active = Column('is_active', Boolean, nullable=False)
    is_staff = Column('is_staff', Boolean, nullable=False)
    is_superuser = Column('is_superuser', Boolean, nullable=False)
    creation_date = Column('creation_date', Date, nullable=False)
    last_update_date = Column('last_update_date', Date, nullable=True)

    def __init__(self, data_user):

        self.user_name = data_user.get('username')
        self.password = data_user.get('password')
        self.is_active = data_user.get('is_active')
        self.is_staff = data_user.get('is_staff')
        self.is_superuser = data_user.get('is_superuser')
        # self.email = data_user.get('creation_date')

    def manage_user_authentication(self, session, data):

        try:

            user_verification = self.check_if_row_exists(session, data)

            # insert validation
            if user_verification:

                # update method
                self.user_update_password(session, data)

            else:
                # insert

                self.insert_data(session, data)

        except SQLAlchemyError as e:
            logger.exception('An exception was occurred while execute transactions: %s', e)
            raise mvc_exc.ItemNotStored(
                'Can\'t insert user_id: "{}" with user_name: {} because it\'s not stored in "{}"'.format(
                    data.get('username'), data.get('is_active'), UsersAuthModel.__tablename__
                )
            )

    # Transaction to looking for a user_role on db to authenticate
    def check_if_row_exists(self, session, data):
        r"""
        Looking for a user_role by name on the database to valid authentication.

        :param session: The session of the database.
        :param data: The data of User model to valid authentication on the API.
        :return row_exists: Statement data row to valid if the user_role name exists to authenticate the API.
        """

        row_exists = None
        user_id = 0

        try:

            user_row = self.get_user_by_id(session, data)

            if user_row is not None:
                user_id = user_row.user_id
            else:
                user_id = 0

            logger.info('User Row object in DB: %s', str(user_row))

            row_exists = session.query(UsersAuthModel).filter(UsersAuthModel.user_id == user_id). \
                filter(UsersAuthModel.user_name == data.get('username')).scalar()

            logger.info('Row to data: {}, Exists: %s'.format(data), str(row_exists))

        except SQLAlchemyError as exc:
            row_exists = None
            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.IntegrityError(
                'Row not stored in "{}". IntegrityError: {}'.format(data.get('username'),
                                                                    str(str(exc.args) + ':' + str(exc.code)))
            )
        finally:
            session.close()

        return row_exists

    def insert_data(self, session, data):
        r"""
        Looking for a user_role by name on the database to valid authentication.

        :param session: The session of the database.
        :param data: The data of User model to valid authentication on the API.
        """

        endpoint_response = None

        if not self.check_if_row_exists(session, data):

            try:

                self.creation_date = get_current_date(session)

                data['creation_date'] = self.creation_date

                new_row = UsersAuthModel(data)

                logger.info('New Row User name: %s', str(new_row.user_name))

                session.add(new_row)

                user_row = self.get_user_by_id(session, data)

                logger.info('User ID Inserted: %s', str(user_row.user_id))

                session.flush()

                data['user_id'] = user_row.user_id

                # check insert correct
                row_inserted = self.get_one_user(session, data)

                logger.info('Data User inserted: %s, Original Data: {}'.format(data), str(row_inserted))

                if row_inserted:
                    logger.info('User inserted is: %s', 'Username: {}, '
                                                        'IsActive: {} '
                                                        'CreationDate: {}'.format(row_inserted.user_name,
                                                                                  row_inserted.is_active,
                                                                                  row_inserted.creation_date))

                    endpoint_response = json.dumps({
                        "Username": row_inserted.user_name,
                        "Password": row_inserted.password,
                        "IsActive": row_inserted.is_active,
                        "IsStaff": row_inserted.is_staff,
                        "IsSuperUser": row_inserted.is_superuser,
                        "CreationDate": row_inserted.creation_date
                    })

            except SQLAlchemyError as exc:
                endpoint_response = None
                session.rollback()
                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('username'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    # Transaction to update user_role' password  hashed on db to authenticate - PATCH
    def user_update_password(self, session, data):
        r"""
        Transaction to update password hashed of a user_role to authenticate on the API correctly.

        :param session: The user_role name to update password hashed.
        :param data: The password hashed to authenticate on the API.
        """

        endpoint_response = None

        if self.check_if_row_exists(session, data):

            try:

                self.last_update_date = get_current_date(session)

                data['last_update_date'] = self.last_update_date

                # update row to database
                session.query(UsersAuthModel).filter(UsersAuthModel.password == data.get('password')). \
                    update({"password": data.get('password'),
                            "last_update_date": data.get('last_update_date')},
                           synchronize_session='fetch')

                session.flush()

                # check update correct
                row_updated = self.get_one_user(session, data)

                logger.info('Data Updated: %s', str(row_updated))

                if row_updated:
                    logger.info('Data User updated')

                    endpoint_response = json.dumps({
                        "Username": row_updated.user_name,
                        "Password": row_updated.password,
                        "IsActive": row_updated.is_active,
                        "IsStaff": row_updated.is_staff,
                        "IsSuperUser": row_updated.is_superuser,
                        "CreationDate": row_updated.creation_date,
                        "UpdatedDate": row_updated.last_update_date
                    })

            except SQLAlchemyError as exc:
                session.rollback()
                endpoint_response = None

                logger.exception('An exception was occurred while execute transactions: %s',
                                 str(str(exc.args) + ':' +
                                     str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('username'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    @staticmethod
    def get_user_by_id(session, data):

        row = None

        try:

            row_exists = session.query(UsersAuthModel).filter(UsersAuthModel.user_name == data.get('username')). \
                filter(UsersAuthModel.is_active == data.get('is_active')). \
                filter(UsersAuthModel.is_superuser == data.get('is_superuser')).scalar()

            if row_exists:
                row = session.query(UsersAuthModel).filter(UsersAuthModel.user_name == data.get('username')).\
                    filter(UsersAuthModel.is_active == data.get('is_active')).\
                    filter(UsersAuthModel.is_superuser == data.get('is_superuser')).one()

                logger.info('Data User on Db: %s',
                            'Username: {}, Is_Active: {}'.format(row.user_name, row.is_activee))

        except SQLAlchemyError as exc:
            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))

            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('username'), UsersAuthModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return row

    def get_one_user(self, session, data):

        row_user = None

        try:

            user_row = self.get_user_by_id(session, data)

            if session.query(UsersAuthModel).filter(UsersAuthModel.user_id == user_row.user_id).scalar():

                row_user = session.query(UsersAuthModel).filter(UsersAuthModel.user_id == user_row.user_id).one()

                if row_user:
                    logger.info('Data Bank on Db: %s',
                                'Bank Name: {}, Bank usaToken: {}, Bank Status: {}'.format(row_user.nombre_banco,
                                                                                           row_user.usa_token,
                                                                                           row_user.estatus_banco))

        except SQLAlchemyError as exc:
            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('user_id'), UsersAuthModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )
        finally:
            session.close()

        return row_user

    @staticmethod
    def get_all_users(session):

        all_users = None
        user_data = []
        data = dict()

        all_users = session.query(UsersAuthModel).all()

        for user_rs in all_users:
            id_user = user_rs.user_id
            username = user_rs.user_name
            password = user_rs.password
            is_active = user_rs.is_active
            is_staff = user_rs.is_staff
            is_superuser = user_rs.is_superuser
            creation_date = user_rs.creation_date
            last_update_date = user_rs.last_update_date

            user_data += [{
                "AuthUser": {
                    "Id": id_user,
                    "Username": username,
                    "Password": password,
                    "IsActive": is_active,
                    "IsStaff": is_staff,
                    "IsSuperuser": is_superuser,
                    "CreationDate": creation_date,
                    "LastUpdateDate": last_update_date
                }
            }]

        return json.dumps(user_data)

    def __repr__(self):
        return "<AuthUserModel(id_user='%s', username='%s', password='%s', email='%s', " \
               "first_name='%s', last_name='%s', is_active='%s', is_staff='%s', is_superuser='%s', " \
               "date_joined='%s')>" % (self.user_id, self.username, self.password, self.email, self.first_name,
                                       self.last_name, self.is_active, self.is_staff, self.is_superuser,
                                       self.date_joined)
