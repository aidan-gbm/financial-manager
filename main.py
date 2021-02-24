import csv
import inquirer
from os import path

from prompt import *
from filesystem import load_statement

# Load Configurations & Data
aliases = {}
data_dir = 'data'
with open(path.join(data_dir, 'aliases.csv'), 'a+') as csv_file:
    csv_file.seek(0)
    p_info('Loading aliases...')
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if row[0] in aliases:
            aliases[row[0]].append(row[1])
        else:
            aliases[row[0]] = [row[1]]

transactions = {}
with open(path.join(data_dir, 'info.csv')) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        p_info('Loading account: ' + row[0])
        transactions[row[0]] = []#load_transactions(row[1])

# Add new activity
options = [
    inquirer.List('action',
        message="Select an action",
        choices=['Add statement', 'View transactions', 'Exit']
    )
]

while ((ans := inquirer.prompt(options)['action']) != 'Exit'):
    if 'Add statement' == ans:
        statement = select_file('Enter the path of the statement file: ')
        if statement.endswith('.csv'):
            account = select_account(transactions.keys(), 'Select the account to which you are appending')
            new_ts, aliases = load_statement(statement, aliases)
            transactions[account].extend(new_ts)
        else:
            p_error('File must be a CSV')
    elif 'View transactions' == ans:
        account = select_account(transactions.keys(), 'Select the account to view')
        p_info('Transactions:')
        for t in transactions[account]:
            print(f'\t({t["date"]}) {t["name"]}: {t["amount"]}')

# Write Changes
with open(path.join(data_dir, 'aliases.csv'), 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    for key, vals in aliases.items():
        for val in vals:
            csv_writer.writerow([key, val])

p_success('Goodbye!')