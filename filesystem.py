from os import path, listdir
from re import sub
import pickle
import csv

from prompt import *
from calc import findMatches

def clean(string:str):
    """Returns filesystem safe string. Not for use with user input."""
    return sub('[\W]+', '', string.lower().replace(' ', '_'))

def save_aliases(data_dir:str, aliases:dict):
    """Saves aliases to disk.

    Pickled object is the aliases dictionary, saved as
    <data_dir>/aliases.pickle
    """
    save_path = path.join(data_dir, 'aliases.pickle')
    with open(save_path, 'wb') as f:
        pickle.dump(aliases, f)
    p_success('Saved aliases')

def load_aliases(data_dir:str):
    """Loads aliases from disk. Returns dict."""
    load_path = path.join(data_dir, 'aliases.pickle')
    with open(load_path, 'rb') as f:
        aliases = pickle.load(f)
    p_success('Loaded aliases')
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
        p_error('File does not exist')
        return ([], aliases)

    p_info('Loading statement...')
    transactions = []

    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            item = row['Description']
            matches = findMatches(item, aliases)
            if list == type(matches):
                p_info(f'No name found for "{item}"')
                opts = [inquirer.List(
                    'sel',
                    message='Select business name',
                    choices=matches + ['New']
                )]
                if 'New' == (name := inquirer.prompt(opts)['sel']):
                    q = [inquirer.Text('name', message='Name of business')]
                    name = inquirer.prompt(q)['name']
                if name in aliases.keys():
                    aliases[name].append(item)
                else:
                    aliases[name] = [item]
            else:
                name = matches
                p_info(f'Matched {name} -> "{item}"')

            transactions.append({
                'date': row['Date'],
                'name': name,
                'amount': row['Amount']
            })
        
        return (transactions, aliases)
