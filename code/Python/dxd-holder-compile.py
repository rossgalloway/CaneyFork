# dxd-holder-compile.py

# Import Pandas and Web3 Libraries
# You may need to install pandas and web3 for this script to run
import pandas as pd
from web3 import Web3

# Define a function to divide values in 18 decimal form
# Check spreadsheets to determine format from etherscan export
def format_value(value):
    return value/10**18

print('opening and formatting csv files...')

# Load the CSV files into separate dataframes. Only bring in addresses and balances columns
eth_df = pd.read_csv('input/dxd-mainnet-03-13-2023.csv',
                     usecols=['HolderAddress', 'Balance'])
arb_df = pd.read_csv('input/dxd-arbitrum-03-13-2023.csv',
                     usecols=['HolderAddress', 'Balance'])
gno_df = pd.read_csv('input/dxd-gnosis-chain-03-13-2023.csv',
                     usecols=['HolderAddress', 'Balance'])

# Rename the balance columns
eth_df = eth_df.rename(columns={'Balance': 'ethereum_balance'})
arb_df = arb_df.rename(columns={'Balance': 'arbitrum_balance'})
gno_df = gno_df.rename(columns={'Balance': 'gnosis_balance'})

# format data to show DXD value in expected units if needed
eth_df['ethereum_balance'] = eth_df['ethereum_balance'].apply(format_value)

# Merge the dataframes based on the "HolderAddress" column
merged_df = pd.merge(eth_df, arb_df, on='HolderAddress', how='outer')
merged_df = pd.merge(merged_df, gno_df, on='HolderAddress', how='outer')

# fill in missing values with 0
merged_df = merged_df.fillna(0)

# Convert HolderAddress column to checksum address
merged_df['HolderAddress'] = merged_df['HolderAddress'].apply(
    Web3.toChecksumAddress)

# Add a new column that sums the balance columns for each row
merged_df['total_balance'] = merged_df['ethereum_balance'] + merged_df['arbitrum_balance'] + merged_df['gnosis_balance']
merged_df = merged_df[merged_df['total_balance'] > 0.000001]

# Sort the dataframe by the total_balance column
merged_df = merged_df.sort_values(by='total_balance', ascending=False)

# print(merged_df['arbitrum_balance'])
merged_df.to_csv('output/test_output.csv', index=False)

# run by typing `python3 dxd-holder-compile.py` in the console