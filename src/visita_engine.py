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

    def leer_achivo(self, ruta_documento):
        if ruta_documento is None:
            return ['test']

        print("leyendo archivo {} ", ruta_documento)

        excel_file = pd.ExcelFile(ruta_documento)
        hoja = excel_file._parse_excel("BITACORA")

        for index, row in hoja.iterrows():
            print(str(row[5]) + " - " + str(row[7]) + " - " + str(row[8]))

            doc = {
                "ESPECIALISTA": row[5],
                "FECHA": row[7],
                "HORA": row[8],
                # more fields
            }

            VisitaMongoClient.getInstance().insert(doc)
        return excel_file.sheet_names
