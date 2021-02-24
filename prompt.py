from colorama import Fore
import inquirer
import readline
import glob

def p_info(msg:str):
    print(f'[{Fore.BLUE}#{Fore.RESET}] {msg}')

def p_success(msg:str):
    print(f'[{Fore.GREEN}+{Fore.RESET}] {msg}')

def p_error(msg:str):
    print(f'[{Fore.RED}!{Fore.RESET}] {msg}')

def p_prompt(msg:str):
    return input(f'[{Fore.LIGHTYELLOW_EX}?{Fore.RESET}] {msg}')

def select_account(accounts, msg):
    options = [
        inquirer.List('act',
        message=msg,
        choices=accounts)
    ]
    return inquirer.prompt(options)['act']

def select_file(msg):
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    return input(f'[{Fore.LIGHTYELLOW_EX}?{Fore.RESET}] {msg}')
