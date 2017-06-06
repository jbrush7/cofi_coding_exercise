#TODO: README/etc
#TODO: Creds.py - remove
#TODO: push

class Transaction(object):
    """ A single transaction """
    def __init__(self, transaction_dict):
        self.amount = transaction_dict.get('amount')
        self.categorization = transaction_dict.get('categorization')
        self.transaction_id = transaction_dict.get('transaction-id')
        self.datetime = transaction_dict.get('transaction-time')
        self.merchant = transaction_dict.get('merchant')
        self.raw_merchant = transaction_dict.get('raw-merchant')
        self.is_pending = transaction_dict.get('is-pending', False)

    def __str__(self):
        return u'{date:%Y-%m-%d}|{merchant}: {amount}'.format(date=self.datetime, merchant=self.merchant, amount=self.amount)

