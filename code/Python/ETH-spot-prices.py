from pycoingecko import CoinGeckoAPI
from datetime import datetime
import time
cg = CoinGeckoAPI()
dates = []

# Enter query dates in 'DD-MM-YYY' format
queryDate1 = '29-01-2023'
# Push dates into dates array
dates.append(queryDate1)
# queryDate2 = '12-02-2023'
# dates.append(queryDate2)
# queryDate3 = '18-01-2023'
# dates.append(queryDate3)
# queryDate4 = '25-01-2023'
# dates.append(queryDate4)
# queryDate5 = '01-02-2023'
# dates.append(queryDate5)
# queryDate6 = '07-02-2023'
# dates.append(queryDate6)
# queryDate7 = '15-02-2023'
# dates.append(queryDate7)
# queryDate8 = '22-02-2023'
# dates.append(queryDate8)


# Function to get prices for each date in dates[]
# 5 second wait to be sure not to overload the API, this could probably be shorter
# Call to coinGecko returns a dict and just the price data is pulled out
def getPrices():
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
