# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later


PostgreSQL DB backend.

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:
    About the Vehicle data on the database to generate CRUD operations from endpoint of the API:
    - Insert data
    - Update data
    - Delete data
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
from apps.vehicle.VehicleModel import VehicleModel
from sqlalchemy_filters import apply_filters
from sqlalchemy import Column, Numeric, Integer, String, Date, Time, Sequence
from db_controller.database_backend import *
from db_controller import mvc_exceptions as mvc_exc

cfg_db = get_config_settings_db()

DRIVER_ID_SEQ = Sequence('driver_seq')  # define sequence explicitly


class DriverModel(Base):
    r"""
    Class to instance the data of DriverModel on the database.
    Transactions:
     - Insert: Add data to the database if not exists.
     - Update: Update data on the database if exists.
     - Delete:
     - Select:
    """

    __tablename__ = cfg_db.gas_driver_table.__str__()

    driver_id = Column(cfg_db.GasDriver.driver_id, Integer, DRIVER_ID_SEQ,
                       primary_key=True, server_default=DRIVER_ID_SEQ.next_value())
    driver_name = Column(cfg_db.GasDriver.driver_name, String, nullable=False)
    driver_last_name = Column(cfg_db.GasDriver.driver_lastname1, String, nullable=False)
    driver_last_name_last = Column(cfg_db.GasDriver.driver_lastname2, String, nullable=True)
    driver_address = Column(cfg_db.GasDriver.driver_address, String, nullable=True)
    driver_registered = Column(cfg_db.GasDriver.driver_date_assignment, Date, nullable=False)
    driver_status = Column(cfg_db.GasDriver.driver_status, String, nullable=False)
    last_update_date = Column('last_update_date', Date, nullable=True)

    vehicle_assignment = Column(
        cfg_db.GasDriver.vehicle_id_fk,
        Integer,
        ForeignKey('VehicleModel.vehicle_id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        unique=True
        # no need to add index=True, all FKs have indexes
    )

    vehicle = relationship(VehicleModel,
                           backref=cfg_db.gas_vehicle_table.__str__())

    def __init__(self, data_driver):
        self.driver_name = data_driver.get('nombre_conductor')
        self.driver_last_name = data_driver.get('apellido_paterno_conductor')
        self.driver_last_name_last = data_driver.get('apellido_materno_conductor')
        self.driver_address = data_driver.get('domicilio_conductor')
        self.driver_status = data_driver.get('estatus_conductor')
        # self.driver_registered = get_current_date(session)
        self.vehicle_assignment = data_driver.get('vehiculo')

    def check_if_row_exists(self, session, data):
        """
        Validate if row exists on database from dictionary data

        :param session: Session database object
        :param data: Dictionary with data to make validation function
        :return: row_exists: Object with boolean response from db
        """

        row_exists = None
        id_driver = 0

        if 'activo' in data.get('estatus_conductor').lower():

            try:
                # for example to check if the insert on db is correct
                row_driver = self.get_driver_id(session, data)

                if row_driver is not None:
                    id_driver = row_driver.driver_id
                else:
                    id_driver = 0

                logger.info('Driver Row object in DB: %s', str(id_driver))

                row_exists = session.query(DriverModel).filter(DriverModel.driver_id == id_driver).scalar()

                logger.info('Row to data: {}, Exists: %s'.format(data), str(row_exists))

            except SQLAlchemyError as exc:
                row_exists = None

                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_conductor'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return row_exists

    def insert_data(self, session, data):
        """
        Function to insert new row on database

        :param session: Session database object
        :param data: Dictionary to insert new the data containing on the db
        :return: endpoint_response
        """

        endpoint_response = None

        if not self.check_if_row_exists(session, data):

            try:

                self.driver_registered = get_current_date(session)

                data['driver_registered'] = self.driver_registered

                new_row = DriverModel(data)

                logger.info('New Row Driver: %s', str(new_row.driver_name))

                session.add(new_row)

                row_driver = self.get_driver_id(session, data)

                logger.info('Driver ID Inserted: %s', str(row_driver.driver_id))

                session.flush()

                data['driver_id'] = row_driver.driver_id

                # check insert correct
                row_inserted = self.get_one_driver(session, data)

                logger.info('Data Driver inserted: %s, Original Data: {}'.format(data), str(row_inserted))

                if row_inserted:
                    endpoint_response = json.dumps({
                        "id_driver": row_inserted.driver_id,
                        "name_driver": row_inserted.driver_name,
                        "lastname_driver": row_inserted.driver_last_name,
                        "lastname_last_driver": row_inserted.driver_last_name_last,
                        "address_driver": row_inserted.driver_address,
                        "driver_added_date": row_inserted.driver_registered,
                        "status_driver": row_inserted.driver_status,
                        "vehicle_driver": row_inserted.vehicle_assignment
                    })

            except SQLAlchemyError as exc:
                endpoint_response = None
                session.rollback()

                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_conductor'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    def update_data(self, session, data):
        """
        Function to update row on database

        :param session: Session database object
        :param data: Dictionary to update the data containing on the db
        :return: endpoint_response
        """

        endpoint_response = None

        if self.check_if_row_exists(session, data):

            try:

                row_driver = self.get_driver_id(session, data)

                if row_driver is not None:
                    id_driver = row_driver.driver_id
                else:
                    id_driver = 0

                logger.info('Driver Row object in DB: %s', str(id_driver))

                self.last_update_date = get_current_date(session)

                data['last_update_date'] = self.last_update_date

                data['driver_id'] = id_driver

                # update row to database
                session.query(DriverModel).filter(DriverModel.driver_id == id_driver).\
                    update({"driver_name": data.get('nombre_conductor'),
                            "driver_last_name": data.get('apellido_paterno_conductor'),
                            "driver_last_name_last": data.get('apellido_materno_conductor'),
                            "driver_address": data.get('apellido_materno_conductor'),
                            "driver_registered": data.get('domicilio_conductor'),
                            "driver_status": data.get('estatus_conductor'),
                            "vehicle_assignment": data.get('vehiculo'),
                            "last_update_date": data.get('last_update_date')},
                           synchronize_session='fetch')

                session.flush()

                # check update correct
                row_updated = self.get_one_driver(session, data)

                logger.info('Data Updated: %s', str(row_updated))

                if row_updated:
                    logger.info('Data Driver updated')

                    endpoint_response = json.dumps({
                        "id_driver": row_updated.driver_id,
                        "name_driver": row_updated.driver_name,
                        "lastname_driver": row_updated.driver_last_name,
                        "lastname_last_driver": row_updated.driver_last_name_last,
                        "address_driver": row_updated.driver_address,
                        "driver_added_date": str(row_updated.driver_registered),
                        "status_driver": row_updated.driver_status,
                        "vehicle_driver": row_updated.vehicle_assignment,
                        "last_date_updated": str(row_updated.last_update_date)
                    })

            except SQLAlchemyError as exc:
                endpoint_response = None
                session.rollback()
                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_conductor'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    def delete_data(self, session, data):
        """
        Inactivate or set INACTIVO the status_driver to do not show anymore

        :param session: Database object session
        :param data: Dictionary with data to inactivate Driver
        :return: endpoint_response
        """

        endpoint_response = None

        status_driver = self.get_status_driver(session, data)

        if status_driver is not None:

            if 'inactivo' not in status_driver:

                try:

                    row_driver = self.get_driver_id(session, data)

                    if row_driver is not None:
                        id_driver = row_driver.driver_id
                    else:
                        id_driver = 0

                    logger.info('Driver Row object in DB: %s', str(id_driver))

                    data['driver_id'] = id_driver

                    session.query(DriverModel).filter(DriverModel.driver_id == id_driver).\
                        update({"driver_status": "INACTIVO"},
                               synchronize_session='fetch')

                    session.flush()

                    # check update correct
                    row_deleted = self.get_one_driver(session, data)

                    if row_deleted:
                        logger.info('Driver inactive')

                        endpoint_response = json.dumps({
                            "id_driver": row_deleted.driver_id,
                            "name_driver": row_deleted.driver_name,
                            "lastname_driver": row_deleted.driver_last_name,
                            "lastname_last_driver": row_deleted.driver_last_name_last,
                            "address_driver": row_deleted.driver_address,
                            "driver_added_date": row_deleted.driver_registered,
                            "status_driver": row_deleted.driver_status,
                            "vehicle_driver": row_deleted.vehicle_assignment
                        })

                except SQLAlchemyError as exc:
                    endpoint_response = None
                    session.rollback()

                    logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                     str(exc.code)))
                    raise mvc_exc.IntegrityError(
                        'Row not stored in "{}". IntegrityError: {}'.format(data.get('nombre_conductor'),
                                                                            str(str(exc.args) + ':' + str(exc.code)))
                    )
                finally:
                    session.close()

        return endpoint_response

    @staticmethod
    def get_driver_id(session, data):
        """
        Get Driver object row registered on database to get the ID

        :param session: Database session object
        :param data: Dictionary with data to get row
        :return: row_driver: The row on database registered
        """

        row_driver = None

        try:

            row_exists = session.query(DriverModel).filter(DriverModel.driver_name == data.get('nombre_conductor')).\
                filter(DriverModel.driver_last_name == data.get('apellido_paterno_conductor')).scalar()

            logger.info('Row Data Driver Exists on DB: %s', str(row_exists))

            if row_exists:

                row_driver = session.query(DriverModel).\
                    filter(DriverModel.driver_name == data.get('nombre_conductor')).\
                    filter(DriverModel.driver_last_name == data.get('apellido_paterno_conductor')).one()

                if 'vehiculo' in data.keys():

                    row_driver = session.query(DriverModel). \
                        filter(DriverModel.driver_name == data.get('nombre_conductor')). \
                        filter(VehicleModel.vehicle_id == data.get('vehiculo')). \
                        filter(DriverModel.driver_last_name == data.get('apellido_paterno_conductor')).one()

                logger.info('Row ID Driver data from database object: {}'.format(str(row_driver)))

        except SQLAlchemyError as exc:

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('nombre_conductor'), DriverModel.__tablename__, str(str(exc.args) + ':' +
                                                                                 str(exc.code))
                )
            )

        finally:
            session.close()

        return row_driver

    @staticmethod
    def get_one_driver(session, data):
        row = None

        try:

            if 'vehiculo' in data.keys():

                row = session.query(DriverModel). \
                    filter(DriverModel.driver_id == data.get('driver_id')). \
                    filter(VehicleModel.vehicle_id == data.get('vehiculo')).one()

            row = session.query(DriverModel).filter(DriverModel.driver_id == data.get('driver_id')).\
                filter(DriverModel.driver_name == data.get('nombre_conductor')).one()

            if row:
                logger.info('Data Driver on Db: %s',
                            'Nombre: {}, Apellido: {}, Estatus: {}'.format(row.driver_name,
                                                                           row.driver_last_name,
                                                                           row.driver_status))

        except SQLAlchemyError as exc:
            row = None
            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))

            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('nombre_conductor'), DriverModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return row

    def get_status_driver(self, session, data):
        """
        Get status driver registered previously to validate the check if apply modifying

        :param session: Database session
        :param data: Dictionary with the data to validate
        :return: str: estatus_conductor
        """

        estatus_conductor = None
        driver_row = None

        try:
            driver_row = self.get_driver_id(session, data)

            logger.info('Driver Id: %s', str(driver_row.driver_id))

            if driver_row:

                row = session.query(DriverModel).filter(DriverModel.driver_id == driver_row.driver_id).one()

                if row:
                    estatus_conductor = row.driver_status

                    logger.info('Driver Status: %s', estatus_conductor)

        except SQLAlchemyError as exc:
            estatus_conductor = None
            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))

            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('nombre_conductor'), DriverModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return estatus_conductor

    @staticmethod
    def get_all_inversiones(session):
        """
        Get all Driver objects data registered on database.

        :param session: Database session
        :return: json.dumps dict
        """

        all_drivers = None
        drivers_data = []

        all_drivers = session.query(DriverModel).all()

        for driver in all_drivers:
            id_driver = driver.driver_id
            name_driver = driver.driver_name
            lastname_driver = driver.driver_last_name
            lastname_last_driver = driver.driver_last_name_last
            address_driver = driver.driver_address
            registered_driver = driver.driver_registered
            status_driver = driver.driver_status
            assigment_vehicle = driver.vehicle_assignment
            last_updated_date = driver.last_update_date

            drivers_data += [{
                "Driver": {
                    "id_driver": id_driver,
                    "name_driver": name_driver,
                    "lastname_driver": lastname_driver,
                    "lastname_last_driver": lastname_last_driver,
                    "address_driver": address_driver,
                    "driver_added_date": str(registered_driver),
                    "status_driver": status_driver,
                    "vehicle_driver": assigment_vehicle,
                    "last_date_updated": str(last_updated_date)
                }
            }]

        return json.dumps(drivers_data)

    @staticmethod
    def get_inversiones_by_filters(session, filter_spec=list):

        query_result = None
        inversiones_data = []

        if filter_spec is None:
            query_result = session.query(GinInversionesModel).all()

        query = session.query(GinInversionesModel)

        filtered_query = apply_filters(query, filter_spec)
        query_result = filtered_query.all()

        logger.info('Query filtered resultSet: %s', str(query_result))

        for inversion in query_result:
            inversion_id = inversion.invId
            cuenta = inversion.cuenta
            estatus = inversion.estatus
            monto = inversion.monto
            autorizacion = inversion.autorizacion
            canal = inversion.canal
            origen = inversion.origen
            comisionistaId = inversion.comisionistaId
            transaccionId = inversion.transaccionId
            motivo = inversion.motivo
            fechaRecepcion = inversion.fechaRecepcion
            horaRecepcion = inversion.horaRecepcion
            fechaAplicacion = inversion.fechaAplicacion
            horaAplicacion = inversion.horaAplicacion
            conciliacionId = inversion.conciliacionId
            codigoBancario = inversion.codigoBancario
            metodoDeposito = inversion.metodoDeposito

            inversiones_data += [{
                "invId": inversion_id,
                "cuenta": cuenta,
                "estatus": estatus,
                "monto": str(monto),
                "autorizacion": autorizacion,
                "canal": canal,
                "origen": origen,
                "comisionistaId": comisionistaId,
                "transaccionId": transaccionId,
                "motivo": motivo,
                "fechaRecepcion": str(fechaRecepcion),
                "horaRecepcion": str(horaRecepcion),
                "fechaAplicacion": str(fechaAplicacion),
                "horaAplicacion": str(horaAplicacion),
                "conciliacionId": conciliacionId,
                "codigoBancario": codigoBancario,
                "metodoDeposito": metodoDeposito
            }]

        return json.dumps(inversiones_data)

    def __repr__(self):
        return "<DriverModel(driver_id='%s', " \
               "             driver_name='%s', " \
               "             driver_last_name='%s', " \
               "             driver_last_name_last='%s', " \
               "             driver_address='%s', " \
               "             driver_registered='%s', " \
               "             driver_status='%s', " \
               "             last_update_date='%s', " \
               "             vehicle_assignment='%s')>" % (self.driver_id, self.driver_name, self.driver_last_name,
                                                           self.driver_last_name_last, self.driver_address,
                                                           self.driver_registered, self.driver_status,
                                                           self.last_update_date, self.vehicle_assignment)
