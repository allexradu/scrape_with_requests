import requests

import json
import os
import openpyxl as xl
from search_product import search_product

json_file = os.path.join(os.getcwd(), 'json', 'table.json')
excel_file_path = os.path.join(os.getcwd(), 'excel', 'a.xlsx')

wb = xl.load_workbook(excel_file_path)
sh = wb[wb.sheetnames[0]]

current_col = 2

for row in range(1, sh.max_row + 1):
    code = sh.cell(row, 1).value
    data = search_product(code)
    for key in data.keys():
        print(f'row {row}/{sh.max_row}')
        sh.cell(row, current_col).value = key
        sh.cell(row, current_col + 1).value = data[key]
        current_col += 1
    current_col = 2

wb.save(excel_file_path)
