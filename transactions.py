import bottle
import json
import pymongo
from bottle import static_file, request
from pymongo import MongoClient

@bottle.get('/transactions')
def get():
    conn = MongoClient('localhost', 27017)
    transactions = conn.stocks.transactions
    transaction_list = []
    for transaction in transactions.find({}, {"_id": False}).sort("id", pymongo.ASCENDING):
        transaction_list.append(transaction)
    return json.dumps(transaction_list)

@bottle.get('/transactions/<id>')
def get(id):
    conn = MongoClient('localhost', 27017)
    transactions = conn.stocks.transactions
    return transactions.find_one({"id": id}, {"_id": False})

@bottle.post('/transactions')
def insert():
    conn = MongoClient('localhost', 27017)
    transactions = conn.stocks.transactions
    counters = conn.stocks.counters
    transactions.insert(request.json)
    counters.update({"_id": "txn_id"}, {"$inc": {"seq": 1}}, new = "true")
    return {"message": "Your transaction has been saved successfully."}

@bottle.post('/transactions/<id>')
def update(id):
    conn = MongoClient('localhost', 27017)
    transactions = conn.stocks.transactions
    transactions.update({"id": id}, request.json)
    return {"message": "Your transaction has been updated successfully."}

@bottle.delete('/transactions/<id>')
def delete(id):
    conn = MongoClient('localhost', 27017)
    transactions = conn.stocks.transactions
    transactions.remove({"id": int(id)})
    print id
    return {"message": "Your transaction has been removed successfully."}

@bottle.get('/currentId')
def get():
    conn = MongoClient('localhost', 27017)
    counters = conn.stocks.counters
    return counters.find_one({"_id": "txn_id"}, {"_id": False})

@bottle.get('/')
def welcome():
    return static_file('index.html', root='./static')

@bottle.get('/static/<subdir>/<file>')
def serve_static(file, subdir):
    return static_file(file, root='./static/'+subdir)

@bottle.get('/static/<subdir>/libs/<file>')
def serve_static(file, subdir):
    return static_file(file, root='./static/'+subdir+'/libs')

bottle.run(host="localhost", port="8085", reloader=True)

