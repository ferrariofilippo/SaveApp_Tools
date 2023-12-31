# Copyright (c) 2023 Filippo Ferrario
# Licensed under the MIT License. See the LICENSE.

import matplotlib.pyplot as plt
from os import system, name

def show_expenses_threshold_graph(thresholds_list, expenses_by_size):
    labels = [ str(x) for x in thresholds_list]
    labels.append(f'+{thresholds_list[-1]}')

    plt.bar(labels, expenses_by_size)
    plt.title('Expenses')
    plt.xlabel('Threshold')
    plt.ylabel('Total')
    plt.show()

def show_incomes_threshold_graph(thresholds_list, incomes_by_size):
    labels = [ str(x) for x in thresholds_list]
    labels.append(f'+{thresholds_list[-1]}')

    plt.bar(labels, incomes_by_size)
    plt.title('Incomes')
    plt.xlabel('Threshold')
    plt.ylabel('Total')
    plt.show()
    
def show_net_worth_by_month(nw_by_month_dic):
    nw = [ nw_by_month_dic[key]['incomes'] - nw_by_month_dic[key]['expenses'] for key in nw_by_month_dic.keys() ]
    labels = range(len(nw_by_month_dic.keys()))

    plt.bar(labels, nw)
    plt.xticks(labels, nw_by_month_dic.keys(), rotation=90)
    plt.title('Net-worth by month')
    plt.xlabel('Month')
    plt.ylabel('Total')
    plt.tight_layout()
    plt.show()

def show_graphs(nw_by_month_dic, thresholds_list, incomes, expenses, can_go_back = True):
    end = False
    while not end:
        print('Available graphs:')
        print('\t- Expenses by threshold (e)')
        print('\t- Incomes by threshold (i)')
        print('\t- Net-worth by month (m)')
        print('\t- Quit (q)')

        choice = input().lower()
        _ = system('cls' if name == 'nt' else 'clear')
        
        match choice:
            case 'e':
                show_expenses_threshold_graph(thresholds_list, expenses)
            case 'i':
                show_incomes_threshold_graph(thresholds_list, incomes)
            case 'm':
                show_net_worth_by_month(nw_by_month_dic)
            case 'q':
                if can_go_back:
                    end = True
                else:
                    exit(1)
