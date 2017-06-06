import requests
import json
from datetime import date
from src.deserializer import to_transactions
from creds import UID, TOKEN, API_TOKEN

ALL_TRANSATIONS_ENDPOINT = 'https://2016.api.levelmoney.com/api/v2/core/get-all-transactions'
PROJECTED_TRANSACTIONS_ENDPOINT = 'https://2016.api.levelmoney.com/api/v2/core/projected-transactions-for-month'

HEADERS = {
    'Accept': 'text/plain',
    'User-Agent': 'JBR Spider (www.john-rush.com)',
}

DATA = {
    "args": {
        "uid": UID,
        "token": TOKEN,
        "api-token": API_TOKEN,
        "json-strict-mode": False,
        "json-verbose-response": False,
    }
}

ERROR_FIELD_NAME = u'error'
OK_ERROR_STATUS = u'no-error'
TRANSATIONS_FIELD_NAME = u'transactions'

def _fetch_transations(url, request_data):
    """
    Makes api requests.

    We could implement caching here if needed.

    Returns:
        (transactions_list, error_dict). error_dict is None when successful
    """
    try:
        r = requests.post(url, json=request_data, headers=HEADERS)
        r.raise_for_status()
        raw_data = r.text
        data = json.loads(raw_data, object_hook=to_transactions)
    except requests.exceptions.RequestException:
        # Here we can handle Timeouts/503s/DNS failures/etc. For now report general failure.
        data = {ERROR_FIELD_NAME: u'networking-failure'}
    return data.get(TRANSATIONS_FIELD_NAME, []), _error_check(data)

def _error_check(data):
    """
    Check for errors in the api results
    """
    if data.get(ERROR_FIELD_NAME) == OK_ERROR_STATUS:
        return None
    return data.get(ERROR_FIELD_NAME, 'malformed response')

def get_current_transations():
    """
    Fetch current transactions.

    Returns:
        (transactions_list, error_dict). error_dict is None when successful
    """

    url = ALL_TRANSATIONS_ENDPOINT
    request_data = dict(DATA)
    return _fetch_transations(url, request_data)

def get_projected_transations():
    """
    Fetch projected transactions.

    Returns:
        (transactions_list, error_dict). error_dict is None when successful
    """

    url = PROJECTED_TRANSACTIONS_ENDPOINT
    request_data = dict(DATA)
    today = date.today()
    request_data.update({'year': today.year, 'month': today.month})
    return _fetch_transations(url, request_data)

def get_current_and_projected_transations():
    """
    Fetch current and pending transactions and combine into a single transaction list.

    Returns:
        (transactions_list, error_dict). error_dict is None when successful
    """
    current_transations, current_errors = get_current_transations()
    projected_transations, projected_errors = get_projected_transations()
    if current_errors is None and projected_errors is None:
        current_transations.extend(projected_transations)
        return current_transations, current_errors
    else:
        # Could be more helpful
        return [], u'failed to get all transactions'

