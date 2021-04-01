import datetime
import json
import os

from binance.client import Client

from google_sheets import update_data_in_table, init_sheet
from settings import BINANCE_API_KEY, BINANCE_API_SECRET


def get_extra_charge(price, currency):
    return (float(price)/float(currency) - 1) * 100


def get_rate(currency):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    # get balance for a specific asset only (BTC)
    return client.get_symbol_ticker(symbol="BTC" + currency)['price']


def get_common_extra_charge(extra_charges):
    sum = 0
    for c in extra_charges:
        sum += c
    return sum / 10


def save_prices(currency, prices, project_name):

    btc_rate = get_rate(currency)

    extra_charges = []
    for price in prices:
        extra_charges.append(get_extra_charge(price, btc_rate))

    daily_extra_charge = get_common_extra_charge(extra_charges)

    current_datetime = str(datetime.datetime.now())
    current_date_dict = {
        'list': prices,
        'currency': currency,
        'rate': btc_rate,
        'extra_charge': daily_extra_charge
    }

    file_path = 'data/%s.json' % project_name
    if not os.path.exists(file_path):
        new_file = open(file_path, "w")
        new_file.write('')
        new_file.close()

    is_new = False

    with open(file_path, 'r+') as localBTCruFile:
        files_data = localBTCruFile.read()
        if not files_data:
            is_new = True
        if not is_new:
            local_bitcoins_dict = json.loads(files_data)
        else:
            local_bitcoins_dict = {'common_extra_charge': 0}

        if daily_extra_charge == 0:
            print('Daily extra charge is null')
            localBTCruFile.close()
            return local_bitcoins_dict['common_extra_charge']

        if not is_new:
            sum = 0
            for key in local_bitcoins_dict.keys():
                if key == 'common_extra_charge':
                    continue
                else:
                    sum += float(local_bitcoins_dict[key]['extra_charge'])

            common_extra_charge = sum / (len(local_bitcoins_dict) - 1)
            update_data_in_table(project_name, current_date_dict, current_datetime, common_extra_charge)
        else:
            common_extra_charge = daily_extra_charge

        print('common_extra_charge: ' + str(common_extra_charge))

        local_bitcoins_dict[current_datetime] = current_date_dict
        local_bitcoins_dict['common_extra_charge'] = common_extra_charge
        localBTCruFile.seek(0)
        localBTCruFile.truncate()
        localBTCruFile.write(json.dumps(local_bitcoins_dict))
        localBTCruFile.close()
    if is_new:
        init_sheet(project_name)
    return common_extra_charge

PLATFORM_NAMES = {
    'bitzlato_ru': 'bitzlato_ru',
    'bitzlato_usd': 'bitzlato_usd',
    'bitzlato_eur': 'bitzlato_eur',
    'bitzlato_gbp': 'bitzlato_gbp',
    'local_bitcoin_eur': 'local_bitcoin_eur',
    'local_bitcoin_gb': 'local_bitcoin_gb',
    'local_bitcoin_usd': 'local_bitcoin_usd',
    'local_bitcoin_ru': 'local_bitcoin_ru',
    'local_coins_swap_ru': 'local_coins_swap_ru',
    'local_coins_swap_usd': 'local_coins_swap_usd',
    'local_coins_swap_gbp': 'local_coins_swap_gbp',
    'local_coins_swap_eur': 'local_coins_swap_eur',
    'paxful_ru': 'paxful_ru',
    'paxful_usd': 'paxful_usd',
    'paxful_eur': 'paxful_eur',
    'paxful_gbp': 'paxful_gbp',
}