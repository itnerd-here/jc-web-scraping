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

url = 'https://racing.hkjc.com/racing/info/meeting/Results/English/Local/20190213/HV/1'
browser = webdriver.Chrome()
browser.get(url)

def check_exists_by_xpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except selenium.common.exceptions.NoSuchElementException:
        return False
    return True


race_date_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/select/option'))

for i in range(0, race_date_num):
    s1= Select(browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/select'))
    s1.select_by_index(i)
    info = s1.first_selected_option.get_attribute('value')

    if 'Local' in info:
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/a').click()

        WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located(
            (By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[1]')))
        detail = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[1]').text
        date = re.split(r'\s', detail)[2].replace('/', '-')

        if not os.path.isdir('/Users/mac/Documents/web_scraping/data/{}'.format(date)):
            os.makedirs('/Users/mac/Documents/web_scraping/data/{}'.format(date))

        #### number of races
            lst = browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td')
            race_num = len([elem for elem in lst if 'href' in elem.get_attribute('outerHTML')])

            #### loop all races
            for race in range(4, 4+race_num):

                #### current race
                cur_race = race-3

                #### number of rows and columns
                WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located(
                    (By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr')))
                row_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr'))
                col_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[1]/td'))

                main_list = []
                headers = []
                ### append data
                for row in range(1, row_num+1):
                    temp = []
                    for col in range(1, col_num + 1):
                        temp.append(browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[{}]/td[{}]'.format(row, col)).text)
                    main_list.append(temp)

                for col in range(1, col_num + 1):
                    header = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/thead/tr/td[{}]'.format(col)).text
                    header = header.replace('\n', ' ')
                    headers.append(header)

                df = pd.DataFrame(data = main_list, columns= headers)
                df.to_csv('./data/{}/race_{}.csv'.format(date, cur_race), index = False)
                time.sleep(5)
                if cur_race != race_num:
                    if check_exists_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[{}]/a'.format(race)):
                        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[{}]/a'.format(race)).click()
                        time.sleep(5)

        else:
            continue

    else:
        continue

browser.close()