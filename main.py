import csv
import inquirer
from os import path

import filesystem as fs
from prompt import *

# Load Configurations & Data
data_dir = path.realpath('data')
aliases = fs.load_aliases(data_dir)
transactions = fs.load_transactions(data_dir)

# Add new activity
options = [
    inquirer.List('action',
        message="Select an action",
        choices=['Add statement', 'View transactions', 'Exit']
    )
]

while ((ans := inquirer.prompt(options)['action']) != 'Exit'):
    if 'Add statement' == ans:
        account = select_account_new(
            transactions.keys(),
            'Select the account for this statement'
        )
        if not account in transactions.keys():
            transactions[account] = []
        
        statement = select_file('Enter the path of the statement file: ')
        if statement.endswith('.csv'):
            new_ts, aliases = fs.load_statement(statement, aliases)
            transactions[account].extend(new_ts)
        else:
            p_error('File must be a CSV')
    elif 'View transactions' == ans:
        if 0 == len(transactions.keys()):
            p_info('No existing accounts.')
        else:
            account = select_account(
                transactions.keys(),
                'Select the account to view'
            )
            p_info('Transactions:')
            for t in transactions[account]:
                print(f'\t({t["date"]}) {t["name"]}: {t["amount"]}')

# Write Changes
fs.save_aliases(data_dir, aliases)
for name, t_list in transactions.items():
    fs.save_transactions(data_dir, name, t_list)

p_success('Goodbye!')