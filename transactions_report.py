import argparse
from pprint import pprint
from src.api_client import get_current_transations, get_current_and_projected_transations
from src.filtering import is_cc_transaction, annotate_cc_transations, is_donut
from src.reporting import build_monthly_report, average_mothly_report


def main():
    parser = argparse.ArgumentParser(description='Filter and report transactions.')
    parser.add_argument('--ignore-donuts', help='We love donuts! Disregard all donut-related transactions.', action='store_true')
    parser.add_argument('--crystal-ball', help='Include transactions that have happened or are expected to happen this month.', action='store_true')
    parser.add_argument('--ignore-cc-payments', help='Disregard all credit card payments.', action='store_true')

    args = parser.parse_args()

    # Get the transactions from the api
    if args.crystal_ball:
        all_transactions, error = get_current_and_projected_transations()
    else:
        all_transactions, error = get_current_transations()
    if error is not None:
        print 'failed to get data :( {error}'.format(error=str(error))
        return

    # Setup Filtering
    transation_filters = []
    if args.ignore_donuts:
        transation_filters.append(is_donut)
    if args.ignore_cc_payments:
        transation_filters.append(is_cc_transaction)
        annotate_cc_transations(all_transactions)

    # Filter transactions
    transactions = [transation for transation in all_transactions if not any(f(transation) for f in transation_filters)]

    # Create Reports
    monthly_report = build_monthly_report(transactions)
    monthly_report.update(average_mothly_report(monthly_report))
    pprint(dict(monthly_report))

    # Print list of ignored cc transactions
    if args.ignore_cc_payments:
        for transation in all_transactions:
            if is_cc_transaction(transation):
                print transation


if __name__ == '__main__':
    main()
