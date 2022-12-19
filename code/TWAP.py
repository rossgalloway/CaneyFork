from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pandas as pd
import time
cg = CoinGeckoAPI()

# Set start date and convert to unix timestamp
# Entered desired date below with yr, mo, day, hr, min.
startdate1 = datetime(2022, 11, 14, 0, 0)
startdate = datetime.timestamp(startdate1)
startdate = str(startdate)
# Set end date and convert to unix timestamp
# Entered desired date below with yr, mo, day, hr, min.
enddate1 = datetime(2022, 12, 20, 0, 0)
enddate = datetime.timestamp(enddate1)
enddate = str(enddate)

print('\ngetting data from API...')
# Import price data from coingecko.
# TWAP data feed. Takes inputs for token, reference currency, and timeframe.
dxdOhlcData = cg.get_coin_ohlc_by_id(id='dxdao', vs_currency='usd', days=30)
# 30 day average price data feed. Takes inputs for token, reference currency, and a specific timeframe.
# Timeframe to be determined with 'startdate' and 'enddate' parameters above
dxdPriceData = cg.get_coin_market_chart_range_by_id(
    id='dxdao', vs_currency='usd', from_timestamp=startdate, to_timestamp=enddate)

# Functions

# option 1. True twap for last 30 days using candle data. Coingecko data gets worse after 30days

def twapPrice(dataFrame):

    # create dataframe and format columns
    print('\ncalculating TWAP...')
    df = pd.DataFrame(dataFrame, columns=[
                      "date", "open", "high", "low", "close"])
    # convert date from unix to date-time so it isn't read in mean calcs.
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    # Calculate the mean of each row
    df['av_row'] = df.mean(axis=1, numeric_only=True)
    # Calculate the TWAP by taking the mean of the means just found
    twap = df['av_row'].mean()
    return twap

# Option 2. Average price over timeframe specified at start.

def avgPrice(dataFrame):

    print('\ncalculating average Price...')
    dfrange = pd.DataFrame(dataFrame)
    # remove un-needed data
    cleanedrange = dfrange.drop(
        ['market_caps', 'total_volumes'], axis='columns')
    # clean up data by splitting list into separate dataframe
    split_range = pd.DataFrame(
        cleanedrange['prices'].tolist(), columns=['date', 'price'])
    # convert date from unix to date-time so it isn't read in mean calcs.
    split_range['date'] = pd.to_datetime(split_range['date'], unit='ms')
    # Calculate the average value by taking the mean of the price column
    averagePrice = split_range['price'].mean()
    return averagePrice

# Output

print('\nlast 30 day TWAP value is : ' + (str(twapPrice(dxdOhlcData))))
print('\nthe average DXD price between ' + str(startdate1) +
      ' and ' + str(enddate1) + ' is: ' + str(avgPrice(dxdPriceData)))
print('\n')
