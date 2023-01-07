import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup


PERIODS = {
    '1': 1,
    '2': 2,
    '3': 4,
    '4': 5,
    '5': 10,
    '6': 15,
    '7': 20,
    '8': 25,
    '9': 30,
}


def url2dict(url: str) -> dict:
    res = dict()
    res['url'] = url.split('?')[0]
    if len(url.split('?')) == 2:
        for param in url.split('?')[1].split('&'):
            name, value = param.split('=')
            res[name] = value
    return res


def read(price, initial_fee, child, purpose_type):
    payload = {
        'initialFee': initial_fee,  # первоначальный взнос
        'price': price,  # цена жилья
        'isHaveChildBefore2018': 0 if child == 0 else 1,  # имеется ли ребенок рожденный после 2018
        'purposeIds[]': 2 if purpose_type == 'new' else 1,
        'specialProgramIds[]': -1,
    }
    start_urls = ['https://www.banki.ru/products/hypothec/search/moskva/?'
                           + urlencode({**payload, **{'period': i}}) for i in range(1, 10)]
    for url in start_urls:
        page = requests.get(url).content.decode("utf-8")
        soup = BeautifulSoup(page, 'html.parser')
        bank_items = soup.find_all('td')
        for i in range(7, len(bank_items), 6):
            item = dict()
            item['bank'] = bank_items[i].contents[0]
            item['mortgage_rate'] = float(bank_items[i + 1].contents[0].replace(' %', '').replace(',', '.'))
            item['payment_per_mouth'] = int(bank_items[i + 2].contents[0].replace(' ', '').replace('₽', ''))
            item['period'] = PERIODS[url2dict(url)['period']]
            item['overpayment'] = item['payment_per_mouth'] * 12 * item['period'] + initial_fee - price
            yield item

