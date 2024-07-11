import util

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

import pandas as pd
import csv
import datetime


def update_df(service):
    df = pd.read_csv('data.csv')

    huds = util.get_huds()

    for headline, url, date_raw in huds:
        if url in df['url']:
            continue

        html = util.get_html_content(url)

        text = util.html2text(html)

        date = datetime.datetime.strptime(date_raw, '%Y-%m-%dT%H:%M:%SZ')

        new_row = [date, headline, text, url]

        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)


service = Service(GeckoDriverManager().install())

# df = pd.DataFrame(columns=['date', 'headline', 'text', 'url'])
# df.to_csv('data.csv')

update_df(service)
