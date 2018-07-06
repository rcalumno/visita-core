import unittest

import pandas as pd
from bson.int64 import Int64
from pymongo import MongoClient


class EscenarioGenericoTestCase(unittest.TestCase):
    client = MongoClient("mongodb://localhost:27017/")
    # client.visita_db.authenticate('roberto', 'admin', mechanism='SCRAM-SHA-1')
    database = client["visita_db"]
    collection = database["visita_col"]
    directorio_base = "D:/home/"

    def test_generar_escenario(self):
        filtro = {"RUC": Int64(100373885001), "TIPO_TRANSACCION": "Recargas"}
        ordenacion = [(u"MES", 1), (u"TIPO_TRANSACCION", -1)]
        # columnas_accion = ['MES', 'NOMBRE', 'TIPO_TRANSACCION', 'MONTO']
        columnas_accion = ['MES', 'MONTO']
        nombre_escenario = "numero_transacciones_mes_ruc"
        agrupar_por = columnas_accion[0:len(columnas_accion) - 1]
        self.funcion_generica(
            filtro,
            ordenacion,
            columnas_accion,
            agrupar_por,
            nombre_escenario,
            2
        )

    def funcion_generica(self, filtrar_por, ordenar_por, columnas_accion, agrupar_por, nombre_escenario, meses_atras):
        query = filtrar_por

        file_name = self.directorio_base + nombre_escenario + ".csv"
        # informacion de la base
        cursor = self.collection.find(query, sort=ordenar_por)
        # data frame en pandas
        self.procesar_data_frame_pandas(columnas_accion, cursor, agrupar_por, meses_atras, file_name)

    def procesar_data_frame_pandas(self, columnas, cursor, agrupar_por, meses_atras, file_name):
        # data frame en pandas
        df_base = pd.DataFrame(list(cursor))
        # Seleccionamos solo las columnas que necesitamos
        df_filtrado_columnas = df_base[columnas]

        df_filtrado_columnas['MES'] = pd.to_datetime(df_filtrado_columnas['MES'])

        # print(data_filtrado)
        df_resultado = df_filtrado_columnas
        if agrupar_por:
            # agrupamos los elementos por el ultimo criterio
            df_agrupado = df_filtrado_columnas.groupby(agrupar_por).count()

            # Renombramos la ultima cabecera ya que toma el nombre de la columna en cuestion
            df_agrupado.rename(columns={columnas[len(columnas) - 1]: 'TOTAL'}, inplace=False)

            df_resultado = df_agrupado
            # print(df_resultado)

        proyeccion = pd.DataFrame(df_resultado)

        for x in range(0, meses_atras):
            nombre = "COL-" + str(meses_atras-x)
            proyeccion.insert(loc=x, column=nombre, value=pd.np.nan)

        # print(proyeccion)

        for x in range(0, meses_atras):
            proyeccion.loc[:,'COL-'+str(1)]=[1, 2, 3, 4, 6, 7, 8, 9]

        print(proyeccion)
                # for index, row in df_resultado.iteritems():
        #     print(row.values)




        # Exportacion de los datos a csv
        # df_resultado.transpose().to_csv(file_name, sep='\t', encoding='utf-8')
