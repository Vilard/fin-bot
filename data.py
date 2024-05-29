import os
import time
from datetime import datetime, timezone, timedelta
import pytz
import requests


# Задаем время запуска скрипта (час по Московскому времени)
run_hour = 6


def get_html_file():
    '''получаем html файл с текущей датой'''
    # Устанавливаем часовой пояс Москвы
    moscow_tz = pytz.timezone('Europe/Moscow')

    # Создаем папку для сохранения страниц, если она еще не существует
    if not os.path.exists('html'):
        os.makedirs('html')


    # Получаем текущую дату и время в Москве
    now = datetime.now(moscow_tz)

    # Формируем имя файла из текущей даты
    filename = now.strftime('%Y-%m-%d') + '.html'

    # Сохраняем страницу в файл
    response = requests.get('https://smart-lab.ru/dividends/')
    with open(os.path.join('html', filename), 'w', encoding='utf-8') as f:
        f.write(response.text)

get_html_file()