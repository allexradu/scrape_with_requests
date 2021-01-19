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


def search_product(code):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("window-size=1400,2100")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

    url = f'https://www.electricautomationnetwork.com/en/buscador?search_query={code}&submit_search='

    driver.get(url)
    sleep(1)

    elements = driver.find_elements_by_xpath('//*[@id="resultados_busqueda"]/tbody/tr/td[2]/a/p')

    for elem in elements:
        if elem.text == code:
            row = elements.index(elem) + 1
            elem = driver.find_element_by_xpath(f'//*[@id="resultados_busqueda"]/tbody/tr[{row}]/td[2]/a')
            url = elem.get_attribute('href')
            return get_data(url)
