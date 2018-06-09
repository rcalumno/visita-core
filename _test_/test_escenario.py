import unittest

import pandas as pd
import pymongo
from bson.int64 import Int64
from pymongo import MongoClient


class EscenarioTestCase(unittest.TestCase):

    def test_transacciones_mes(self):
        client = MongoClient("mongodb://localhost:27017/")
        client.visita_db.authenticate('roberto', 'admin', mechanism='SCRAM-SHA-1')
        database = client["visita_db"]
        collection = database["visita_col"]
        query = {}
        query["RUC"] = Int64(100373885001)

        # informacion de la base
        cursor = collection.find(query).sort([['MES', pymongo.ASCENDING], ['TIPO_TRANSACCION', pymongo.ASCENDING]])
        # data frame en pandas
        data = pd.DataFrame(list(cursor))

        data_filtrado = data[['MES', 'NOMBRE', 'TIPO_TRANSACCION', 'MONTO']]

        print(data_filtrado)

        conteo = data_filtrado.groupby(['MES', 'TIPO_TRANSACCION']).count()

        print(conteo)
