import pymongo


class TransactionDAO:
    def __init__(self, database):
        self.db = database
        self.transactions = self.db.transactions

    def insert(self, transaction):
        self.transactions.insert(transaction)

    def remove(self, id):
        self.transactions.remove({"id": id})

    def get(self, id):
        return self.transactions.find_one({"id": id}, {"_id": False})

    def update(self, id, transaction):
        self.transactions.update({"id": id}, transaction)

    def get_all(self):
        transaction_list = []
        for transaction in self.transactions.find({}, {"_id": False}).sort("id", pymongo.ASCENDING):
            transaction_list.append(transaction)
        return transaction_list