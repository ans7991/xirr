class CounterDAO:
	
	def __init__(self, database):
		self.db = database
		self.counters = self.db.counters

	def get(self):
		return self.counters.find_one({"_id": "txn_id"}, {"_id": False})

	def update(self):
		self.counters.update({"_id": "txn_id"}, {"$inc": {"seq": 1}}, new = "true")