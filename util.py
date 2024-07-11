import requests
import json
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from fp.fp import FreeProxy  # Assuming you have the FreeProxy library installed
from bs4 import BeautifulSoup


def get_huds(url: str = 'https://bcs-express.ru/category/rossiyskiy-rynok'):
    """Get an array with 10 last news items in HUD format (headline, url, date)"""
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    soup = BeautifulSoup(response.content, 'html.parser')

    script_tag = soup.find('script', type='application/ld+json')

    json_data = json.loads(script_tag.string)

    huds = []

    for item1 in json_data['@graph']:
        if item1['@type'] == 'ItemList':
            for item2 in item1['itemListElement']:

                item = item2['item']
                date = item['datePublished']
                headline = item['headline']
                url = item['mainEntityOfPage']['@id']

                huds.append((headline, url, date))

    return huds

def get_html_content(url, service=None, proxy=None):
    """Utilizes random proxy and selenium to access bcs-express website"""
    options = Options()
    options.add_argument('--headless')  # Run headless Firefox
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    if not service:
        service = Service(GeckoDriverManager().install())
    
    if not proxy:
        proxy = FreeProxy(rand=True, country_id=['RU'], elite=True).get()
    
    options.add_argument(f'--proxy-server={proxy}')
    
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html
    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")
        if 'ERR_CONNECTION_RESET' in str(e):
            print("Connection was reset. Please check the proxy and network settings.")
        # Add more specific error handling as needed
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

def html2text(html_content: str):
    """Parses out text from the HTML of bcs-express website"""
    soup = BeautifulSoup(html_content, 'html.parser')

    p_tags = soup.find_all('p')
    text = ""
    for p in p_tags:
        if 'Компания БКС' in p.text \
                or 'Компания хочет направить привлеченные средства на финансирование инвестиционной программы' in p.text \
                or 'БКС Мир инвестиций' in p.text:
            break
        text += p.text + '\n'
    return text