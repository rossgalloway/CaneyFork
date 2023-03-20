from pycoingecko import CoinGeckoAPI
from datetime import datetime
import time
cg = CoinGeckoAPI()
dates = []

# Enter query dates in 'DD-MM-YYY' format
queryDate1 = '29-01-2023'
# Push dates into dates array
dates.append(queryDate1)

# Function to get prices for each date in dates[]
# 5 second wait to be sure not to overload the API, this could probably be shorter
# Call to coinGecko returns a dict and just the price data is pulled out
def getPrices():
    '''Function to get prices for each date in dates[] \n
    5 second wait to be sure not to overload the API, this could probably be shorter \n
    Call to coinGecko returns a dict and just the price data is pulled out'''
    for specificDate in dates:
        print(f'\n getting price for {specificDate}...')
        # time.sleep(5)
        ethPrice1 = (cg.get_coin_history_by_id(
            id='ethereum', date=specificDate, localization='false')['market_data']['current_price']['usd'])
        outputText = " The price of ETH on {0} was :{1}"
        print(outputText.format(specificDate, ethPrice1))

print('\n Starting data retrieval from API...')
getPrices()
print('\n All prices retrieved.')
