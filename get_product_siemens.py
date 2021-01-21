import requests
import lxml.html as lh
import json
import os
from lxml import html

json_file = os.path.join(os.getcwd(), 'json', 'table.json')
characters = ['Show prices', 'List Price', 'Customer Price', 'Service & Support', 'eClass', 'REACH']


# ['+', '\n', 'REACH', '€', 'Title', 'UNSPSC', 'VersionClassification']


def get_data(code):
    if code.find(':') == -1:
        url = f'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/{code}'
    else:
        url = f'https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/?mlfb={code}'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    page = requests.get(url, headers = headers)
    doc = lh.fromstring(page.content)

    tr_elements = doc.xpath('//tr')
    data = {}
    key = ''
    value = ''
    skip = False

    img = doc.cssselect('td#content div.pictureArea.pictureAreaCursor > img')
    if img:
        data.update({'image1': img.attrib['src']})

    def check_for_illegal_characters(column_text, illegal_characters):
        for item in illegal_characters:
            if item in column_text:
                return False
        return True

    'https://mall.industry.siemens.com/mall/en/ww/Catalog/DatasheetDownload?downloadUrl=teddatasheet%2F%3Fformat%3DPDF%26caller%3DMall%26mlfbs%3D3NA3820%26language%3Den'

    for row in tr_elements:
        if len(row) in [2, 3]:
            for col in range(len(row)):
                for col in range(len(row)):
                    col_data = str(row[col].text_content())
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
                if key != "" and value != "":
                    if 'DataSheet in PDF' not in key:
                        data.update({key: value.strip()})
                    else:
                        if 'support.industry.siemens.com' not in str(lh.tostring(row[1])):
                            doc2 = lh.fromstring(lh.tostring(row[1]))
                            a = doc2.xpath('//a')[0]
                            if 'href' in a.attrib.keys():
                                url = a.attrib['href']
                                data.update({'pdf': url})
            value = ''

    return data


with open(json_file, "w") as outfile:
    json.dump(get_data('1FK7032-5AK71-1LH3'), outfile, indent = 4)
