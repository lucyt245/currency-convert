from requests import get
from pprint import PrettyPrinter

BASE_URL = 'https://free.currconv.com'
API_KEY = '3595273882e54ab3dace'

printer = PrettyPrinter()


def get_currencies():
    # gets a list of currencies
    end = f'/api/v7/currencies?apiKey={API_KEY}'
    url = BASE_URL + end
    data = get(url).json()['results']

    data = list(data.items())
    data.sort()

    return data


def menu_system():
    while True:
        print(''' 
        -------
        0. Quit
        1. Currency covert
        2. Currency list
        3. Exchange rate
        -------''')

        data = get_currencies()

        choice = int(input('Enter your choice: '))
        # allows user to pick what they would like to do
        if choice == 1:
            cur1, cur2 = choose_currencies(data)
            currency_convert(cur1, cur2)
        elif choice == 2:
            currency_list(data)
        elif choice == 3:
            cur1, cur2 = choose_currencies(data)
            rate = exchange_rate(cur1, cur2)
            print(f'{cur1} -> {cur2} = {rate}')
        elif choice == 0:
            break
        else:
            print('Invalid option')


def choose_currencies(data):
    acronyms = []
    for name, currency in data:
        acronyms.append(currency.get('id', ''))

    cur1 = input('Enter base currency: ')
    # checks that the input is a valid currency abbreviation
    if cur1.upper() not in acronyms:
        print('Not a valid currency')
        choose_currencies(data)
    
    cur2 = input('Enter currency to convert to: ')
    if cur2.upper() not in acronyms:
        print('Not a valid currency')
        choose_currencies(data)

    return cur1, cur2


def currency_list(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        acronym = currency['id']
        # returns empty if currency has no symbol
        symbol = currency.get('currencySymbol', '')
        
        # formats the output so it is more readable
        # gets rid of empty space if currency has no symbol
        if symbol != '':
            print(f'{name} - {acronym}, {symbol}')
        else:
            print(f'{name} - {acronym}')


def exchange_rate(cur1, cur2):
    # finds the exchange rate between the base currency (cur1) and the one it is to be converted to (cur2)
    end = f'/api/v7/convert?q={cur1}_{cur2}&compact=ultra&apiKey={API_KEY}'
    url = BASE_URL + end
    response = get(url)
    data = response.json()
    
    return list(data.values())[0]


def currency_convert(cur1, cur2):
    # finds the exchange rate
    rate = exchange_rate(cur1, cur2)

    amount = float(input('How much do you want to convert? '))

    # finds the converted amount
    converted = amount * rate
    print(f'{amount} {cur1} = {converted} {cur2}')


menu_system()
