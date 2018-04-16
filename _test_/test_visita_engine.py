import unittest

from visita_engine import VisitaEngine


class VisitaTestCase(unittest.TestCase):
    def test_visita_engine_existen_hojas(self):
        excel_archive = VisitaEngine.getInstance().leer_achivo(
            ".././src/resources/VISITA_TEST.xlsx")
        self.assertIsNotNone(excel_archive)
        print(excel_archive)
