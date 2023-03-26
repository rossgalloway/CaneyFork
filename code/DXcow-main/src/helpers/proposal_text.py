import os
import json
import dotenv
import requests
import textwrap

# Load .env
dotenv.load_dotenv()


def generate_proposal_text(proposal_data):
    """generate text of proposal with info passed in from proposal_data object"""

    order_id = proposal_data["ORDER ID"]
    sell_amount_int = proposal_data["ORDER SELL AMOUNT"]
    sell_amount = (sell_amount_int /
                   (10 ** proposal_data["SELL TOKEN DECIMALS"]))
    sell_token_name = proposal_data["SELL TOKEN NAME"]
    buy_token_name = proposal_data["BUY TOKEN NAME"]
    buy_token_price = proposal_data["BUY TOKEN PRICE"]
    formatted_buy_token_price = f"{buy_token_price:,}"

    # TODO update text and add in price from proposal_data object.
    proposal_text = {
        "description": textwrap.dedent(f"""
            This proposal places a {sell_amount} ({sell_amount_int}) {sell_token_name} Liquidity order on CowSwap to buy DXD. It does so by approving {sell_amount} {sell_token_name} to be spend by Cowswap and signing the following order: https://explorer.cow.fi/orders/{order_id}

            This order is placed as part of the [DXD buyback program] (https://dxvote.eth.limo/#/mainnet/proposal/0x072519e7fa7d55619fcc675c5c47e446e499ee454da1f2b370825ac447d06758).

            The order is placed at a price of {formatted_buy_token_price} {sell_token_name.upper()}/{buy_token_name.upper()} which was calculated to be 70% of treasury NAV in line with [New DXD Token Model](https://alchemy.3ac.vc/dao/0x519b70055af55a007110b4ff99b0ea33071c720a/proposal/0xb7ff31ec2bcdb8a254b8a1b06c6d2080a4089135b03ed55e684fd41b5176d946) using [this spreadsheet](https://docs.google.com/spreadsheets/d/1mS1sVmyP0Z3YiA1JiZpHgPHjSIh3da7MawpjQodE34Y/edit#gid=1664575995). 

            Once this transaction passes and the calls are executed, this order can be accessed by placing a limit order (not a swap) on [Swapr](https://swapr.eth.limo/#/swap?chainId=1) or [Cowswap](https://swap.cow.fi/#/1/limit-orders/DXD/ETH?tab=open&page=1).
            """),
        "title": f"CowSwap Order {order_id[2:10]} to buy {sell_amount} {sell_token_name} worth of DXD",
        "tags": ["cowswap", "buyback"],
        # enter DAOtalk link in url field.
        "url": "",
    }
    return proposal_text


def pin_proposal_text(proposal_text):
    """pin the proposal text object to pinata"""

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    payload = json.dumps(
        {
            "pinataOptions": {"cidVersion": 0},
            "pinataContent": proposal_text
        }
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("PINATA_JWT"),
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, timeout=10)
    cid = response.json()["IpfsHash"]
    print(f"\nIPFS hash: {cid}")
    print(
        f"See your pinned data here (It may take a few minutes to show up): \nhttps://gateway.pinata.cloud/ipfs/{cid}")
    return cid
