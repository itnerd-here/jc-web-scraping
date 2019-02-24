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
import itertools


url = 'https://racing.hkjc.com/racing/information/English/Horse/SelectHorse.aspx'
browser = webdriver.Chrome()
browser.get(url)

letters = list(string.ascii_uppercase)

horse_name = []
country_of_origin_age = []
country_of_origin_age = []
color_sex = []
import_type = []
season_stakes = []
total_stakes = []
no_of_123_stakes = []
no_of_starts_in_past_races  = []
trainer = []
owner = []
current_rating = []
start_of_season_rating = []
sire = []
dam = []
dam_sire = []

for letter in letters:
    browser.find_element_by_link_text(letter).click()
    # find the size of the table and do the required operation
    row_count = len(browser.find_elements_by_xpath(
        "/html/body/div[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr"))
    column_count = len(browser.find_elements_by_xpath(
        "/html/body/div[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td"))
    WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located(
                    (By.XPATH,
                    "/html/body/div[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]")))

    for row in range(1, row_count+1):
        for col in range(1, column_count+1):
            try:
                # WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located(
                #     (By.XPATH,
                #      "/html/body/div[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[{}]/td[{}]/table[1]/tbody[1]/tr[1]/td[1]/li/a".format(
                #          row, col))
                # ))
                time.sleep(1)
                browser.find_element_by_xpath(
                    "/html/body/div[1]/p[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[{}]/td[{}]/table[1]/tbody[1]/tr[1]/td[1]/li/a".format(row, col)).click()
                WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located(
                    (By.XPATH,
                     "/html/body/div[1]/table[1]/tbody[1]/tr[1]")))
                horse_name.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[1]/table/tbody/tr[1]").text)
                country_of_origin_age.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[3]").text)
                color_sex.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[3]").text)
                import_type.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[3]/td[3]").text)
                season_stakes.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[4]/td[3]").text)
                total_stakes.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td[3]").text)
                no_of_123_stakes.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[6]/td[3]").text)
                no_of_starts_in_past_races.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr[7]/td[3]").text)
                trainer.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[1]/td[3]").text)
                owner.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[2]/td[3]").text)
                current_rating.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[3]/td[3]").text)
                start_of_season_rating.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[4]/td[3]").text)
                sire.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[5]/td[3]").text)
                dam.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[6]/td[3]").text)
                dam_sire.append(browser.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr[7]/td[3]").text)

                browser.back()

            except selenium.common.exceptions.NoSuchElementException:
                break

    browser.back()

time.sleep(5)
browser.close()

data = [{'Horse_name': a, 'Country of Origin & Age': b, 'Color & Sex': c, 'Import Type': d, 'Season Stakes': e, 'Total Stakes': f, 'Number Of 123 Starts': g, 'Number of Starts In Past Races': h, 'Trainer': i, 'Owner': j, 'Current Rating': k, 'Start Of Season Rating': l, 'Sire': m, 'Dam': n, 'Dam Sire': o } for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o in zip(horse_name, country_of_origin_age, color_sex,import_type, season_stakes, total_stakes, no_of_starts_in_past_races, no_of_starts_in_past_races, trainer, owner, current_rating, start_of_season_rating, sire, dam, dam_sire)]

pd.DataFrame(data).to_csv('horse_info.csv', index = False)