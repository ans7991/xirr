import json
import csv

import bottle
from bottle import static_file, request
from pymongo import MongoClient

import transactionDAO
import counterDAO
import transactionService


@bottle.get('/transactions')
def get():
    return json.dumps(transactions.get_all())


@bottle.get('/transactions/<id>')
def get(id):
    return transactions.get(int(id))


@bottle.post('/transactions')
def insert():
    transactions.insert(request.json)
    counters.update()
    return {"message": "Your transaction has been saved successfully."}


@bottle.post('/transactions/<id>')
def update(id):
    transactions.update(int(id), request.json)
    return {"message": "Your transaction has been updated successfully."}


@bottle.delete('/transactions/<id>')
def delete(id):
    transactions.remove(int(id))
    return {"message": "Your transaction has been removed successfully."}


@bottle.get('/currentId')
def get_current_id():
    return counters.get()


@bottle.get('/summary')
def summary():
    return service.calculate_summary(request.query.amount)


@bottle.post('/upload')
def upload():
    data = request.files.get('upload')
    reader = csv.DictReader(data.file, delimiter=',')
    service.upload(reader)
    return {"message": "File uploaded successfully."}


@bottle.get('/')
def welcome():
    return static_file('index.html', root='./static')


@bottle.get('/static/<subdir>/<file>')
def serve_static(file, subdir):
    return static_file(file, root='./static/' + subdir)


@bottle.get('/static/<subdir>/libs/<file>')
def serve_static(file, subdir):
    return static_file(file, root='./static/' + subdir + '/libs')


connectionURL = "mongodb://localhost"
connection = MongoClient(connectionURL)
database = connection.stocks

transactions = transactionDAO.TransactionDAO(database)
counters = counterDAO.CounterDAO(database)
service = transactionService.TransactionService(transactions, counters)

bottle.run(host="localhost", port="8085", reloader=True)
