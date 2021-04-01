import bs4
from selenium import webdriver

from common import save_prices, PLATFORM_NAMES


def get_bitzlato_prices(url):
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, "html.parser")
    driver.close()

    prices_tags = soup.find_all('div', class_='jss191 jss189')
    prices = []
    for p in prices_tags:
        prices.append(p.text.split('BTC')[1])
    return prices


def bitzlato_main():
    bitzlato_extra_charges = []
    ru_desc = 'bitzlato russian sellers'
    print(ru_desc)
    ru_prices = get_bitzlato_prices('https://bitzlato.bz/p2p?currency=RUB&isOwnerActive=true')
    ru_extra_charge = save_prices('RUB', ru_prices, PLATFORM_NAMES['bitzlato_ru'])
    bitzlato_extra_charges.append([
        ru_desc, ru_extra_charge
    ])

    usa_desc = 'bitzlato usa sellers'
    print(usa_desc)
    us_prices = get_bitzlato_prices('https://bitzlato.bz/p2p?currency=USD&isOwnerActive=true')
    usa_extra_charge = save_prices('BUSD', us_prices, PLATFORM_NAMES['bitzlato_usd'])
    bitzlato_extra_charges.append([usa_desc, usa_extra_charge])

    eur_desc = 'bitzlato euro sellers'
    print(eur_desc)
    eur_prices = get_bitzlato_prices('https://bitzlato.bz/p2p?currency=USD&isOwnerActive=true')
    eur_extra_charge = save_prices('EUR', eur_prices, PLATFORM_NAMES['bitzlato_eur'])
    bitzlato_extra_charges.append([eur_desc, eur_extra_charge])

    gbp_desc = 'bitzlato british sellers'
    print(gbp_desc)
    gbp_prices = get_bitzlato_prices('https://bitzlato.bz/p2p?currency=GBP&isOwnerActive=true')
    gbp_extra_charge = save_prices('GBP', gbp_prices, PLATFORM_NAMES['bitzlato_gbp'])
    bitzlato_extra_charges.append([gbp_desc, gbp_extra_charge])
    return bitzlato_extra_charges
