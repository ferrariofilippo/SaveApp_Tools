# Copyright (c) 2023 Filippo Ferrario
# Licensed under the MIT License. See the LICENSE.

def try_read_file(src_path):
    try:
        file = open(src_path, 'rt')

        # Skip the header line
        file.readline()
        rows = file.readlines()
        file.close()

        return rows
    except:
        print('File not found. Terminating execution...')
        exit(1)

def create_csv(nw_by_month_dic):
    csv = open('incomes_expenses_by_month.csv', 'wt')
    csv.write('DATE,EXPENSES,INCOME\n')

    for key in nw_by_month_dic:
        csv.write(f'{key},{round(nw_by_month_dic[key]["expenses"], 2)},{round(nw_by_month_dic[key]["incomes"], 2)}\n')

    csv.flush()
    csv.close()
