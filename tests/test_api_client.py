from mock import patch, Mock, DEFAULT
from unittest import TestCase
from datetime import date
from src.api_client import _fetch_transations, _error_check
from src.api_client import get_current_transations, get_projected_transations, get_current_and_projected_transations
from src.api_client import ALL_TRANSATIONS_ENDPOINT, PROJECTED_TRANSACTIONS_ENDPOINT, DATA

class TestFeching(TestCase):
    def setUp(self):
        self.patcher = patch.multiple('src.api_client', requests=DEFAULT, json=DEFAULT)
        self.mocks = self.patcher.start()
        self.mock_response = Mock()
        self.mocks['requests'].post.return_value = self.mock_response

    def tearDown(self):
        self.patcher.stop()

    def test_fetch_tries_to_deserialize(self):
        data = "{'errors': 'no-errors', 'transactions': []}"
        self.mock_response.text = "{'errors': 'no-errors', 'transactions': []}"
        transactions, error = _fetch_transations('http://test.url', {})
        assert self.mocks['json'].loads.called_with(data)

class TestErrorChecking(TestCase):

    def test_error_check(self):
        data = {u'error': u'no-error'}
        assert _error_check(data) is None

        data = {u'error': u'networking-failure'}
        assert _error_check(data) == u'networking-failure'

        data = {}
        assert _error_check(data) == u'malformed response'


class TestGetTransactions(TestCase):
    def setUp(self):
        self.patcher = patch.multiple('src.api_client', _fetch_transations=DEFAULT)
        self.mocks = self.patcher.start()
        self.mock_fetch = Mock()
        self.mocks['_fetch_transations'].return_value = self.mock_fetch

    def tearDown(self):
        self.patcher.stop()

    def test_get_current_transations(self):
        get_current_transations()
        self.mocks['_fetch_transations'].assert_called_with(ALL_TRANSATIONS_ENDPOINT, DATA)

    def test_get_projected_transations(self):
        get_projected_transations()
        expected_data = dict(DATA)
        #
        today = date.today()
        expected_data.update({'year': today.year, 'month': today.month})

        self.mocks['_fetch_transations'].assert_called_with(PROJECTED_TRANSACTIONS_ENDPOINT, expected_data)

    @patch('src.api_client.get_current_transations')
    @patch('src.api_client.get_projected_transations')
    def test_get_current_and_projected_transations(self, mock_get_current_transations, mock_get_projected_transations):
        mock_get_current_transations.return_value = ['a'], None
        mock_get_projected_transations.return_value =['b'], None

        transactions, errors = get_current_and_projected_transations()
        assert transactions == ['b', 'a']
        assert errors is None

        mock_get_current_transations.return_value = ['a'], 'error'
        mock_get_projected_transations.return_value =['b'], None

        transactions, errors = get_current_and_projected_transations()
        assert transactions == []
        assert errors == u'failed to get all transactions'


        mock_get_current_transations.return_value = ['a'], None
        mock_get_projected_transations.return_value =['b'], 'error'

        transactions, errors = get_current_and_projected_transations()
        assert transactions == []
        assert errors == u'failed to get all transactions'
