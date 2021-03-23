import bs4
import requests

from common import save_prices, PLATFORM_NAMES
from settings import LOCAL_BITCOINS_API_KEY


def get_local_bitcoins_prices_ru():
    url = 'https://localbitcoins.net.ru/'
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    prices_tags = soup.find_all('th', class_='text-success')
    prices = []
    for p in prices_tags[0:10]:
        prices.append(p.text)
    return prices


# Структура json файла
# {
#     date: {
#         list: [],
#         currency: string,
#         extra_charge: string,
#         rate: string
#     }
#     common_extra_charge: string
# }


def get_local_bitcoins_prices_foreign_sellers(url):
    # VOVA_TOR_LINK = "mlshitcheatsheet.ru:9050"
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = VOVA_TOR_LINK
    # prox.socks_proxy = VOVA_TOR_LINK
    # prox.ssl_proxy = VOVA_TOR_LINK
    #
    # #
    # capabilities = webdriver.DesiredCapabilities.FIREFOX
    # capabilities['marionette'] = True
    # capabilities['proxy'] = {
    #     "proxyType": "MANUAL",
    #     # "httpProxy": '120.203.215.6:80'
    #     # "ftpProxy": f'socks5h://{VOVA_TOR_LINK}',
    #     # "sslProxy": VOVA_TOR_LINK
    #     # 'socksProxy': VOVA_TOR_LINK,
    #     'socksProxy': '72.223.168.67:4145',
    #     'socksVersion': 5
    # }
    # driver = webdriver.Firefox(desired_capabilities=capabilities, proxy=prox)
    # driver.get(url)
    # html = driver.page_source
    # print(html)

    headers = {
        "apikey": LOCAL_BITCOINS_API_KEY
    }

    params = (
        ("url", url),
        ("render", "true"),
    )

    r = requests.get('https://app.zenscrape.com/api/v1/get', headers=headers, params=params)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    price_tags = soup.find_all('td', class_='column-price')
    prices = []
    for p in price_tags[0:10]:
        prices.append(p.text.replace(',', '').strip().split(' ')[0])
    return prices


def local_bitcoins_main():
    local_bitcoins_extra_charges = []
    ru_desc = 'local bitcoins russian sellers'
    print(ru_desc)
    ru_prices = get_local_bitcoins_prices_ru()
    ru_extra_charge = save_prices('RUB', ru_prices, PLATFORM_NAMES['local_bitcoin_ru'])
    local_bitcoins_extra_charges.append([
        ru_desc, ru_extra_charge
    ])
    usa_desc = 'local bitcoins USA sellers'
    print(usa_desc)
    us_prices = get_local_bitcoins_prices_foreign_sellers('https://localbitcoins.net/instant-bitcoins/?action=buy&amount=&currency=USD&country_code=US&online_provider=ALL_ONLINE&find-offers=Search')
    usa_extra_charge = save_prices('BUSD', us_prices, PLATFORM_NAMES['local_bitcoin_usd'])
    local_bitcoins_extra_charges.append([
        usa_desc, usa_extra_charge
    ])
    gb_desc = 'local bitcoins GB sellers'
    print(gb_desc)
    gbp_prices = get_local_bitcoins_prices_foreign_sellers('https://localbitcoins.net/instant-bitcoins/?action=buy&amount=&currency=GBP&country_code=GB&online_provider=ALL_ONLINE&find-offers=Search')
    gb_extra_charge = save_prices('GBP', gbp_prices, PLATFORM_NAMES['local_bitcoin_gb'])
    local_bitcoins_extra_charges.append([
        gb_desc, gb_extra_charge
    ])
    eu_desc = 'local bitcoins euro sellers'
    print(eu_desc)
    eur_prices = get_local_bitcoins_prices_foreign_sellers(
        'https://localbitcoins.net/instant-bitcoins/?action=buy&amount=&currency=EUR&country_code=DE&online_provider=ALL_ONLINE&find-offers=Search')
    eu_extra_charge = save_prices('EUR', eur_prices, PLATFORM_NAMES['local_bitcoin_eur'])
    local_bitcoins_extra_charges.append([
        eu_desc, eu_extra_charge
    ])
    return local_bitcoins_extra_charges