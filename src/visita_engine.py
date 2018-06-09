import pandas as pd

from visita_mongo_client import VisitaMongoClient


class VisitaEngine:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if VisitaEngine.__instance is None:
            VisitaEngine()
        return VisitaEngine.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if VisitaEngine.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            VisitaEngine.__instance = self

    def leer_achivo(self, ruta_documento, nombre_hoja):
        if ruta_documento is None:
            return ['test']

        print("leyendo archivo {} ", ruta_documento)

        excel_file = pd.ExcelFile(ruta_documento)
        hoja = excel_file._parse_excel(nombre_hoja)

        for index, row in hoja.iterrows():
            print(str(row[0]) + " - " + str(row[1]) + " - " + str(row[9]))

            doc = {
                "RUC": row[0],
                "NOMBRE": row[1],
                "TIPO_TRANSACCION": row[9],
                "CONTEO_TRANSACCION": row[11],
                "MONTO": row[12],
                "COSTO": row[17],
                "COMISION": row[18],
                "RESULTADO": row[19],
                "ZONA": row[3],
                "PROVINCIA": row[4],
                "CANTON": row[5],
                "EJECUTIVO": row[15],
                "SUPERVISOR": row[16],
                "MES": row[14],
            }

            VisitaMongoClient.getInstance().insert(doc)
        return excel_file.sheet_names
