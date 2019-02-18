from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import re
import selenium
import pandas as pd
import time
import string

url = 'https://racing.hkjc.com/racing/information/English/Horse/SelectHorse.aspx'
browser = webdriver.Chrome()
browser.get(url)

letters = list(string.ascii_uppercase)

for letter in letters:
    browser.find_element_by_link_text(letter).click()
    # find the size of the table and do the required operation
    row_count = len(browser.find_elements_by_xpath(
        "/html/body/div[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr"))
    column_count = len(browser.find_elements_by_xpath(
        "/html/body/div[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td"))

    for row in range(1, row_count+1):
        for col in range(1, column_count+1):



  #  print(row_count)
  #  print(column_count)
    browser.back()

time.sleep(5)
browser.close()