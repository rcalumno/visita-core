from pymongo import MongoClient


class VisitaMongoClient:
    __instance = None
    client = MongoClient()

    client.visita_db.authenticate('roberto', 'admin', mechanism='SCRAM-SHA-1')

    db = client['visita_db']

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

        coll = self.db['visita']
        doc_id = coll.insert_one(document).inserted_id
        print(doc_id)
