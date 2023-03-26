from time import time
import json
import requests
from requests.exceptions import RequestException
import emoji

def cowswap_liquidity_order(proposal_data):
    """function to submit a new order to the CowSwap API"""

    sell_token = proposal_data['SELL TOKEN ADDRESS']
    sell_amount = proposal_data['ORDER SELL AMOUNT']
    sell_token_price = proposal_data['SELL TOKEN PRICE']
    sell_token_decimals = proposal_data['SELL TOKEN DECIMALS']
    buy_token = proposal_data['BUY TOKEN ADDRESS']
    avatar = proposal_data['AVATAR']
    cow_api = proposal_data['COW API']
    cow_settlement_address = proposal_data['COW SETTLEMENT']

    # Set 40 day deadline
    deadline = int(time()) + 60 * 60 * 24 * 40  # 40 days

    # buy amount = sell amount * dxd/{sell_token_price}
    sell_amount_safe = sell_amount / (10**sell_token_decimals)
    buy_amount = int((sell_amount_safe * sell_token_price) * 10**sell_token_decimals)

    # set order parameters here
    order_payload = {
        "settlementContract": cow_settlement_address,
        "fullFeeAmount": "0",
        "isLiquidityOrder": True, 
        "sellToken": sell_token,
        "buyToken": buy_token,
        "receiver": avatar,
        "sellAmount": str(sell_amount),
        "buyAmount": str(buy_amount),
        "validTo": deadline,
        "appData": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "feeAmount": "0",
        "kind": "buy",
        "partiallyFillable": True, 
        "sellTokenBalance": "erc20",
        "buyTokenBalance": "erc20",
        "signingScheme": "presign",
        "signature": "0x",
        "from": avatar,
        "quoteId": 0
    }

    print("\nOrder Created! Please review your order:")
    print("-----------------------------------------------------------------------------------------")
    for key, value in order_payload.items():
        print(f'{key}: {value}')
    print("-----------------------------------------------------------------------------------------")

    # Ask user if they want to submit this CowSwap order   
    submit = input("\n>>>Do you want to submit this CowSwap order to the orderbook? (y/n): ")
    if submit.upper() == "Y":

        # Submit order to the Cowswap "orders" endpoint
        orders_url = cow_api + "orders"
        # r_order = requests.post(orders_url, json=order_payload, timeout=10)
        # # TODO improve error handling
        # assert r_order.ok and r_order.status_code == 201
        try:
            r_order = requests.post(orders_url, json=order_payload, timeout=10)
            r_order.raise_for_status()
        except RequestException as error:
            if error.response is not None:
                error_message = f"Error creating order: {error.response.status_code} - {error.response.text}"
            else:
                error_message = f"Error creating order: {str(error)}"
            raise Exception(error_message)

        confetti_emoji = emoji.emojize(":party_popper:")
        print("\n-----------------------------")
        print(f"Order Submitted! {confetti_emoji}")
        print("-----------------------------")

        # Get order id from the response object
        order_uid = r_order.json()
        print(f"\nYour order uid is: {order_uid}")
        print(f"You can see your order on the Cow Explorer here: \nhttps://explorer.cow.fi/orders/{order_uid}")
        return order_uid
