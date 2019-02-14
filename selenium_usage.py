from selenium import webdriver
import selenium
import pandas as pd
import time

url = 'https://racing.hkjc.com/racing/info/meeting/Results/English/Local/20190213/HV/1'
browser = webdriver.Chrome()
browser.get(url)

# print(len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/thead/tr/td')))
row_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr'))
col_num = len(browser.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[1]/td'))

main_list = []
headers = []

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


# while True:
#     try:
#         col = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[{}]'.format(col_num))
#         row_num = 1
#         while True:
#             try:
#                 row = col.find_element_by_xpath("./td[{}]".format(row_num))
#                 row_num += 1
#             except selenium.common.exceptions.NoSuchElementException:
#                 break
#         col_num += 1
#     except selenium.common.exceptions.NoSuchElementException:
#         break

browser.close()

df = pd.DataFrame(data = main_list, columns= headers)