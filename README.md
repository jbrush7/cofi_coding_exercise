# cofi_coding_exercise

# Installation
The best way to use a virtualenv. Once it's installed use the following bootstrap:

~~~~
virtualenv C1
source C1/bin/activate
pip install -r requirements.txt
cp creds.py.sample creds.py
~~~~

*Very important*

Update the creds.py with the uid, token and api_token. Happy to send to you, but don't want to commit them in source control :)

## Usage

python transactions_report.py 

also supports various optional parameters including:

--ignore-donuts

--crystal-ball

--ignore-cc-payments

## Testing
Not as much coverage as I'd like, but covered the most important parts. The reporting could use some tests. 

## Future Improvements
Allow for arbitrary grouping for reporting (not just by month)

Filter by merchant name

Better connection error/network reporting

Caching
