# Copyright (c) 2023 Filippo Ferrario
# Licensed under the MIT License. See the LICENSE.

import csvtools
import analytics
import graphs
from os import system, name
from sys import argv
from threading import Thread
from time import sleep

###############################################################################
# Customize your params

# Your source .csv file 
YOUR_FILE_PATH = 'INSERT PATH TO YOUR FILE HERE'

# Thresholds to split movements (eg. x < 10, 10 <= x < 50, ...)
thresholds = [ 10, 50, 200, 1000 ]
###############################################################################

is_analyzing = True

incomes_ids = set()
statistics = { }
by_month = { }
incomes_list = [ ]
expenses_list = [ ]

def get_income_ids():
    ids = input('Insert your income tags\' ids separated by a comma (,): ').split(',')

    for id in ids:
        if id.isdigit():
            incomes_ids.add(id)
        else:
            print(f'Parsing failed. ID: {id} was skipped.')

def help():
    print('SaveApp CLI help:')
    print('Except for \'-h\', each options should be preceeded by the list of income tags ids. See the example below:')
    print('> python3 ./main.py 1 2 -g\n')
    print('-s\t\t\tprint statistics')
    print('-c\t\t\tcreate a -csv file containing the net-worth for each month')
    print('-g\t\t\topen graph menu')
    print('-h\t\t\tshow help menu')

def parse_args():
    if argv[1] == '-h':
        help()
        return
    
    length = len(argv)
    i = 1
    while i < length and argv[i].isdigit():
        incomes_ids.add(argv[i])
        i += 1
    
    if i == length:
        print('No option specified!')
        return
    
    rows = csvtools.try_read_file(YOUR_FILE_PATH)
    analytics.analyze_data(rows, statistics, thresholds, by_month, incomes_list, expenses_list, incomes_ids)

    match argv[i]:
        case '-s':
            analytics.print_statistics(statistics, thresholds)
        case '-c':
            csvtools.create_csv(by_month)
        case '-g':
            graphs.show_graphs(by_month, thresholds, statistics['incomes_by_size'], statistics['expenses_by_size'], False)
        case _:
            print(f'Specified options \'{argv[i]}\' doesn\'t exist!')

def menu():
    while True:
        print('Available actions:')
        print('\t- Print statistics (s)')
        print('\t- Create csv (c)')
        print('\t- Show graphs (g)')
        print('\t- Quit (q)')
        choice = input().lower()
        _ = system('cls' if name == 'nt' else 'clear')
        
        match choice:
            case 's':
                analytics.print_statistics(statistics, thresholds)
            case 'c':
                csvtools.create_csv(by_month)
            case 'g':
                graphs.show_graphs(by_month, thresholds, statistics['incomes_by_size'], statistics['expenses_by_size'])
            case 'q':
                exit(1)

def loading_screen():
    while is_analyzing:
        print('Loading data...')
        sleep(2)

    system('cls' if name == 'nt' else 'clear')

if __name__ == '__main__':
    analytics.initialize_statistics(statistics, len(thresholds))

    if len(argv) != 1:
        parse_args()
    else:
        rows = csvtools.try_read_file(YOUR_FILE_PATH)
        get_income_ids()

        t = Thread(target=loading_screen, daemon=True)
        t.start()
        analytics.analyze_data(rows, statistics, thresholds, by_month, incomes_list, expenses_list, incomes_ids)
        is_analyzing = False
        t.join()

        menu()
