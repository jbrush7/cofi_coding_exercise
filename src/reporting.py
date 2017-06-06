from collections import defaultdict

def build_monthly_report(transactions):
    monthly_report = defaultdict(lambda: {'spent': 0, 'income': 0})
    for trans in transactions:
        report_key = '{year}-{month:02d}'.format(year=trans.datetime.year, month=trans.datetime.month)
        if trans.amount <= 0:
            monthly_report[report_key]['spent'] += trans.amount
        else:
            monthly_report[report_key]['income'] += trans.amount
    return monthly_report

def average_mothly_report(monthly_report):
    avg_spend = 0
    avg_income = 0
    for amounts in monthly_report.itervalues():
        avg_spend += amounts['spent']
        avg_income += amounts['income']
    avg_spend = avg_spend / len(monthly_report)
    avg_income = avg_income / len(monthly_report)

    return {'average': {'spent': avg_spend, 'income': avg_income}}

