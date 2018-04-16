from pymongo import MongoClient


class VisitaMongoClient:
    __instance = None
    client = MongoClient()
    db = client['visita_client']

    def __init__(self):
        """ Virtually private constructor. """
        if VisitaMongoClient.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            VisitaMongoClient.__instance = self

    @staticmethod
    def getInstance():
        if VisitaMongoClient.__instance is None:
            VisitaMongoClient()
        return VisitaMongoClient.__instance

    def insert(self, document):

        coll = self.db['client_db']
        doc_id = coll.insert_one(document).inserted_id
        print(doc_id)
