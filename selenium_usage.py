from selenium import webdriver
import selenium
import time

url = 'https://racing.hkjc.com/racing/info/meeting/Results/English/Local/20190213/HV/1'
browser = webdriver.Chrome()
browser.get(url)

col_num = 1
while True:
    try:
        col = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[{}]'.format(col_num))
        row_num = 1
        while True:
            try:
                row = col.find_element_by_xpath("./td[{}]".format(row_num))
                row_num += 1
                print(row.text)
            except selenium.common.exceptions.NoSuchElementException:
                break
        col_num += 1
    except selenium.common.exceptions.NoSuchElementException:
        break


browser.close()
