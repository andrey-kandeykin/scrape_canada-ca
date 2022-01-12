from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import re
import csv



service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-notifications')

driver = webdriver.Chrome(
    service=service,
    options=options
)

def parse():
    try:
        driver.get('https://innovation.ised-isde.canada.ca/s/list-liste?language=en_CA&token=a0B5W000000WsFSUA0')
        time.sleep(4)

        сount = 1
        while True:
            try:
                more_btn = driver.find_element(By.ID, 'moreBtn')
                print('founded: ', сount)
                more_btn.click()
                time.sleep(1)
                сount += 1
            except NoSuchElementException:
                print('not founded')
                break

        article_btns = driver.find_elements(By.CLASS_NAME, 'list-item-dov')
        for article_btn in article_btns:
            article_btn.click()


        html = driver.page_source
        with open('index.html', 'w', encoding="UTF-8-sig") as file:
            file.write(html)

        with open('index.html', encoding="UTF-8-sig") as file:
            html = file.read()
            # print('read')
        soup = BeautifulSoup(html, 'lxml')
        # print('read soup')

        output = []
        blocks = soup.find_all(class_="advanced-results")

        count = 0

        for block in blocks:
            try:
                name = block.find('div', class_='list-sub-title').text
                short_desc = block.find(class_='h4').text
                long_desc = block.find(class_='program-dov-description').text
                all_statuses = block.find(class_='mrgn-lft-xl')

                statuses_list = ''
                if all_statuses:
                    all_statuses.find_all('p')
                    for status in all_statuses:
                        statuses_list + status.text.strip() + '. '
                else:
                    statuses_list= 'None'

            except Exception as e:
                print('1', e, 'count: ', count)

            try:
                moneys_list = ''
                moneys = block.find('b', text=re.compile('Money'))
                if moneys:
                    moneys = block.find('b', text=re.compile('Money')).find_parent().find_next_sibling().find_all('li')

                    for money in moneys:
                        moneys_list = moneys_list + money.find('span').text.strip() + '. '
                        # print('moneys_list: ', moneys_list)
                else:
                    moneys_list = 'None'

            except Exception as e:
                print('2', e, 'count: ', count)

            try:
                use_this_to = block.find('b', text='Use this to')
                use_this_to_list = ''
                if use_this_to:
                    use_this_to = block.find('b', text='Use this to').find_parent().find_next_sibling().find_all('li')
                    for i in use_this_to:
                        use_this_to_list = use_this_to_list + i.find('span').text.strip() + '. '
                    # print('use_this_to_list: ', use_this_to_list)
                else:
                    use_this_to_list = 'None'

            except Exception as e:
                print('3', e, 'count: ', count)

            try:
                funding = block.find('b', text='Funding Limits')
                funding_list = ''
                if funding:
                    funding = block.find('b', text='Funding Limits').find_parent().find_next_sibling().find_all('li')
                    for i in funding:
                        funding_list = funding_list + i.find('span').text.strip() + '. '
                    # print('funding_list: ', funding_list)
                else:
                    funding_list = 'None'
            except Exception as e:
                print('4', e, 'count: ', count)

            try:
                you = block.find('b', text='You')
                you_list = ''
                if you:
                    you = block.find('b', text='You').find_parent().find_next_sibling().find_all('li')
                    for i in you:
                        you_list = you_list + i.find('span').text.strip() + '. '
                    # print('you_list: ', you_list)
                else:
                    you_list = 'None'
            except Exception as e:
                print('5', e, 'count: ', count)

            btn_yellow = block.find('a', class_='btn-yellow')
            if btn_yellow:
                btn_yellow = block.find('a', class_='btn-yellow').get('href')
                str(btn_yellow)
            else:
                btn_yellow = 'None'
            # print(btn_yellow)

            data = [name, short_desc, long_desc, statuses_list, moneys_list, use_this_to_list, funding_list, you_list, btn_yellow]

            output.append(data)
            count += 1
            titles = ['Name', 'Short Description', 'Long Description', 'Status', 'Money', 'Use this to', 'Funding Limits', 'You', 'Link']


        with open('list.csv', 'w', encoding='UTF-8-sig') as file:
            writer = csv.writer(file, delimiter=";", lineterminator='\n')
            writer.writerow(titles)
            for i in output:
                writer.writerow(i)

    except Exception as e:
        print('Exception!', e)


if __name__ == '__main__':
    parse()
    driver.quit()
