from pycoingecko import CoinGeckoAPI
from datetime import datetime
import time
import flatdict
cg = CoinGeckoAPI()

# Enter coingecko asset IDs
assets = ['ethereum', 'seth2', 'swapr', 'liquity-usd', 'staked-ether',
          'ethereum-name-service', 'reth2', 'bitcoin', 'defipulse-index', 'gnosis']

# Function to get prices for each date in dates[] and each asset is assets[]
# 5 second wait to be sure not to overload the API, this could probably be shorter
# Call to coinGecko returns a dict and just the price data is pulled out


def getPrices():
    print(f'\n getting current prices for DXD Treasury Assets...\n')
    prices = (cg.get_price(
        ids=assets, vs_currencies='usd'))
    for asset in assets:
        print(asset,': ',prices[asset]['usd'])


print('\n Starting data retrieval from API...')
getPrices()
print('\n All prices retrieved.')
