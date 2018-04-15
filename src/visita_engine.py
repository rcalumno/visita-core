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
        print ("leyendo archivo {} ", ruta_documento)
