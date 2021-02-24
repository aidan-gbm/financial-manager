# Financial Management Tool
Created and maintained by [theGingerbreadMan](https://github.com/aidan-gbm)

## Usage
Python 3.8 application. Requirements detailed in [requirements.txt](requirements.txt). Only supported on Unix systems (inquirer breaks on Windows).

## TODO
- Use better command line colors (scheme support?)
- Add support for reading statement exports from financial institutions
    - AMEX
    - Chase
    - Schwab
    - USAA
- Add collision detection when adding duplicate statements
- Add interactive management of accounts
- Improve run loop
    - Shell (class?) for main inquirer loop
    - Add cancel option to prompts
- Add info and/or statistics about accounts
    - Query system?
- Add filesystem encryption w/ password protection