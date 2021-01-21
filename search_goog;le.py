import requests

import lxml.html as lh
import json
import os
from get_product_data import get_data
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from time import sleep

json_file = os.path.join(os.getcwd(), 'json', 'table.json')

# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("disable-gpu")
# chrome_options.add_argument("window-size=1400,2100")
# chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)


driver = webdriver.Chrome()


def search_product(code):
    url = f'https://www.google.com/search?q=site:mall.industry.siemens.com%20{code}'

    driver.get(url)
    sleep(2)

    WebDriverWait(driver, 10).until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe")))
    agree = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="introAgreeButton"]/span/span')))
    agree.click()
    sleep(1)

    parent = driver.find_elements_by_xpath('//*[@id="rso"]/div/div')[0]
    child = parent.find_elements_by_xpath('//div/div[1]/a/h3/span')
    for ch in child:
        print(ch.text)
        if ch.text == f'{code} - Product Details - Industry Mall - Siemens WW':
            test = driver.find_element_by_css_selector(
                f'div#rso div:nth-child({child.index(ch) + 1}) > div > div.yuRUbf > a')
            print(test.get_attribute('href'))
            break
    #     print(child.text)
    # print(child)
    # for par in parent:
    #     child = par.find_elements_by_xpath('//div/div[1]/a/h3/span')
    #     print(child.text)
    # for ch in child:
    #     if ch.text == f'{code} - Product Details - Industry Mall - Siemens WW':
    #         print(ch.text)

    # for elem in elements:
    #     if elem.text == code:
    #         row = elements.index(elem) + 1
    #         elem = driver.find_element_by_xpath(f'//*[@id="resultados_busqueda"]/tbody/tr[{row}]/td[2]/a')
    #         url = elem.get_attribute('href')
    #         return get_data(url)


search_product('3NA3360')
