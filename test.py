from selenium import webdriver
from selenium.webdriver.support.select import Select
import os
import re
import selenium
import pandas as pd
import time

url = 'https://racing.hkjc.com/racing/info/meeting/Results/English/Local/20190213/HV/1'
browser = webdriver.Chrome()
browser.get(url)

race_date_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/select/option'))

for i in range(0, race_date_num):
    s1= Select(browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/select'))
    s1.select_by_index(i)
    info = s1.first_selected_option.get_attribute('value')

    if 'Local' in info:
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/a').click()

        detail = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[1]').text
        date = re.split(r'\s', detail)[2].replace('/', '-')


        if not os.path.isdir('/Users/mac/Documents/web_scraping/data/{}'.format(date)):
            os.makedirs('/Users/mac/Documents/web_scraping/data/{}'.format(date))

        #### number of races
        race_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td')) - 3

        #### loop all races
        for race in range(4, 4+race_num):

            #### current race
            cur_race = race-3

            #### number of rows and columns
            row_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr'))
            col_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[1]/td'))

            main_list = []
            headers = []
            ### append data
            for row in range(1, row_num+1):
                temp = []
                for col in range(1, col_num + 1):
                    try:
                        temp.append(browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[{}]/td[{}]'.format(row, col)).text)
                    except selenium.common.exceptions.NoSuchElementException:
                        break
                main_list.append(temp)

            for col in range(1, col_num + 1):
                try:
                    header = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/thead/tr/td[{}]'.format(col)).text
                    header = header.replace('\n', ' ')
                    headers.append(header)
                except selenium.common.exceptions.NoSuchElementException:
                    break

            df = pd.DataFrame(data = main_list, columns= headers)
            df.to_csv('./data/{}/race_{}.csv'.format(date, cur_race), index = False)

            if cur_race != race_num:
                browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[{}]/a'.format(race)).click()

    else:
        continue

time.sleep(10)
browser.close()