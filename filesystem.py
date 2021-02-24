from os import path
import csv

from prompt import *

def get_key(aliases:dict, value:str):
    for key, vals in aliases.items():
        if value in vals:
            return key
    return False

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
