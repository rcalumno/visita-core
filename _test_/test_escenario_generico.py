import unittest

import numpy as np
import pandas as pd
from bson.int64 import Int64
from pymongo import MongoClient


class EscenarioGenericoTestCase(unittest.TestCase):
    client = MongoClient("mongodb://localhost:27017/")
    client.visita_db.authenticate('roberto', 'admin', mechanism='SCRAM-SHA-1')
    database = client["visita_db"]
    collection = database["visita_col"]
    directorio_base = "/home/roberto/salida_escenario/"

    def test_generar_escenario(self):
        filtro = {"RUC": Int64(100373885001), "TIPO_TRANSACCION": "Recargas"}
        ordenacion = [(u"MES", 1), (u"TIPO_TRANSACCION", -1)]
        columnas_accion = ['MES', 'MONTO']
        nombre_escenario = "escenario_1"
        agrupar_por = columnas_accion[0:len(columnas_accion) - 1]

        self.generar_escenario_generico(
            filtro,
            ordenacion,
            columnas_accion,
            agrupar_por,
            nombre_escenario,
            2, False
        )

        filtro = {"EJECUTIVO": "CAJAMARCA MIRANDA ANGEL HERIBERTO", "TIPO_TRANSACCION": "Recargas"}
        ordenacion = [(u"MES", 1), (u"TIPO_TRANSACCION", -1)]
        columnas_accion = ['MES', 'COSTO']
        nombre_escenario = "escenario_2"
        agrupar_por = columnas_accion[0:len(columnas_accion) - 1]

        self.generar_escenario_generico(
            filtro,
            ordenacion,
            columnas_accion,
            agrupar_por,
            nombre_escenario,
            4, False
        )

        filtro = {"RUC": Int64(100373885001), "TIPO_TRANSACCION": "Recargas"}
        ordenacion = [(u"MES", 1), (u"TIPO_TRANSACCION", -1)]
        columnas_accion = ['MES', 'MONTO', 'RESULTADO']
        nombre_escenario = "escenario_3"
        agrupar_por = None

        self.generar_escenario_generico(
            filtro,
            ordenacion,
            columnas_accion,
            agrupar_por,
            nombre_escenario,
            4, True
        )

    def generar_escenario_generico(self, filtrar_por, ordenar_por, columnas_accion, agrupar_por, nombre_escenario,
                                   meses_atras, borrar_na):
        query = filtrar_por

        file_name = self.directorio_base + nombre_escenario + ".csv"
        # informacion de la base
        cursor = self.collection.find(query, sort=ordenar_por)
        # data frame en pandas
        self.procesar_data_frame_pandas(columnas_accion, cursor, agrupar_por, meses_atras, file_name, borrar_na)

    def procesar_data_frame_pandas(self, columnas, cursor, agrupar_por, meses_atras, file_name, borrar_na):
        numero_columnas = len(columnas)

        # data frame en pandas
        df_base = pd.DataFrame(list(cursor))

        # Seleccionamos solo las columnas que necesitamos
        df_filtrado_columnas = df_base[columnas]

        df_filtrado_columnas['MES'] = pd.to_datetime(df_filtrado_columnas['MES'])

        df_resultado = df_filtrado_columnas
        if agrupar_por:
            # agrupamos los elementos por el ultimo criterio
            df_agrupado = df_filtrado_columnas.groupby(agrupar_por).count()

            # Renombramos la ultima cabecera ya que toma el nombre de la columna en cuestion
            df_agrupado.rename(columns={columnas[len(columnas) - 1]: 'TOTAL'}, inplace=False)

            df_resultado = df_agrupado

        print(df_resultado)

        # Convertimos la agrupacion en un dataframe
        proyeccion = pd.DataFrame(df_resultado)

        numero_filas = proyeccion.shape[0]
        print("Numero de filas    : " + str(numero_filas))
        print("Numero de columnas : " + str(numero_columnas))

        # Con esta instruccion tomamos los valores resultantes para poder proyectarlos
        columna_accion = self.obtenerUltimaColumna(proyeccion, -1)
        self.proyectar_datos(proyeccion, columna_accion, meses_atras, numero_filas, "A")

        # if numero_columnas > 2:
        # columna_accion2 = self.obtenerUltimaColumna(proyeccion, len(columnas) - 1)
        # self.proyectar_datos(proyeccion, columna_accion2, meses_atras, numero_filas, "B")

        print("\n\n###########################################################")
        print("DataFrame Resultante")
        if borrar_na:
            proyeccion.dropna(inplace=True)
        print(proyeccion)
        print("###########################################################")

        # Exportacion de los datos a csv
        df_resultado.dropna().to_csv(file_name, sep='\t', encoding='utf-8')

    def proyectar_datos(self, data_frame_tmp, columna_accion, meses_atras, numero_filas, prefijo):
        # Con esta instruccion tomamos los valores resultantes para poder proyectarlos
        print("Columna de accion  :" + str(columna_accion))

        for x_meses in range(meses_atras, 0, -1):
            nombre = prefijo + "-COL-" + str(x_meses)

            columnas_insercion = np.array([])
            elementos_iterados: int = 0
            for y_elementos in range(0, numero_filas):
                if y_elementos > (x_meses - 1):
                    columnas_insercion = np.append(columnas_insercion, columna_accion[y_elementos - elementos_iterados])
                else:
                    columnas_insercion = np.append(columnas_insercion, [pd.np.nan])
                    elementos_iterados += 1

            data_frame_tmp.insert(loc=(meses_atras - x_meses), column=nombre, value=columnas_insercion)

    def obtenerUltimaColumna(self, data_frame_tmp, columna):
        return pd.Series(data_frame_tmp.values[:, columna], name=data_frame_tmp.columns[columna]).values
