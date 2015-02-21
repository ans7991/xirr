class Transaction(object):
    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, v)
