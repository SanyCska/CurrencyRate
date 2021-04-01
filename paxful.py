from common import save_prices, PLATFORM_NAMES
import hmac
import time
from hashlib import sha256
from urllib.parse import urlencode

import requests  # pip install requests


def get_paxful_prices(params):

    API_URL = "https://paxful.com/api/offer/all"
    # nonce = int(time.time())
    #
    # payload = {"apikey": API_KEY, "nonce": nonce}
    # payload = urlencode(sorted(payload.items()))
    # apiseal = hmac.new(API_SECRET.encode(), payload.encode(), sha256).hexdigest()
    # data_with_apiseal = payload + "&apiseal=" + apiseal + '&offer_type=buy'
    headers = {"Accept": "application/json", "Content-Type": "text/plain"}
    resp = requests.post(API_URL, data=params, headers=headers)
    offers = resp.json()['data']['offers']
    prices_list = []
    for o in offers[0:10]:
        prices_list.append(o['fiat_price_per_btc'])
    return prices_list


def paxful_main():
    paxful_extra_charges = []
    usa_desc = 'paxful usa sellers'
    print(usa_desc)
    us_prices = get_paxful_prices('&offer_type=buy&currency_code=USD')
    usa_extra_charge = save_prices('BUSD', us_prices, PLATFORM_NAMES['paxful_usd'])
    paxful_extra_charges.append([
        usa_desc, usa_extra_charge
    ])

    ru_desc = 'paxful russian sellers'
    print(ru_desc)
    ru_prices = get_paxful_prices('&offer_type=buy&currency_code=RUB')
    ru_extra_charge = save_prices('RUB', ru_prices, PLATFORM_NAMES['paxful_ru'])
    paxful_extra_charges.append([
        ru_desc, ru_extra_charge
    ])

    gbp_desc = 'paxful british sellers'
    print(gbp_desc)
    gbp_prices = get_paxful_prices('&offer_type=buy&currency_code=GBP')
    gbp_extra_charge = save_prices('GBP', gbp_prices, PLATFORM_NAMES['paxful_gbp'])
    paxful_extra_charges.append([
        gbp_desc, gbp_extra_charge
    ])

    eur_desc = 'paxful euro sellers'
    print(eur_desc)
    eur_prices = get_paxful_prices('&offer_type=buy&currency_code=EUR')
    eur_extra_charge = save_prices('EUR', eur_prices, PLATFORM_NAMES['paxful_eur'])
    paxful_extra_charges.append([
        eur_desc, eur_extra_charge
    ])
    return paxful_extra_charges