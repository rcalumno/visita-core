import unittest
from datetime import datetime

import pandas as pd
import pymongo
from bson.int64 import Int64
from pymongo import MongoClient


class EscenarioTestCase(unittest.TestCase):
    client = MongoClient("mongodb://localhost:27017/")
    client.visita_db.authenticate('roberto', 'admin', mechanism='SCRAM-SHA-1')
    database = client["visita_db"]
    collection = database["visita_col"]

    def test_transacciones_mes(self):
        query = {}
        query["RUC"] = Int64(100373885001)

        # informacion de la base
        cursor = self.collection.find(query).sort([['MES', pymongo.ASCENDING], ['TIPO_TRANSACCION', pymongo.ASCENDING]])
        # data frame en pandas
        data = pd.DataFrame(list(cursor))

        data_filtrado = data[['MES', 'NOMBRE', 'TIPO_TRANSACCION', 'MONTO']]

        print(data_filtrado)

        conteo = data_filtrado.groupby(['MES', 'NOMBRE', 'TIPO_TRANSACCION']).count()

        print(conteo)

    def test_costo_mes(self):
        query = {}
        query["RUC"] = Int64(100373885001)

        # informacion de la base
        cursor = self.collection.find(query).sort(
            [['MES', pymongo.ASCENDING], ['TIPO_TRANSACCION', pymongo.ASCENDING]])
        # data frame en pandas
        data = pd.DataFrame(list(cursor))

        data_filtrado = data[['MES', 'NOMBRE', 'TIPO_TRANSACCION', 'COSTO']]

        print(data_filtrado)

    def test_monto_mes(self):
        query = {}
        query["RUC"] = Int64(100373885001)

        # informacion de la base
        cursor = self.collection.find(query).sort(
            [['MES', pymongo.ASCENDING], ['TIPO_TRANSACCION', pymongo.ASCENDING]])
        # data frame en pandas
        data = pd.DataFrame(list(cursor))

        data_filtrado = data[['MES', 'NOMBRE', 'TIPO_TRANSACCION', 'MONTO']]

        print(data_filtrado)

    def test_transacciones_provincia_mes(self):
        query = {}
        # query["RUC"] = Int64(100373885001)
        query["MES"] = datetime(2017, 1, 1, 0, 0, 0)

        # informacion de la base
        cursor = self.collection.find(query)
        # data frame en pandas
        data = pd.DataFrame(list(cursor))

        data_filtrado = data[['PROVINCIA', 'MES', 'NOMBRE', 'TIPO_TRANSACCION', 'MONTO']]

        print(data_filtrado)

        conteo = data_filtrado.groupby(['PROVINCIA', 'MES', 'NOMBRE', 'TIPO_TRANSACCION']).count()

        print(conteo)
