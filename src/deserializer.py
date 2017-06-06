from datetime import datetime
from src.models import Transaction


TRANSACTION_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def to_transactions(json_dict):
    if 'transaction-id' in json_dict:
        if 'transaction-time' in json_dict:
            # Convert to datetime object
            json_dict['transaction-time'] = datetime.strptime(json_dict['transaction-time'], TRANSACTION_DATETIME_FORMAT)
        return Transaction(json_dict)
    return json_dict
