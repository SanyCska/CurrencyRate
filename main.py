from bitzlato import bitzlato_main
from google_sheets import update_main_page
from local_bitcoins import local_bitcoins_main
from local_coins_swap import local_coins_swap_main
from paxful import paxful_main

all_extra_charges = []
all_extra_charges.extend(local_bitcoins_main())
all_extra_charges.extend(local_coins_swap_main())
all_extra_charges.extend(bitzlato_main())
all_extra_charges.extend(paxful_main())
update_main_page(all_extra_charges)
