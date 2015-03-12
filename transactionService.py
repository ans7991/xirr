import transaction
import time

DAYS_IN_YEAR = 365

COMM_BUY_FACTOR = 1 + .0067
COMM_SELL_FACTOR = 1 - .0067
SECONDS_IN_ONE_DAY = 3600 * 24
GUESS = 0.1
DATE_FORMAT = "%Y-%m-%d"


class TransactionService():
    def __init__(self, transactions, counters):
        self.transactions = transactions
        self.counters = counters

    def calculate_xirr(self, current_worth):
        amounts = []
        days = []
        transactions = self.transactions.get_all()
        first_date = time.mktime(time.strptime(transactions[0]['date'], DATE_FORMAT))

        for txn in transactions:
            txn = transaction.Transaction(txn)
            if txn.type == "BUY":
                amounts.append(calc_buy_amount(txn))
            else:
                amounts.append(calc_sell_amount(txn))
            days.append(calc_day_diff(first_date, txn.date))

        amounts.append(float(current_worth))
        days.append(calc_day_diff(first_date, time.strftime(DATE_FORMAT)))

        return newton(GUESS, amounts, days)

    def upload(self, reader):
        for row in reader:
            row['id'] = int(self.counters.get()['seq'])
            row['price'] = float(row['price'])
            row['quantity'] = float(row['quantity'])
            self.transactions.insert(row)
            self.counters.update()


def function_of_dx(x, amounts, days):
    sum = 0.0
    for i, amount in enumerate(amounts):
        sum += ((-days[i] / DAYS_IN_YEAR) * amount * ((1 + x) ** ((-days[i] / DAYS_IN_YEAR) - 1)))
    return sum


def function_of_x(x, amounts, days):
    sum = 0.0
    for i, amount in enumerate(amounts):
        sum += (amount * ((1 + x) ** (-days[i] / DAYS_IN_YEAR)))
    return sum


def newton(x, amounts, days):
    for i in range(0, 100):
        x -= function_of_x(x, amounts, days) / function_of_dx(x, amounts, days)
    return round(x * 100, 2)


def calc_buy_amount(txn):
    return round((-int(txn.quantity) * float(txn.price) * COMM_BUY_FACTOR), 2)


def calc_sell_amount(txn):
    return round((int(txn.quantity) * float(txn.price) * COMM_SELL_FACTOR), 2)


def calc_day_diff(first_date, date):
    return float((time.mktime(time.strptime(date, DATE_FORMAT)) - first_date) / SECONDS_IN_ONE_DAY)
