from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import time
import csv
cg = CoinGeckoAPI()
start_date = datetime(2022, 6, 1)  # start date of time period
end_date = datetime(2023, 2, 23)  # end date of time period
# end_date = datetime(2022, 7, 1)  # end date of time period
dates = []


def getDates():
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == 0:  # check if current date is a Monday (0 represents Monday)
            current_date_string = current_date.strftime("%d-%m-%Y")
            dates.append(current_date_string)
        current_date += timedelta(days=1)  # add one day to current date

# To append custom dates, enter query dates in 'DD-MM-YYY' format
# customDate1 = '01-01-2023'
# Push custom dates into dates array
# dates.append(queryDate1)



def getBenchmarkPrices():
    print(f'\n getting Benchmark prices for {dates[0]}...')
    time.sleep(5)
    dxdBenchmarkDict = cg.get_coin_history_by_id(
        id='dxdao', date=dates[0], localization='false')
    dxdBenchmarkUSD = dxdBenchmarkDict['market_data']['current_price']['usd']
    dxdBenchmarkETH = dxdBenchmarkDict['market_data']['current_price']['eth']
    outputText = " The benchmark price of DXD in USD on {0} was :{1}"
    print(outputText.format(dates[0], dxdBenchmarkUSD))
    outputText = " The benchmark price of DXD in ETH on {0} was :{1}"
    print(outputText.format(dates[0], dxdBenchmarkETH))
    return dxdBenchmarkUSD, dxdBenchmarkETH

# Function to get prices for each date in dates[]
# 5 second wait to be sure not to overload the API, this could probably be shorter
# Call to coinGecko returns a dict and just the price data is pulled out
# I want to output a file in the following format: PriceData = { date1 { UsdPrice, EthPrice, BenchmarkPrice }, date2 { UsdPrice, EthPrice, BenchmarkPrice }...}

def getPrices(dxdBenchmarkUSD, dxdBenchmarkETH):
    PriceData = {}
    priceDataCsv = []
    for specificDate in dates:
        print(f'\n getting price for {specificDate}...')
        time.sleep(10)
        dxdDict = cg.get_coin_history_by_id(
            id='dxdao', date=specificDate, localization='false')

        dxdUSD = dxdDict['market_data']['current_price']['usd']
        dxdETH = dxdDict['market_data']['current_price']['eth']

        benchmarkDeltaUSD = ((dxdUSD - dxdBenchmarkUSD)/dxdBenchmarkUSD)*(1/3)
        benchmarkDeltaETH = ((dxdETH - dxdBenchmarkETH)/dxdBenchmarkETH)*(2/3)
        finalBenchmarkDelta = 1 + benchmarkDeltaETH + benchmarkDeltaUSD

        PriceData[specificDate] = {
            'UsdPrice': dxdUSD, 'EthPrice': dxdETH, 'BenchmarkPrice': finalBenchmarkDelta}
        priceDataCsv.append([specificDate, dxdUSD, dxdETH, finalBenchmarkDelta])

    return PriceData, priceDataCsv

        # outputText = " The price of DXD in USD on {0} was :{1}"
        # print(outputText.format(specificDate, dxdUSD))
        # # outputText = " The change from the USD benchmark on {0} was :{1}"
        # # print(outputText.format(specificDate, benchmarkDeltaUSD))
        # outputText = " The price of DXD in ETH on {0} was :{1}"
        # print(outputText.format(specificDate, dxdETH))
        # # outputText = " The change from the ETH benchmark on {0} was :{1}"
        # # print(outputText.format(specificDate, benchmarkDeltaETH))
        # outputText = " The change from the benchmark on {0} was :{1}"
        # print(outputText.format(specificDate, finalBenchmarkDelta))


print('\n Starting data retrieval from API...')
print(' Getting DXD prices in USD and ETH and a custom benchmark of 2/3 ETH and 1/3 USD...')
getDates()
result1, result2 = getBenchmarkPrices()
PriceData, PriceDataCsv = getPrices(result1, result2)
print('\n All prices retrieved.')

print('\n Saving to CSV...')

with open('output/PriceDataCsv.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'USD Price', 'ETH Price', 'Benchmark Price'])
    writer.writerows(PriceDataCsv)

print('\n Saved and Complete.')

# with open('output/PriceData.txt', 'w') as f:
#     for date in PriceData:
#         usdPrice = PriceData[date]['UsdPrice']
#         ethPrice = PriceData[date]['EthPrice']
#         benchmarkPrice = PriceData[date]['BenchmarkPrice']
#         f.write(
#             f'{date} {{ UsdPrice: {usdPrice}, EthPrice: {ethPrice}, BenchmarkPrice: {benchmarkPrice} }}\n')

