from http import client
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

from sqlalchemy import PrimaryKeyConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://host:port/clientsDb'
db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(50))
    razao = db.Column(db.String(50))
    cnpj = db.Column(db.String(50))
    date = db.Column(db.DateTime)

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "razao": self.razao, "cnpj": self.cnpj, "data": self.date }

db.create_all()

#--------selecionar---------#
@app.route("/clients", methods=["GET"])
def selectClients():
    clientsObjects = Client.query.all()
    clientsJsons  = [client.to_json() for client in clientsObjects]

    return Response(json.dumps(clientsJsons))

#-----selecionar um-------#
@app.route("/client/<id>", methods=["GET"])
def selectOneClient(id):
    clientObject = client.query.filter_by(id=id).first()
    clientJson = clientObject.to_json()

    return gera_response(200, "Cliente", clientJson)

#------cadastrar---------#
@app.route("/client", methods=["POST"])
def createClient():
    body = request.get_json()

    try:
        client = Client(nome=body["nome"], razao= body["razao"], cnpj = body["cnpj"], date = body["date"])
        db.session.add(client)
        db.session.commit()
        return gera_response(201, "Cliente", client.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Cliente", {}, "Erro ao cadastrar")


#-----------atualizar---------#
@app.route("/client/<id>", methods=["PUT"])
def clientUpdate(id):
    clientObject = client.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            clientObject.nome = body['nome']
        if('razao' in body):
            clientObject.razao = body['razao']
        if('cnpj' in body):
            clientObject.cnpj = body['cnpj']

        
        db.session.add(clientObject)
        db.session.commit()
        return gera_response(200, "Cliente", clientObject.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Cliente", {}, "Erro ao atualizar")


# Deletar
@app.route("/client/<id>", methods=["DELETE"])
def deleteClient(id):
    clientObject = Client.query.filter_by(id=id).first()

    try:
        db.session.delete(clientObject)
        db.session.commit()
        return gera_response(200, "Cliente", clientObject.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Cliente", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")



app.run()