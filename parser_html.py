import asyncio 
from bs4 import BeautifulSoup
from datetime import datetime
import os
from bot import send_message
from typing import List
import time

folder_path = 'html'
latest_file = max([os.path.join(folder_path, f) for f in os.listdir(folder_path)], key=os.path.getctime)


with open(latest_file, 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
tables = soup.find_all('table')
# print(tables)


data = []
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        row_data = [col.text.strip() for col in cols]
        data.append(row_data)
# print(data)
k = 0
future_divs = []
past_divs = []
for i in data: 
    if len(i) == 0:
        k += 1
    else:    
        if k == 1:
            future_divs.append(i)
        if k == 2:
            past_divs.append(i)

future_divs = future_divs[:-1]    

'''получение текущей даты в формате дд.мм.гггг'''
def get_current_date():
    current_date = datetime.now().strftime("%d.%m.%Y")
    return current_date


import os
from bs4 import BeautifulSoup

class DataExtractor:
    def __init__(self):
        self.folder_path = 'html'
        self.latest_file = self.get_latest_file()
        self.previous_file = self.get_previous_file()
        self.soup = self.get_soup(self.latest_file)
        self.tables = self.soup.find_all('table')
        self.data = self.get_data()
        self.future_divs, self.past_divs = self.get_dividends()
        self.new_future_divs, self.new_past_divs = self.compare_files()

    def get_latest_file(self):
        return max([os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)], key=os.path.getctime)

    def get_previous_file(self):
        files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)]
        files.remove(self.latest_file)
        return max(files, key=os.path.getctime)

    def get_soup(self, file):
        with open(file, 'r') as f:
            return BeautifulSoup(f.read(), 'html.parser')

    def get_data(self):
        data = []
        for table in self.tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                row_data = [col.text.strip() for col in cols]
                data.append(row_data)
        return data

    def get_dividends(self):
        k = 0
        future_divs = []
        past_divs = []
        for i in self.data: 
            if len(i) == 0:
                k += 1
            else:    
                if k == 1:
                    future_divs.append(i)
                if k == 2:
                    past_divs.append(i)
        future_divs = future_divs[:-1]
        return future_divs, past_divs

    def compare_files(self):
        previous_soup = self.get_soup(self.previous_file)
        previous_tables = previous_soup.find_all('table')

        previous_data = []
        for table in previous_tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                row_data = [col.text.strip() for col in cols]
                previous_data.append(row_data)

        k = 0
        previous_future_divs = []
        previous_past_divs = []
        for i in previous_data: 
            if len(i) == 0:
                k += 1
            else:    
                if k == 1:
                    previous_future_divs.append(i)
                if k == 2:
                    previous_past_divs.append(i)
        previous_future_divs = previous_future_divs[:-1]

        new_future_divs = [x for x in self.future_divs if x not in previous_future_divs]
        new_past_divs = [x for x in self.past_divs if x not in previous_past_divs]
        
        return new_future_divs, new_past_divs


class MessageFutureDividends(DataExtractor):
    def get_message(self) -> str:
        # Реализуйте этот метод для формирования текстового сообщения для будущих дивидендов
        message = "Текстовое сообщение для будущих дивидендов"
        return message


class MessagePastDividends(DataExtractor):
    def get_message(self) -> str:
        # Реализуйте этот метод для формирования текстового сообщения для прошлых дивидендов
        message = "Текстовое сообщение для прошлых дивидендов"
        return message


message = DataExtractor()
new_future_divs, new_past_divs = message.compare_files()
future_divs, past_divs = message.get_dividends()

# print(new_future_divs)

def get_divs(divs):
    txt_summary = 'Ближайшие выплаты дивидендов \n'    
    arraydivs = []
    for i in divs:
        # print('\n', i[0])
        name = ''.join(filter(str.isalnum, i[0]))
        tiker = i[1]
        fiat_divs = i[3]
        dividend_income = i[4]
        buy_before = i[6]
        closing_date_of_the_register = i[7]
        payment_up_to = i[8]
        share_price = i[9]
        
        
        txt = f'''{name} {tiker} 
        дивиденды в рублях {fiat_divs} 
        доходность {dividend_income}
        купить до {buy_before}
        дата закрытия реестра {closing_date_of_the_register}
        выплата до {payment_up_to}
        цена акции {share_price}
        '''
        txt_summary += txt + '\n'
        arraydivs.append(txt_summary)
        # print(arraydivs)
        txt_summary = ''
    return arraydivs
    # asyncio.run(send_message(txt_summary))    

"""        
get_divs(new_future_divs)

"""
# get_divs(new_future_divs)
def get_limit_message(arrey_all_stocks_yesterday):
    '''количество бумаг которые будут обеденены в сообщении'''
    limit_stocks_in_message = 5
    arrey = []
    counter = 0
    message = ''
    for i in get_divs(new_future_divs):
        if counter <= limit_stocks_in_message:
            message += i
            # print(i)  
        else:
            arrey.append(message)
            message = ''
            counter = 0
        counter += 1
    return arrey


short_message_list = get_limit_message(get_divs(new_future_divs))

def send_message_list(message_list=short_message_list):
    for i in short_message_list:
        asyncio.run(send_message(i))  
        time.sleep(1)  


send_message_list(message_list=short_message_list)


    # print(i)
# print(get_limit_message(get_divs(new_future_divs)))
# asyncio.run(send_message(get_divs(new_future_divs)))
# print(get_divs(new_future_divs))

# print(new_future_divs)
# print(new_past_divs)
