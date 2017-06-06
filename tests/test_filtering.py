from unittest import TestCase

from src.filtering import is_donut, is_cc_transaction
from src.filtering import annotate_cc_transations
from src.models import Transaction
from datetime import datetime

class TestFiltering(TestCase):
    def test_is_donut(self):
        """ Check to see if transactions match known donut merchants """
        not_donut_transaction = Transaction({
            'raw-merchant': 'NOT DONUT',
        })

        donut_a_transaction = Transaction({
            'raw-merchant': 'Dunkin #336784',
        })

        donut_b_transaction = Transaction({
            'raw-merchant': 'Krispy Kreme Donuts',
        })

        assert not is_donut(not_donut_transaction)
        assert is_donut(donut_a_transaction)
        assert is_donut(donut_b_transaction)

    def test_is_cc_transaction(self):
        not_cc_transaction = Transaction({})
        assert not is_cc_transaction(not_cc_transaction)

        explictly_not_cc_transaction = Transaction({})
        explictly_not_cc_transaction.is_cc_transaction = False
        assert not is_cc_transaction(explictly_not_cc_transaction)

        cc_transaction = Transaction({})
        cc_transaction.is_cc_transaction = True
        assert is_cc_transaction(cc_transaction)

class TestAnnotations(TestCase):
    def test_no_transactions(self):
        transactions = []
        annotate_cc_transations(transactions)
        for transaction in transactions:
            assert not transaction.is_cc_transaction

    def test_no_amounts_match(self):
        transactions = [
            Transaction({
                'amount': 100,
                'transaction-time': datetime(year=2017, month=6, day=6)
            }),
            Transaction({
                'amount': -200,
                'transaction-time': datetime(year=2017, month=6, day=6)
            }),
            Transaction({
                'amount': -5,
                'transaction-time': datetime(year=2017, month=6, day=6)
            }),
            Transaction({
                'amount': 50,
                'transaction-time': datetime(year=2017, month=6, day=6)
            }),
            ]
        annotate_cc_transations(transactions)
        for transaction in transactions:
            assert not is_cc_transaction(transaction)

    def test_amounts_match_but_greater_than_24_hours(self):
        transactions = [
            Transaction({
                'amount': 100,
                'transaction-time': datetime(year=2017, month=6, day=1)
            }),
            Transaction({
                'amount': -100,
                'transaction-time': datetime(year=2017, month=6, day=6)
            }),
            Transaction({
                'amount': -5,
                'transaction-time': datetime(year=2017, month=6, day=10)
            }),
            Transaction({
                'amount': 50,
                'transaction-time': datetime(year=2017, month=6, day=10)
            }),
            ]
        annotate_cc_transations(transactions)
        for transaction in transactions:
            print transaction.amount, transaction.datetime
            assert not is_cc_transaction(transaction)

    def test_same_day_transactions(self):
        matching_transactions = [
            Transaction({
                'amount': 100,
                'transaction-time': datetime(year=2017, month=6, day=1)
            }),
            Transaction({
                'amount': -100,
                'transaction-time': datetime(year=2017, month=6, day=1)
            }),
        ]
        no_match_transactions = [
            Transaction({
                'amount': -5,
                'transaction-time': datetime(year=2017, month=6, day=10)
            }),
            Transaction({
                'amount': 50,
                'transaction-time': datetime(year=2017, month=6, day=10)
            }),
        ]
        transactions = no_match_transactions + matching_transactions

        annotate_cc_transations(transactions)
        for transaction in no_match_transactions:
            assert not is_cc_transaction(transaction)
        for transaction in matching_transactions:

            assert is_cc_transaction(transaction)

    def test_next_day_transactions(self):
        matching_transactions = [
            Transaction({
                'amount': 100,
                'transaction-time': datetime(year=2017, month=6, day=1)
            }),
            Transaction({
                'amount': -100,
                'transaction-time': datetime(year=2017, month=6, day=2)
            }),
        ]
        no_match_transactions = [
            Transaction({
                'amount': -5,
                'transaction-time': datetime(year=2017, month=6, day=10)
            }),
            Transaction({
                'amount': 50,
                'transaction-time': datetime(year=2017, month=6, day=10)
            }),
        ]
        transactions = no_match_transactions + matching_transactions

        annotate_cc_transations(transactions)
        for transaction in no_match_transactions:
            assert not is_cc_transaction(transaction)
        for transaction in matching_transactions:
            assert is_cc_transaction(transaction)
