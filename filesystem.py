from os import path, listdir
import pickle
import csv
import re

from prompt import *

def clean(string:str):
    return re.sub('[\W]+', '', string.replace(' ', '_'))

def get_key(aliases:dict, value:str):
    for key, vals in aliases.items():
        if value in vals:
            return key
    return False

def load_aliases(data_dir:str):
    aliases = {}
    with open(path.join(data_dir, 'aliases.csv'), 'a+') as csv_file:
        p_info('Loading aliases...')
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] in aliases:
                aliases[row[0]].append(row[1])
            else:
                aliases[row[0]] = [row[1]]
    return aliases

def save_transactions(data_dir:str, account:str, transactions:list):
    """Saves an individual account's transactions.
    
    Pickled object is a tuple based on the real account name and the
    transaction list. Filename is a sanitized version of the account name.
    """
    filename = clean(account) + '.transaction.pickle'
    save_path = path.join(data_dir, filename)
    with open(save_path, 'wb') as f:
        pickle.dump((account, transactions), f, pickle.HIGHEST_PROTOCOL)
    p_success('Saved transactions for ' + account)

def load_transactions(data_dir:str):
    """Load all existing transactions in the data directory.

    Returns a ready-to-use dictionary with account names as keys and
    transaction lists as values.
    """
    transactions = {}
    for filename in listdir(data_dir):
        if filename.endswith('.transaction.pickle'):
            with open(path.join(data_dir, filename), 'rb') as f:
                account, t_list = pickle.load(f)
                transactions[account] = t_list
                p_success('Loaded transactions for ' + account)
    return transactions

def load_statement(file_path:str, aliases:dict):
    file_path = path.expanduser(file_path)
    if not path.exists(file_path):
        raise FileNotFoundError(file_path)
    p_info('Loading statement...')

    alias_values = [x for v in aliases.values() for x in v]
    transactions = []

    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if key := get_key(aliases, row['Description']):
                name = key
            else:
                p_info('No name found for: ' + row['Description'])
                name = p_prompt('Enter name for transaction: ')
                if name in aliases.keys():
                    aliases[name].append(row['Description'])
                else:
                    aliases[name] = [row['Description']]

            transactions.append({
                'date': row['Date'],
                'name': name,
                'amount': row['Amount']
            })
        
        return (transactions, aliases)
