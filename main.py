import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

def get_df(date, no_races):

    if not os.path.isdir('/Users/mac/Documents/web_scraping/data/{}'.format(date)):
        os.makedirs('/Users/mac/Documents/web_scraping/data/{}'.format(date))

    for j in range(1, no_races+1):


        url = 'https://racing.hkjc.com/racing/info/meeting/Results/English/Local/{}/HV/{}'.format(date, str(j))
        print(url)

        source = requests.get(url).text

        soup = BeautifulSoup(source, 'lxml')


        content = soup.findAll("div", {"class": "clearDivFloat rowDiv15"})[0]
        table = soup.find('table', attrs={'class':'tableBorder trBgBlue tdAlignC number12 draggable'})


        main_list = []
        for tr in table.findAll('tr'):
            temp = []
            for td in tr.findAll('td'):
                temp.append(td.text)
            main_list.append(temp)


        main_list[0] = [x.lstrip().rstrip().replace('\r\n', '') for x in main_list[0]]
        columns = main_list.pop(0)

        main_list = [main_list[i] for i in range(0,len(main_list), 2)]

        for i in range(len(main_list)):
            lst = main_list[i]
            runningPosition = ','.join(lst[10:-2])
            lst = lst[:9] + lst[-2:]
            lst.insert(-2, runningPosition)
            main_list[i] = lst

#        main_list.insert(0, columns)


        # with open('{}_{}'.format(date, i), 'w', newline='') as myfile:
        #     wr = csv.writer(myfile)
        #     wr.writerow(main_list)

        main_df = pd.DataFrame(data = main_list, columns = columns)

        print(main_df)
        print('')

        main_df.to_csv('/Users/mac/Documents/web_scraping/data/{}/race_{}.csv'.format(date, str(j)), index = False)





get_df('20190130', 8)

