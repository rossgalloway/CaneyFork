from time import time
import json
import requests
import web3
from brownie import Wei

AVATAR = {
    "MAINNET": "0x519b70055af55a007110b4ff99b0ea33071c720a",
    "GNOSIS": "0xe716ec63c5673b3a4732d22909b38d779fa47c3f",
}

# https://api.cow.fi/docs/
nets = {
    "MAINNET": "https://api.cow.fi/mainnet/api/v1/",
    "GNOSIS": "https://api.cow.fi/xdai/api/v1/",
}


def cowswap_sell(sell_token, buy_token, amount, net):
    # get the fee + the buy amount after fee
    fee_and_quote = nets[net] + "quote/"

    get_params = {
        "sellToken": sell_token,
        "buyToken": buy_token,
        "receiver": AVATAR[net],
        "appData": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "partiallyFillable": False,
        "from": AVATAR[net],
        "priceQuality": "optimal",
        "signingScheme": "presign",
        "onchainOrder": False,
        "kind": "sell",
        "sellAmountBeforeFee": amount,
    }

    r = requests.post(fee_and_quote, json=get_params)
    assert r.ok and r.status_code == 200

    # Submit order
    order_payload = r.json()["quote"]

    # Set 30 day deadline
    deadline = int(time()) + 60 * 60 * 24 * 40  # 30 days
    order_payload["validTo"] = deadline

    # Add 20% slippage - for time delay
    order_payload["buyAmount"] = str(int(Wei(order_payload["buyAmount"]) * 0.88))

    order_payload["signingScheme"] = "presign"
    order_payload["signature"] = "0x"
    order_payload["from"] = AVATAR[net]
    if net == "GNOSIS":
        order_payload["feeAmount"] = str(int(Wei(order_payload["feeAmount"])))

    orders_url = nets[net] + "orders"
    r = requests.post(orders_url, json=order_payload)
    assert r.ok and r.status_code == 201
    order_uid = r.json()
    print(f"Payload: {order_payload}")
    print(f"Order uid: {order_uid}")


if __name__ == "__main__":
    net = "GNOSIS"  # MAINNET GNOSIS
    sell = "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1"
    buy = "0xb90D6bec20993Be5d72A5ab353343f7a0281f158"
    amount = 5000000000000000000

    cowswap_sell(sell, buy, str(amount), net)
