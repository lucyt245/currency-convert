from requests import get
from pprint import PrettyPrinter

BASE_URL = 'https://free.currconv.com'
API_KEY = '3595273882e54ab3dace'

printer = PrettyPrinter()


def get_currencies():
    end = f'/api/v7/currencies?apiKey={API_KEY}'
    url = BASE_URL + end
    data = get(url).json()['results']

    data = list(data.items())
    data.sort()

    return data


def format_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        acronym = currency.get('id', '')
        symbol = currency.get('currencySymbol', '')

        if symbol != '':
            print(f'{name} - {acronym}, {symbol}')
        else:
            print(f'{name} - {acronym}')


def exchange_rate(cur1, cur2):
    end = f'api/v7/convert?q={cur1}_{cur2}&compact=ultra&apiKey={API_KEY}'
    url = BASE_URL + end
    response = get(url)
    data = response.json()

    if len(data) == 0:
        print ('Invalid currencies')
        return
    
    return list(data.values())[0]
    

data = get_currencies()
format_currencies(data)
