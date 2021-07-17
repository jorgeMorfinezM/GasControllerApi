# -*- coding: utf-8 -*-

"""
Requires Python 3.8 or later


PostgreSQL DB backend.

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:
    About the Bank Bot data on the database to generate CRUD operations from endpoint of the API:
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
from sqlalchemy_filters import apply_filters
from sqlalchemy import Column, Numeric, Integer, String, Date, Time, Sequence, Float
from db_controller.database_backend import *
from db_controller import mvc_exceptions as mvc_exc

cfg_db = get_config_settings_db()

VEHICLE_ID_SEQ = Sequence('vehicle_seq')  # define sequence explicitly


class VehicleModel(Base):
    r"""
    Class to instance the data of VehicleModel on the database.
    Transactions:
     - Insert: Add data to the database if not exists.
     - Update: Update data on the database if exists.
     - Delete:
     - Select:
    """

    __tablename__ = cfg_db.gas_vehicle_table.__str__()

    vehicle_id = Column(cfg_db.GasVehicle.vehiculo_id, Integer, VEHICLE_ID_SEQ,
                        primary_key=True, server_default=VEHICLE_ID_SEQ.next_value())
    vehicle_model = Column(cfg_db.GasVehicle.vehiculo_modelo, String, nullable=False)
    vehicle_brand = Column(cfg_db.GasVehicle.vehiculo_marca, String, nullable=False)
    vehicle_plate = Column(cfg_db.GasVehicle.vehiculo_matricula, String, nullable=False)
    vehicle_num_seats = Column(cfg_db.GasVehicle.vehiculo_numero_asientos, Integer, nullable=False)
    vehicle_num_doors = Column(cfg_db.GasVehicle.vehiculo_numero_puertas, Integer, nullable=False)
    vehicle_color = Column(cfg_db.GasVehicle.vehiculo_color, String, nullable=True)
    vehicle_anio_model = Column(cfg_db.GasVehicle.vehiculo_anio_modelo, Integer, nullable=True)
    vehicle_model_motor = Column(cfg_db.GasVehicle.vehiculo_modelo_motor, String, nullable=True)
    vehicle_anio_motor = Column(cfg_db.GasVehicle.vehiculo_anio_motor, Integer, nullable=True)
    vehicle_chasis_number = Column(cfg_db.GasVehicle.vehiculo_numero_chasis, String, nullable=True)
    vehicle_transmision = Column(cfg_db.GasVehicle.vehiculo_transmision, String, nullable=True)
    vehicle_gas_type = Column(cfg_db.GasVehicle.vehiculo_tipo_combustible, String, nullable=False)
    vehicle_co2_emisions = Column(cfg_db.GasVehicle.vehiculo_emisiones_co2, Float, nullable=True)
    vehicle_horse_power = Column(cfg_db.GasVehicle.vehiculo_caballos_fuerza, Integer, nullable=True)
    vehicle_potence = Column(cfg_db.GasVehicle.vehiculo_potencia, Integer, nullable=True)
    vehicle_description = Column(cfg_db.GasVehicle.vehiculo_descripcion, String, nullable=True)
    vehicle_catalog_cost = Column(cfg_db.GasVehicle.vehiculo_costo_catalogo, Float, nullable=False)
    vehicle_purchase_cost = Column(cfg_db.GasVehicle.vehiculo_costo_compra, Float, nullable=False)
    vehicle_tax_cost = Column(cfg_db.GasVehicle.vehiculo_costo_impuesto, Integer, nullable=False)
    vehicle_register_date = Column(cfg_db.GasVehicle.vehiculo_fecha_registro, Date, nullable=True)
    vehicle_low_register_date = Column(cfg_db.GasVehicle.vehiculo_fecha_baja, Date, nullable=False)

    def __init__(self, data_vehicle):

        self.vehicle_model = data_vehicle.get('vehiculo_modelo')
        self.vehicle_brand = data_vehicle.get('vehiculo_marca')
        self.vehicle_plate = data_vehicle.get('vehiculo_matricula')
        self.vehicle_num_seats = data_vehicle.get('vehiculo_numero_asientos')
        self.vehicle_num_doors = data_vehicle.get('vehiculo_numero_puertas')
        self.vehicle_color = data_vehicle.get('vehiculo_color')
        self.vehicle_anio_model = data_vehicle.get('vehiculo_modelo_anio')
        self.vehicle_model_motor = data_vehicle.get('vehiculo_modelo_motor')
        self.vehicle_anio_motor = data_vehicle.get('vehiculo_anio_motor')
        self.vehicle_chasis_number = data_vehicle.get('vehiculo_numero_chasis')
        self.vehicle_transmision = data_vehicle.get('vehiculo_transmision')
        self.vehicle_gas_type = data_vehicle.get('vehiculo_tipo_transmision')
        self.vehicle_co2_emisions = data_vehicle.get('vehiculo_emisiones_co2')
        self.vehicle_horse_power = data_vehicle.get('vehiculo_caballos_fuerza')
        self.vehicle_potence = data_vehicle.get('vehiculo_potencia')
        self.vehicle_description = data_vehicle.get('vehiculo_descripcion')
        self.vehicle_catalog_cost = data_vehicle.get('vehiculo_costo_catalogo')
        self.vehicle_purchase_cost = data_vehicle.get('vehiculo_costo_compra')
        self.vehicle_tax_cost = data_vehicle.get('vehiculo_costo_impuesto')
        self.vehicle_register_date = data_vehicle.get('vehiculo_fecha_registro')
        self.vehicle_low_register_date = data_vehicle.get('vehiculo_fecha_baja')

    def check_if_row_exists(self, session, data):

        row_exists = None
        inversion_id = 0

        try:
            # for example to check if the insert on db is correct
            inv_id = self.get_inversion_id(session, data)

            if inv_id is not None:
                inversion_id = inv_id.invId
            else:
                inversion_id = 0

            logger.info('Inversion Row object in DB: %s', str(inversion_id))

            row_exists = session.query(GinInversionesModel).filter(GinInversionesModel.invId == inversion_id).\
                filter(GinInversionesModel.cuenta == data.get('cuenta')).scalar()

            logger.info('Row to data: {}, Exists: %s'.format(data), str(row_exists))

        except SQLAlchemyError as exc:
            row_exists = None

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.IntegrityError(
                'Row not stored in "{}". IntegrityError: {}'.format(data.get('cuenta'),
                                                                    str(str(exc.args) + ':' + str(exc.code)))
            )
        finally:
            session.close()

        return row_exists

    def insert_data(self, session, data):

        endpoint_response = None

        if not self.check_if_row_exists(session, data):

            try:

                new_row = GinInversionesModel(data)

                logger.info('New Row Inversion Cuenta: %s', str(new_row.cuenta))

                session.add(new_row)

                inv_id = self.get_inversion_id(session, data).invId

                logger.info('Inversion ID Inserted: %s', str(inv_id))

                session.flush()

                data['invId'] = inv_id

                # check insert correct
                row_inserted = self.get_one_inversion(session, data)

                logger.info('Data Bank inserted: %s, Original Data: {}'.format(data), str(row_inserted))

                if row_inserted:
                    endpoint_response = json.dumps({
                        "invId": inv_id,
                        "cuenta": row_inserted.cuenta,
                        "monto": str(row_inserted.monto),
                        "estatus": row_inserted.estatus,
                        "canal": row_inserted.canal,
                        "origen": row_inserted.origen,
                        "autorizacion": row_inserted.autorizacion,
                        "motivo": row_inserted.motivo,
                        "comisionistaId": row_inserted.comisionistaId,
                        "transaccionId": row_inserted.transaccionId,
                        "fechaRecepcion": str(row_inserted.fechaRecepcion),
                        "horaRecepcion": str(row_inserted.horaRecepcion),
                        "conciliacionId": str(row_inserted.conciliacionId)
                    })

            except SQLAlchemyError as exc:

                endpoint_response = None

                session.rollback()

                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('cuenta'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    def save_inversion(self, session, data):

        endpoint_response = None

        if not self.check_if_row_exists(session, data):

            try:

                new_row = GinInversionesModel(data)

                logger.info('New Row Inversion Cuenta: %s', str(new_row.cuenta))

                session.add(new_row)

                inv_id = self.get_inversion_id(session, data).invId

                logger.info('Inversion ID Inserted: %s', str(inv_id))

                session.flush()

                data['invId'] = inv_id

                # check insert correct
                row_inserted = self.get_one_inversion(session, data)

                logger.info('Data Bank inserted: %s, Original Data: {}'.format(data), str(row_inserted))

                if row_inserted:

                    endpoint_response = json.dumps({
                        "invId": inv_id,
                        "cuenta": row_inserted.cuenta,
                        "monto": str(row_inserted.monto),
                        "estatus": row_inserted.estatus,
                        "canal": row_inserted.canal,
                        "origen": row_inserted.origen,
                        "autorizacion": row_inserted.autorizacion,
                        "motivo": row_inserted.motivo,
                        "comisionistaId": row_inserted.comisionistaId,
                        "transaccionId": row_inserted.transaccionId,
                        "fechaRecepcion": str(row_inserted.fechaRecepcion),
                        "horaRecepcion": str(row_inserted.horaRecepcion),
                        "fechaAplicacion": str(row_inserted.fechaAplicacion),
                        "horaAplicacion": str(row_inserted.horaAplicacion),
                        "conciliacionId": str(row_inserted.conciliacionId),
                        "codigoBancario": str(row_inserted.codigoBancario),
                        "metodoDeposito": str(row_inserted.metodoDeposito),
                    })

            except SQLAlchemyError as exc:
                session.rollback()
                logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                 str(exc.code)))
                raise mvc_exc.IntegrityError(
                    'Row not stored in "{}". IntegrityError: {}'.format(data.get('cuenta'),
                                                                        str(str(exc.args) + ':' + str(exc.code)))
                )
            finally:
                session.close()

        return endpoint_response

    def delete_data(self, session, data):

        endpoint_response = None

        estatus_inversion = self.get_status_inversion(session, data)

        if estatus_inversion:

            if 'CANCELADO' not in estatus_inversion:

                try:

                    inv_id = self.get_inversion_id_delete(session,
                                                          data.get('cuenta'),
                                                          data.get('canal'),
                                                          data.get('autorizacion')).invId

                    logger.info('Inversion Id: %s', str(inv_id))

                    # update row to database to inactivate Bank
                    # session.query(GinInversionesModel).filter(GinInversionesModel.invId == inv_id). \
                    #     filter(GinInversionesModel.cuenta == data.get('cuenta')).\
                    #     filter(GinInversionesModel.autorizacion == data.get('autorizacion')).\
                    #     update({"estatus": "CANCELADO"},
                    #            synchronize_session='fetch')

                    session.query(GinInversionesModel).filter(GinInversionesModel.invId == inv_id).\
                        update({"estatus": "CANCELADO"},
                               synchronize_session='fetch')

                    session.flush()

                    data['invId'] = inv_id

                    # check update correct
                    row_deleted = self.get_one_inversion(session, data)

                    if row_deleted:
                        logger.info('Bank inactive')

                        endpoint_response = json.dumps({
                            "invId": inv_id,
                            "cuenta": row_deleted.cuenta,
                            "monto": str(row_deleted.monto),
                            "estatus": row_deleted.estatus,
                            "canal": row_deleted.canal,
                            "origen": row_deleted.origen,
                            "autorizacion": row_deleted.autorizacion,
                            "motivo": row_deleted.motivo,
                            "comisionistaId": row_deleted.comisionistaId,
                            "transaccionId": row_deleted.transaccionId,
                            "fechaRecepcion": str(row_deleted.fechaRecepcion),
                            "horaRecepcion": str(row_deleted.horaRecepcion),
                            "fechaAplicacion": str(row_deleted.fechaAplicacion),
                            "horaAplicacion": str(row_deleted.horaAplicacion),
                            "conciliacionId": str(row_deleted.conciliacionId),
                            "codigoBancario": str(row_deleted.codigoBancario),
                            "metodoDeposito": str(row_deleted.metodoDeposito),
                        })

                except SQLAlchemyError as exc:

                    endpoint_response = None

                    session.rollback()

                    logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                                     str(exc.code)))
                    raise mvc_exc.IntegrityError(
                        'Row not stored in "{}". IntegrityError: {}'.format(data.get('cuenta'),
                                                                            str(str(exc.args) + ':' + str(exc.code)))
                    )
                finally:
                    session.close()

        return endpoint_response

    @staticmethod
    def get_inversion_id(session, data):

        row_inversion = None

        try:

            row_exists = session.query(GinInversionesModel).filter(GinInversionesModel.cuenta == data.get('cuenta')).\
                filter(GinInversionesModel.autorizacion == data.get('autorizacion')).\
                filter(GinInversionesModel.transaccionId == data.get('transaccionId')).\
                filter(GinInversionesModel.comisionistaId == data.get('comisionistaId')).scalar()

            logger.info('Row Data Inversion Exists on DB: %s', str(row_exists))

            if row_exists:

                row_inversion = session.query(GinInversionesModel).\
                    filter(GinInversionesModel.cuenta == data.get('cuenta')).\
                    filter(GinInversionesModel.autorizacion == data.get('autorizacion')).\
                    filter(GinInversionesModel.transaccionId == data.get('transaccionId')).\
                    filter(GinInversionesModel.comisionistaId == data.get('comisionistaId')).one()

                logger.info('Row ID Inversion data from database object: {}'.format(str(row_inversion)))

        except SQLAlchemyError as exc:

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('transaccionId'), GinInversionesModel.__tablename__, str(str(exc.args) + ':' +
                                                                                      str(exc.code))
                )
            )

        finally:
            session.close()

        return row_inversion

    @staticmethod
    def get_inversion_id_delete(session, cuenta, canal, autorizacion):

        row_inversion = None

        try:

            row_exists = session.query(GinInversionesModel).filter(GinInversionesModel.cuenta == str(cuenta)). \
                filter(GinInversionesModel.canal == str(canal)).\
                filter(GinInversionesModel.autorizacion == str(autorizacion)).scalar()

            logger.info('Row Data Inversion Exists to InvId: %s', str(row_exists))

            if row_exists:
                row_inversion = session.query(GinInversionesModel).filter(GinInversionesModel.cuenta == str(cuenta)). \
                    filter(GinInversionesModel.canal == str(canal)).\
                    filter(GinInversionesModel.autorizacion == autorizacion).one()

                logger.info('Row ID Inversion data from database object: {}'.format(str(row_inversion)))

        except SQLAlchemyError as exc:

            row_inversion = None

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))
            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    cuenta, GinInversionesModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return row_inversion

    @staticmethod
    def get_all_inversiones(session):

        all_inversiones = None
        inversiones_data = []

        all_inversiones = session.query(GinInversionesModel).all()

        for inversion in all_inversiones:
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
                "Inversion": {
                    "invId": inversion.invId,
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
                }
            }]

        return json.dumps(inversiones_data)

    @staticmethod
    def get_one_inversion(session, data):
        row = None

        try:
            row = session.query(GinInversionesModel).filter(GinInversionesModel.cuenta == data.get('cuenta')).\
                filter(GinInversionesModel.invId == data.get('invId')).one()

            if row:
                logger.info('Data Inversion on Db: %s',
                            'Cuenta: {}, Monto inversion: {}, Inversion Estatus: {}'.format(row.cuenta,
                                                                                            row.monto,
                                                                                            row.estatus))

        except SQLAlchemyError as exc:

            row = None

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))

            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('cuenta'), GinInversionesModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return row

    def get_status_inversion(self, session, data):

        estatus_inv = None

        try:
            inv_id = self.get_inversion_id_delete(session,
                                                  data.get('cuenta'),
                                                  data.get('canal'),
                                                  data.get('autorizacion')).invId

            logger.info('Inversion Id: %s', str(inv_id))

            if inv_id:

                row = session.query(GinInversionesModel).filter(GinInversionesModel.invId == inv_id).\
                    filter(GinInversionesModel.cuenta == data.get('cuenta')).one()

                if row:
                    estatus_inv = row.estatus

                    logger.info('Inversion Estatus: %s', estatus_inv)

        except SQLAlchemyError as exc:
            estatus_inv = None

            logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
                                                                                             str(exc.code)))

            raise mvc_exc.ItemNotStored(
                'Can\'t read data: "{}" because it\'s not stored in "{}". Row empty: {}'.format(
                    data.get('cuenta'), GinInversionesModel.__tablename__, str(str(exc.args) + ':' + str(exc.code))
                )
            )

        finally:
            session.close()

        return estatus_inv

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
        return "<GinInversionesModel(" \
               "invId='%s', " \
               "cuenta='%s', " \
               "estatus='%s', " \
               "canal='%s', " \
               "origen='%s', " \
               "fechaRecepcion='%s')>" % (self.invId,
                                          self.cuenta,
                                          self.estatus,
                                          self.canal,
                                          self.origen,
                                          self.fechaRecepcion
        )

    # DEPRECATED - NOT USE by API
    # def update_data(self, session, data):
    #     if self.check_if_row_exists(session, data):
    #
    #         try:
    #
    #             inv_id = self.get_inversion_id(session,
    #                                            data.get('cuenta'),
    #                                            data.get('estatus'),
    #                                            data.get('monto')).invId
    #
    #             # update row to database
    #             session.query(GinInversionesModel).filter(GinInversionesModel.invId == inv_id).\
    #                 filter(GinInversionesModel == data.get('cuenta')).\
    #                 update({"cuenta": data.get('cuenta'),
    #                         "estatus": data.get('estatus'),
    #                         "monto": data.get('monto'),
    #                         "autorizacion": data.get('autorizacion'),
    #                         "canal": data.get('canal'),
    #                         "origen": data.get('origen'),
    #                         "comisionistaId": data.get('comisionistaId'),
    #                         "transaccionId": data.get('transaccionId'),
    #                         "motivo": data.get('motivo'),
    #                         "fechaRecepcion": data.get('fechaRecepcion'),
    #                         "horaRecepcion": data.get('horaRecepcion'),
    #                         "fechaAplicacion": data.get('fechaAplicacion'),
    #                         "horaAplicacion": data.get('horaAplicacion'),
    #                         "conciliacionId": data.get('conciliacionId'),
    #                         "codigoBancario": data.get('codigoBancario'),
    #                         "metodoDeposito": data.get('metodoDeposito')},
    #                        synchronize_session='fetch')
    #
    #             session.flush()
    #
    #             data['invId'] = inv_id
    #
    #             # check update correct
    #             row_updated = self.get_one_inversion(session, data)
    #
    #             logger.info('Data Updated: %s', str(row_updated))
    #
    #             if row_updated:
    #                 logger.info('Data Inversion updated')
    #
    #                 # session.commit()
    #
    #                 return json.dumps({
    #                     "cuenta": row_updated.cuenta,
    #                     "estatus": row_updated.estatus,
    #                     "monto": str(row_updated.monto),
    #                     "autorizacion": row_updated.autorizacion,
    #                     "canal": row_updated.canal,
    #                     "origen": row_updated.origen,
    #                     "comisionistaId": row_updated.comisionistaId,
    #                     "transaccionId": row_updated.transaccionId,
    #                     "motivo": row_updated.motivo,
    #                     "fechaRecepcion": row_updated.fechaRecepcion,
    #                     "horaRecepcion": row_updated.horaRecepcion,
    #                     "fechaAplicacion": row_updated.fechaAplicacion,
    #                     "horaAplicacion": row_updated.horaAplicacion,
    #                     "conciliacionId": row_updated.conciliacionId,
    #                     "codigoBancario": row_updated.codigoBancario,
    #                     "metodoDeposito": row_updated.metodoDeposito
    #                 })
    #
    #         except SQLAlchemyError as exc:
    #             session.rollback()
    #             logger.exception('An exception was occurred while execute transactions: %s', str(str(exc.args) + ':' +
    #                                                                                              str(exc.code)))
    #             raise mvc_exc.IntegrityError(
    #                 'Row not stored in "{}". IntegrityError: {}'.format(data.get('cuenta'),
    #                                                                     str(str(exc.args) + ':' + str(exc.code)))
    #             )
    #         finally:
    #             session.close()
