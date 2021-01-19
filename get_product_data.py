import requests
import lxml.html as lh
import json
import os

json_file = os.path.join(os.getcwd(), 'json', 'table.json')
characters = ['+', '\n', 'REACH', '€', 'Title', 'UNSPSC', 'VersionClassification']


def get_data(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content)

    tr_elements = doc.xpath('//tr')
    data = {}
    key = ''
    value = ''
    skip = False

    def check_for_illegal_characters(column_text, illegal_characters):
        for item in illegal_characters:
            if item in column_text:
                return False
        return True

    for row in tr_elements:
        if len(row) in [2, 3]:
            for col in range(len(row)):
                col_data = row[col].text_content()

                if check_for_illegal_characters(col_data, characters):
                    if len(col_data) != "":
                        skip = False
                        if col == 0:
                            key = col_data
                            # print('key: ', key)
                        if len(row) == 2:
                            if col == 1:
                                value = col_data
                                # print('value: ', value)
                        else:
                            if col == 1:
                                value = col_data
                                # print('value 1: ', value)
                            if col == 2:
                                value += col_data
                                # print('value 2: ', value)
                else:
                    skip = True
            if not skip:
                # print('value 3: ', value)
                if key != "" and value != "":
                    data.update({key: value.strip()})
                value = ''

    return data
