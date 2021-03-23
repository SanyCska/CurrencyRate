import bs4
import requests

from common import save_prices, PLATFORM_NAMES


def get_local_coins_swap_prices(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    sellers = soup.find_all('div', class_='bg-white dark:bg-dgrey-700 rounded-lg p-2 lg:p-4 mt-3')
    prices_list = []
    for s in sellers:
        price = s.find('div', class_='text-lg lg:text-xl text-green font-600')
        prices_list.append(price.text.replace(',', '').strip().split(' ')[0])
    return prices_list


def local_coins_swap_main():
    local_coins_swap_extra_charges = []
    usa_desc = 'localCoinsSwap usa sellers'
    print(usa_desc)
    us_prices = get_local_coins_swap_prices('https://localcoinswap.com/ru/buy/BTC/united-states/all-payments?buy-sort=current_price_usd&fiat-currency=USD&country-code=US&hide-new=1')
    usa_extra_charge = save_prices('BUSD', us_prices, PLATFORM_NAMES['local_coins_swap_usd'])
    local_coins_swap_extra_charges.append([
        usa_desc, usa_extra_charge
    ])
    ru_desc = 'localCoinsSwap russian sellers'
    print(ru_desc)
    ru_prices = get_local_coins_swap_prices('https://localcoinswap.com/ru/buy/BTC/russian-federation/all-payments?buy-sort=current_price_usd&fiat-currency=RUB&country-code=RU&hide-new=1')
    ru_extra_charge = save_prices('RUB', ru_prices, PLATFORM_NAMES['local_coins_swap_ru'])
    local_coins_swap_extra_charges.append([
        ru_desc, ru_extra_charge
    ])
    return local_coins_swap_extra_charges