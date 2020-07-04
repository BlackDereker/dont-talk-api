from flask_restful import Resource

class Ping(Resource):
    def get(self):
        data = {"status": "OK"}
        return data, 200