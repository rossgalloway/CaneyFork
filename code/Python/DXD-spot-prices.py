from datetime import datetime, timedelta
import time
import csv
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# set your start and end dates here
start_date = datetime(2022, 6, 1)  # start date of time period
end_date = datetime(2023, 2, 23)  # end date of time period
dates = []

def getDates():
    '''function to find all mondays between start_date and end_date'''
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 0:  # check if current date is a Monday (0 represents Monday)
            current_date_string = current_date.strftime("%d-%m-%Y")
            dates.append(current_date_string)
        current_date += timedelta(days=1)  # add one day to current date

# # To append custom dates, enter query dates in 'DD-MM-YYY' format
# customDate1 = '01-01-2023'
# # Push custom dates into dates array
# dates.append(queryDate1)

def getBenchmarkPrices():
    '''Funtion to get price for DXD on start_date in USD and ETH'''
    print(f'\n getting Benchmark prices based on prices from {dates[0]}...')
    # call coingecko API for DXD price info 
    dxdBenchmarkDict = cg.get_coin_history_by_id(
        id='dxdao', date=dates[0], localization='false')
    # get DXD price in USD
    dxdBenchmarkUSD = dxdBenchmarkDict['market_data']['current_price']['usd']
    # get DXD price in ETH
    dxdBenchmarkETH = dxdBenchmarkDict['market_data']['current_price']['eth']
    print(f"The benchmark price of DXD in USD on {dates[0]} was :{dxdBenchmarkUSD}")
    print(f"The benchmark price of DXD in USD on {dates[0]} was :{dxdBenchmarkETH}")
    return dxdBenchmarkUSD, dxdBenchmarkETH

# Function to get prices for each date in dates[]
# 5 second wait to be sure not to overload the API, this could probably be shorter
# Call to coinGecko returns a dict and just the price data is pulled out
# I want to output a file in the following format: PriceData = { date1 { UsdPrice, EthPrice, BenchmarkPrice }, date2 { UsdPrice, EthPrice, BenchmarkPrice }...}

def getPrices(dxdBenchmarkUSD, dxdBenchmarkETH):
    '''function to get prices and compare them to a benchmark'''
    priceDataCsv = []
    for specificDate in dates:
        print(f'getting price for {specificDate}...')
        # call coingecko API for DXD price info
        dxdDict = cg.get_coin_history_by_id(
            id='dxdao', date=specificDate, localization='false')
        # extract USD and ETH denominated prices
        dxdUSD = dxdDict['market_data']['current_price']['usd']
        dxdETH = dxdDict['market_data']['current_price']['eth']
        # Calculate change from benchmark by asset
        benchmarkDeltaUSD = ((dxdUSD - dxdBenchmarkUSD)/dxdBenchmarkUSD)
        benchmarkDeltaETH = ((dxdETH - dxdBenchmarkETH)/dxdBenchmarkETH)
        finalBenchmarkDelta = 1 + (benchmarkDeltaETH*(2/3)) + (benchmarkDeltaUSD*(1/3))
        priceDataCsv.append([specificDate, dxdUSD, dxdETH, finalBenchmarkDelta])
        time.sleep(5)
    return priceDataCsv

print('\n Starting data retrieval from API...')
print(' Getting DXD prices in USD and ETH and a custom benchmark of 2/3 ETH and 1/3 USD...')
getDates()
result1, result2 = getBenchmarkPrices()
PriceDataCsv = getPrices(result1, result2)
print('\n All prices retrieved.')

print('\n Saving to CSV...')

with open('output/PriceDataCsv.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'USD Price', 'ETH Price', 'Benchmark Price'])
    writer.writerows(PriceDataCsv)

print('\n Saved and Complete.')
