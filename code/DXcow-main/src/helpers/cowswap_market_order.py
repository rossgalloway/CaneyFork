from time import time
import requests
from brownie import Wei

def cowswap_market_order(proposal_data):
    """function to submit a new order to the CowSwap API"""

    sell_token = proposal_data['SELL TOKEN ADDRESS']
    buy_token = proposal_data['BUY TOKEN ADDRESS']
    amount = proposal_data['ORDER SELL AMOUNT']
    network = proposal_data['NETWORK']
    avatar = proposal_data['AVATAR']
    cow_api = proposal_data['COW API']

    # get the fee + the buy amount after fee
    fee_and_quote = cow_api + "quote/"

    # set order parameters here
    get_params = {
        "sellToken": sell_token,
        "buyToken": buy_token,
        "receiver": avatar,
        "appData": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "partiallyFillable": False, # pylint: disable=E0602:undefined-variable 
        "from": avatar,
        "priceQuality": "optimal",
        "signingScheme": "presign",
        "onchainOrder": False,  # pylint: disable=E0602:undefined-variable 
        "kind": "sell",
        "sellAmountBeforeFee": amount,
    }

    # TODO this gets the current market price. We need the 70% of NAV price.
    # send the get_params object to cowSwap quote endpoint
    print(f"\nGetting quote from CowSwap on {network}...")
    r_quote = requests.post(fee_and_quote, json=get_params, timeout=10)
    assert r_quote.ok and r_quote.status_code == 200

    # create a new order_payload from the "quote" section of the response
    order_payload = r_quote.json()["quote"]
    print(f"\nquote response: {order_payload}")

    # Set 40 day deadline
    deadline = int(time()) + 60 * 60 * 24 * 40  # 40 days
    order_payload["validTo"] = deadline

    # TODO remove when 70% of NAV price is added.
    # Add 4% slippage - for time delay
    order_payload["buyAmount"] = str(
        int(Wei(order_payload["buyAmount"]) * 0.96))

    # Set Signing Scheme
    order_payload["signingScheme"] = "presign"

    # Set Signature
    order_payload["signature"] = "0x"

    # Set "From" to DXdao Avatar
    order_payload["from"] = avatar
    # assure fee amount is a string
    if network == "GNOSIS":
         order_payload["feeAmount"] = str(int(Wei(order_payload["feeAmount"])))

    # Submit order to the Cowswap "orders" endpoint
    orders_url = cow_api + "orders"
    r_order = requests.post(orders_url, json=order_payload, timeout=10)
    assert r_order.ok and r_order.status_code == 201

    # Get order id from the response object
    order_uid = r_order.json()
    print(f"Payload: {order_payload}")
    print(f"\nOrder uid: {order_uid}")
    return order_uid
