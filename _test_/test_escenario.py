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

    def test_generar_escenario(self):
        self.funcion_generica(['MES', 'NOMBRE', 'TIPO_TRANSACCION', 'MONTO'],
                              "numero_transacciones_mes_ruc", {"RUC": Int64(100373885001)}, None)

        self.funcion_generica(['NOMBRE', 'TIPO_TRANSACCION', 'MONTO'],
                              "numero_transacciones_ruc_anio", {"RUC": Int64(100373885001)},
                              [['MES', pymongo.ASCENDING], ['TIPO_TRANSACCION', pymongo.ASCENDING]])

        self.funcion_generica(['PROVINCIA', 'MES', 'NOMBRE', 'TIPO_TRANSACCION', 'MONTO'],
                              "numero_transacciones_provincia", {}, None)


    def funcion_generica(self, columnas, tipo_escenario, filtrar_por, ordenar_por):
        """
        Permite generar un escenario especifico en fncion a los parametros que pasamos al metodo
        :param columnas: Columnas sobre las cuales vamos a trabajar dentro del universo de datos en nuestra tabla de mongo
        :param tipo_escenario: nombre cidentificativo del escenario que estamos construyendo
        :param filtrar_por: /*arreglo*/ filtro de busqueda que determina que elementos buscar en la base mongo
        :param ordenar_por: /*arreglo*/ permite ordenar la colleccion de datos resultante por los criterios enviados
        :return:
        """
        query = filtrar_por

        if "MES" in columnas:
            for x in range(1, 12):
                query["MES"] = datetime(2017, x, 1, 0, 0, 0)
                file_name = "/home/roberto/salida_escenario/" + tipo_escenario + "_Mes_" + str(x) + ".csv"
                # informacion de la base
                cursor = self.collection.find(query)
                # data frame en pandas
                self.procesar_data_frame_pandas(columnas, cursor, file_name)
        else:

            file_name = "/home/roberto/salida_escenario/" + tipo_escenario + ".csv"

            # informacion de la base
            cursor = self.collection.find(query).sort(ordenar_por)
            # data frame en pandas
            self.procesar_data_frame_pandas(columnas, cursor, file_name)


    def procesar_data_frame_pandas(self, columnas, cursor, file_name):
        """
        Permite ttransformar el cursos de pymongo a un data frame de pandas, para poder exportarlo a excel
        :param columnas: columnas sobre las cuales se trabajara, puesto que el cursos de mongo retorna todas las columnas existentes en la tabla
        :param cursor: corresponde al set de datos que retorno el mongo
        :param file_name: nombre de archivo con el cual se generarar el escenario
        :return:
        """
        # data frame en pandas
        data = pd.DataFrame(list(cursor))
        #Seleccionamos solo las columnas que necesitamos
        data_filtrado = data[columnas]

        # print(data_filtrado)
        # agrupamos los elementos por el ultimo criterio
        conteo = data_filtrado.groupby(columnas[0:len(columnas) - 1]).count()

        #Renombramos la ultima cabecera ya que toma el nombre de la columna en cuestion
        conteo.rename(columns={columnas[len(columnas) - 1]: 'TOTAL'}, inplace=True)
        print(conteo)
        # Exportacion de los datos a csv
        conteo.to_csv(file_name, sep='\t', encoding='utf-8')