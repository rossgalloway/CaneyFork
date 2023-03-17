from pycoingecko import CoinGeckoAPI
from datetime import datetime
import time
cg = CoinGeckoAPI()
dates = []

# Enter query dates in 'DD-MM-YYY' format
dates = ['10-03-2023']

# Enter coingecko asset IDs 
assets = ['ethereum', 'bitcoin', 'swapr',
          'ethereum-name-service', 'gnosis', 'defipulse-index']

# Function to get prices for each date in dates[] and each asset is assets[]
# 5 second wait to be sure not to overload the API, this could probably be shorter
# Call to coinGecko returns a dict and just the price data is pulled out
def getPrices():
    for specificDate in dates:
        print(f'\n getting prices for {specificDate}...')
        for specificAsset in assets:
            price = (cg.get_coin_history_by_id(
                id=specificAsset, date=specificDate, localization='false')['market_data']['current_price']['usd'])
            outputText = " The price of {2} on {0} was :{1}"
            print(outputText.format(specificDate, price, specificAsset))
            time.sleep(5)

print('\n Starting data retrieval from API...')
getPrices()
print('\n All prices retrieved.')
