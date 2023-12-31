# Copyright (c) 2023 Filippo Ferrario
# Licensed under the MIT License. See the LICENSE.

FIELDS_COUNT = 6
VALUE_INDEX = 1
DATE_INDEX = 3
TAG_INDEX = 4

months = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]

def initialize_statistics(statistics, thresholds_count):
    statistics['expenses_count'] = 0
    statistics['expenses_sum'] = 0.0
    statistics['avg_expense'] = 0.0
    statistics['median_expense'] = 0.0
    statistics['max_expense'] = None
    statistics['min_expense'] = None
    statistics['expenses_by_size'] = [ 0.0 for x in range(thresholds_count + 1)]

    statistics['incomes_count'] = 0
    statistics['incomes_sum'] = 0.0
    statistics['avg_income'] = 0.0
    statistics['median_income'] = 0.0
    statistics['max_income'] = None
    statistics['min_income'] = None
    statistics['incomes_by_size'] = [ 0.0 for x in range(thresholds_count + 1)]
    
    statistics['net_worth'] = 0.0
    statistics['month_median_nw'] = 0.0

def get_month_and_year(str):
    splitted_date = str.split('-')
    
    if splitted_date[0].isdigit and splitted_date[1].isdigit:
        return f'{months[int(splitted_date[1]) - 1]} {splitted_date[0]}'

    return 'undefined'

def get_median(l):
    length = len(l)
    
    if length == 0:
        return 0.0

    l.sort()
    middle = length // 2

    if length % 2 or length < 2:
        return l[middle]
    
    return (l[middle] + l[middle - 1]) / 2

def get_month_median(nw_by_month):
    months_net_worth = [ nw_by_month[key]['incomes'] - nw_by_month[key]['expenses'] for key in nw_by_month.keys() ]

    return get_median(months_net_worth)

def add_to_incomes(value, date, threshold_index, statistics, nw_by_month, incomes_list):
    statistics['incomes_count'] += 1
    statistics['incomes_sum'] += value
    statistics['incomes_by_size'][threshold_index] += value
    nw_by_month[date]['incomes'] += value
    incomes_list.append(value)
                
    if statistics['min_income'] == None or statistics['min_income'] > value:
        statistics['min_income'] = value
                
    if statistics['max_income'] == None or statistics['max_income'] < value:
        statistics['max_income'] = value

def add_to_expenses(value, date, threshold_index, statistics, nw_by_month, expenses_list):
    statistics['expenses_count'] += 1
    statistics['expenses_sum'] += value
    statistics['expenses_by_size'][threshold_index] += value
    nw_by_month[date]['expenses'] += value
    expenses_list.append(value)
    
    if statistics['min_expense'] == None or statistics['min_expense'] > value:
        statistics['min_expense'] = value
                
    if statistics['max_expense'] == None or statistics['max_expense'] < value:
        statistics['max_expense'] = value

def analyze_data(rows, statistics, thresholds, nw_by_month_dic, incomes_list, expenses_list, incomes_ids):
    thresholds_len = len(thresholds)
    for row in rows:
        fields = row.split(',')
        
        if len(fields) == 6:
            value = 0.0

            try:
                value = float(fields[VALUE_INDEX])
            except ValueError:
                continue

            date = get_month_and_year(fields[DATE_INDEX])

            if not (date in nw_by_month_dic.keys()):
                nw_by_month_dic[date] = { 'expenses': 0.0, 'incomes': 0.0 }
            
            i = 0
            while i < thresholds_len and value > thresholds[i]:
                i += 1

            if fields[TAG_INDEX] in incomes_ids:
                add_to_incomes(value, date, i, statistics, nw_by_month_dic, incomes_list)
            else:
                add_to_expenses(value, date, i, statistics, nw_by_month_dic, expenses_list)

    statistics['avg_income'] = 0 if statistics['incomes_count'] == 0 else statistics['incomes_sum'] / statistics['incomes_count']
    statistics['median_income'] = get_median(incomes_list)

    statistics['avg_expense'] = 0 if statistics['expenses_count'] == 0 else statistics['expenses_sum'] / statistics['expenses_count']
    statistics['median_expense'] = get_median(expenses_list)

    statistics['net_worth'] = statistics['incomes_sum'] - statistics['expenses_sum']
    statistics['month_median_nw'] = get_month_median(nw_by_month_dic)

def print_statistics(statistics, thresholds):
    print('\nExpenses data:')
    print(f'Count:\t{round(statistics["expenses_count"], 2)}')
    print(f'Sum:\t{round(statistics["expenses_sum"], 2)}')
    print(f'Avg:\t{round(statistics["avg_expense"], 2)}')
    print(f'Median:\t{round(statistics["median_expense"], 2)}')
    print(f'Max:\t{round(statistics["max_expense"], 2)}')
    print(f'Min:\t{round(statistics["min_expense"], 2)}')
    print('Expenses by thresholds:')
    for i in range(len(thresholds)):
        print(f'x < {thresholds[i]}: {round(statistics["expenses_by_size"][i], 2)}', end=' | ')

    print(f'{thresholds[-1]} < x: {round(statistics["expenses_by_size"][-1], 2)}')

    print('\nIncomes data:')
    print(f'Count:\t{statistics["incomes_count"]}')
    print(f'Sum:\t{round(statistics["incomes_sum"], 2)}')
    print(f'Avg:\t{round(statistics["avg_income"], 2)}')
    print(f'Median:\t{round(statistics["median_income"], 2)}')
    print(f'Max:\t{round(statistics["max_income"], 2)}')
    print(f'Min:\t{round(statistics["min_income"], 2)}')
    print('Incomes by thresholds:')
    for i in range(len(thresholds)):
        print(f'x < {thresholds[i]}: {round(statistics["incomes_by_size"][i], 2)}', end=' | ')

    print(f'{thresholds[-1]} < x: {round(statistics["incomes_by_size"][-1], 2)}')

    print('\nNet-Worth data:')
    print(f'Net-Worth:\t{round(statistics["net_worth"], 2)}')
    print(f'Month median:\t{round(statistics["month_median_nw"], 2)}\n')
