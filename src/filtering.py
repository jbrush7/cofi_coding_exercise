from operator import attrgetter
from datetime import timedelta

DONUT_MERCHANTS = [
    'Dunkin #336784',
    'Krispy Kreme Donuts'
    ]

def is_donut(transation):
    return transation.raw_merchant in DONUT_MERCHANTS

def is_cc_transaction(transaction):
    try:
        return transaction.is_cc_transaction
    except AttributeError:
        return False

def annotate_cc_transations(transactions):
    """
    This looks for 2 offsetting transactions within a 24 hour period and annotates them as a credit card transaction.

    Basically it walk a list of transactions once, keeping track of today's and yesterday's transactions. At the end of each day
    we check to see if an inverse transaction (amount * -1) exists in either today's or yesterday's collection. If we find
    any matches we'll annotate the transactions.

    """
    transactions.sort(key=attrgetter('datetime')) # API doesn't promise sorting, so we are being defensive.
    current_date = None
    yesterdays_transactions = {}
    todays_transactions = {}
    for trans in transactions:
        # Amount is zero, an offsetting transaction doesn't make sense
        if trans.amount == 0:
            continue

        # Update yesterday's/today's transactions
        if trans.datetime.date() == current_date:
            todays_transactions[trans.amount] = trans
        elif current_date and trans.datetime.date() > current_date + timedelta(days=1):
            # More than 1 day separating the transactions
            yesterdays_transactions = {}
            todays_transactions = {}
            current_date = trans.datetime.date()
            todays_transactions[trans.amount] = trans
        else:
            # 1 day or less separates the transactions
            yesterdays_transactions = todays_transactions
            todays_transactions = {}
            current_date = trans.datetime.date()
            todays_transactions[trans.amount] = trans

        # Annotate transactions if needed
        inverse_amount = -1 * trans.amount
        if inverse_amount in todays_transactions:
            trans.is_cc_transaction = True
            todays_transactions[inverse_amount].is_cc_transaction = True
        elif inverse_amount in yesterdays_transactions:
            trans.is_cc_transaction = True
            yesterdays_transactions[inverse_amount].is_cc_transaction = True
