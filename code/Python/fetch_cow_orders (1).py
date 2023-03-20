import requests
import pandas as pd

# Request current Cow auction
r = requests.get('https://api.cow.fi/mainnet/api/v1/auction')

orders = r.json()['orders']

DXD = '0xa1d65E8fB6e87b60FECCBc582F7f97804B725521'.lower()

dxd_orders = [i for i in orders if i['sellToken'] == DXD]

# Create a dataframe with the orders
df = pd.DataFrame(dxd_orders)

df.to_csv('sell_orders.csv', index=False)

dxd_orders = [i for i in orders if i['buyToken'] == DXD]

# Create a dataframe with the orders
df = pd.DataFrame(dxd_orders)

df.to_csv('buy_orders.csv', index=False)