from flask import Flask
from flask_restplus import Api, Resource, request

from instance import server
app, api = server.app, server.api

client_db = [
    {'id': 0, 'name': 'David Ian', 'razao': 'asnanas', 'cnpj': '00000000000', "date": '07/07/2022'},
    {'id': 1, 'name': 'Larissa Acioly', 'razao': 'asaosj', 'cnpj': '1111111111', "date": '07/07/2022'},
    {'id': 0, 'name': 'Julio Pereira', 'razao': 'bhbddhd', 'cnpj': '22222222222', "date": '07/07/2022'},

]
class ClientList(Resource):
    def get(self, ):
        return client_db
    def post(self, ):
        response = api.payload
        client_db.append(response)
        return response, 200