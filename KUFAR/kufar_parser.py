import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint

from KUFAR.models import Notebook


class ParserNotebook:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive'
    }
    @classmethod
    def get_soup(cls, url: str) -> BeautifulSoup:
        response = requests.get(url, headers=cls.HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            print(f'{url} | {response.status_code}')


    @staticmethod
    def _get_item_links(soup: BeautifulSoup) -> list:
        links = []
        sections = soup.find_all('section')
        for section in sections:
            link = section.find('a', href=True)['href'].split('?')[0]
            price = section.find('p', class_="styles_price__G3lbO")
            if not price:
                price = section.find('span', class_="styles_price__vIwzP").text
            else:
                price = price.text
            price = re.sub(r'[^0-9]', '', price)
            if price.isdigit():
                links.append(link)

        return links

    @staticmethod
    def _get_notebook_data(soup: BeautifulSoup, url: str) -> Notebook:
        notebook = Notebook(url)

        return notebook

    def run(self):
        url = 'https://www.kufar.by/l/r~minsk/noutbuki'
        links = self._get_item_links(self.get_soup(url))
        notebooks = []
        for link in links:
            soup = self.get_soup(link)
            if soup:
                notebook_data = self._get_notebook_data(soup, link)
        pprint(links)


parser = ParserNotebook()
parser.run()