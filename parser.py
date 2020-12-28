import asyncio

from asyncpg import Connection
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from loader import db


class DBCommand:
    pool: Connection = db
    GET_VALUES_DB = 'SELECT * FROM birzha;'
    ADD_VALUE = 'INSERT INTO birzha (ticker, company_name, insider_name, price, date, insider_trading_shares, marcet_cap, status, insider_position) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);'

    async def add_value_db(self, ticker, company_name, insider_name, price, date, insider_trading_shares, marcet_cap, status, insider_position):
        args = ticker, company_name, insider_name, price, date, insider_trading_shares, marcet_cap, status, insider_position
        await self.pool.execute(self.ADD_VALUE, *args)

    async def get_values_db(self):
        return await self.pool.fetch(self.GET_VALUES_DB)


db = DBCommand()

class ParseBirzha:
    date_button = '/html/body/div[1]/div/div/div/section/main/div/div[1]/div[7]/div/table/thead[1]/tr/th[7]/span'
    link = 'https://www.gurufocus.com/insider/summary'
    row_table_attr = 'data-v-1efd84d8'

    def __init__(self):
        self.browser = webdriver.Remote(command_executor='http://selenium:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
        print('Подключено')

    async def get_html(self, page=None):
        print('Парсим')
        browser = self.browser
        browser.get(self.link)
        sleep(15)
        browser.find_element_by_xpath(self.date_button).click()
        if page != None:
            browser.find_element_by_xpath(page).click()
        sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup


    async def parser_html(self, soup):
        all_values = await db.get_values_db()

        for i in soup.find_all('tbody')[0].find_all('tr'):
            if i.has_attr(self.row_table_attr):
                ticker = i.find(attrs={"data-column" : "Ticker"}).text.strip()
                company = i.find(attrs={"data-column" : "Company"}).text.strip()
                price = float(i.find(attrs={"data-column" : "Price"}).text.strip().replace('$', '').replace(',', ''))
                insider_name = i.find(attrs={"data-column" : "Insider Name"}).text.strip()
                date = i.find(attrs={"data-column" : "Date"}).text.strip()
                buy_sell = i.find(attrs={"data-column" : "Buy/Sell"}).text.strip()
                insider_trading_shares = int(i.find(attrs={"data-column" : "Insider Trading Shares"}).text.strip().replace(',', ''))
                market_cap = i.find(attrs={"data-column" : "Market Cap ($M)"}).text.strip()
                insider_position = i.find(attrs={"data-column" : 'Insider Position'}).text.strip()


                if price * insider_trading_shares >= 1000000 and buy_sell == 'Buy':
                    adoption = True
                    for item in all_values:
                        if item[1] == ticker and item[2] == company and item[3] == insider_name and item[4] == price and item[5] == date and item[6] == insider_trading_shares and item[7] == market_cap and item[9] == insider_position:
                            # print('Точно такая же запись')
                            adoption = False
                            break
                    if adoption:
                        await db.add_value_db(ticker, company, insider_name, price, date, insider_trading_shares, market_cap, 'New', insider_position)


                # print(f'{ticker} - {company} - {price} - {insider_name} - {date} - {buy_sell} - {insider_trading_shares} - {market_cap}')

    async def parse(self):
        soup = await self.get_html()
        await self.parser_html(soup)
        soup2 = await self.get_html('/html/body/div[1]/div/div/div/section/main/div/div[1]/div[8]/div/ul/li[2]')
        await self.parser_html(soup2)



