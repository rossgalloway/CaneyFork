from pycoingecko import CoinGeckoAPI
import time
cg = CoinGeckoAPI()


# enter query dates in 'DD-MM-YYY' format
queryDate1 = '04-01-2023'
queryDate2 = '11-01-2023'
queryDate3 = '18-01-2023'
queryDate4 = '25-01-2023'
queryDate5 = '01-02-2023'
queryDate6 = '07-02-2023'
queryDate7 = '15-02-2023'
queryDate8 = '22-02-2023'

print('\ngetting data from API...')

# Get Data for ETH on the date desired. each day is a separate call.
print('\n price for date 1...')
ethPriceObject1 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate1, localization='false')
ethPrice1 = ethPriceObject1['market_data']['current_price']['usd']
#wait 5 seconds
print('\n price for date 2...')
time.sleep(5)
ethPriceObject2 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate2, localization='false')
ethPrice2 = ethPriceObject2['market_data']['current_price']['usd']
# wait 5 seconds
print('\n price for date 3...')
time.sleep(5)
ethPriceObject3 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate3, localization='false')
ethPrice3 = ethPriceObject3['market_data']['current_price']['usd']
# wait 5 seconds
print('\n price for date 4...')
time.sleep(5)
ethPriceObject4 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate4, localization='false')
ethPrice4 = ethPriceObject4['market_data']['current_price']['usd']
# wait 5 seconds
print('\n price for date 5...')
time.sleep(5)
ethPriceObject5 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate5, localization='false')
ethPrice5 = ethPriceObject5['market_data']['current_price']['usd']
# wait 5 seconds
print('\n price for date 6...')
time.sleep(5)
ethPriceObject6 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate6, localization='false')
ethPrice6 = ethPriceObject6['market_data']['current_price']['usd']
# wait 5 seconds
print('\n price for date 7...')
time.sleep(5)
ethPriceObject7 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate7, localization='false')
ethPrice7 = ethPriceObject7['market_data']['current_price']['usd']
# wait 5 seconds
print('\n price for date 8...')
time.sleep(5)
ethPriceObject8 = cg.get_coin_history_by_id(
    id='ethereum', date=queryDate8, localization='false')
ethPrice8 = ethPriceObject8['market_data']['current_price']['usd']

outputText = "The price of ETH on {0} was :{1}"

print(outputText.format(queryDate1, ethPrice1))
print(outputText.format(queryDate2, ethPrice2))
print(outputText.format(queryDate3, ethPrice3))
print(outputText.format(queryDate4, ethPrice4))
print(outputText.format(queryDate5, ethPrice5))
print(outputText.format(queryDate6, ethPrice6))
print(outputText.format(queryDate7, ethPrice7))
print(outputText.format(queryDate8, ethPrice8))
