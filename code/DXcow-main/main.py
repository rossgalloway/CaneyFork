from time import time
import json
import requests
from web3 import Web3, Account
from brownie import Wei
import dotenv
import os

# Load .env
dotenv.load_dotenv()

# DXD avatar addresses on different chains
AVATAR = {
    "MAINNET": "0x519b70055af55a007110b4ff99b0ea33071c720a",
    "GNOSIS": "0xe716ec63c5673b3a4732d22909b38d779fa47c3f",
}

# DXD token addresses on different chains
DXD = {
    "MAINNET": "0xa1d65E8fB6e87b60FECCBc582F7f97804B725521",
    "GNOSIS": "0xb90D6bec20993Be5d72A5ab353343f7a0281f158",
}

# CowSwap api addresses on different chains
# https://api.cow.fi/docs/
COW_API = {
    "MAINNET": "https://api.cow.fi/mainnet/api/v1/",
    "GNOSIS": "https://api.cow.fi/xdai/api/v1/",
}

# Multicall modules on different chains
MULTICALL = {
    "MAINNET": "0x34c42c3ee81a03fd9ea773987b4a6ef62f3fc151",
    "GNOSIS": "0xaFE59DF878E23623A7a91d16001a66A4DD87e0c0",
}

# Token Addresses on different chains
# TODO: set decimals. break tokens into separate objects with address and decimal keys.
tokens = {
    "MAINNET": {
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "DAI" : "0x6b175474e89094c44da98b954eedeac495271d0f",
        "LUSD": "0x5f98805a4e8be255a32880fdec7f6728c6568ba0",
        "SUSD": "0x57ab1ec28d129707052df4df418d58a2d46d5f51",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",

    },
    "GNOSIS": {
        "WETH" : "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
        "WXDAI": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
    },
}


def cowswap_sell(sell_token, buy_token, amount, network):
    # get the fee + the buy amount after fee
    fee_and_quote = COW_API[network] + "quote/"

    get_params = {
        "sellToken": sell_token,
        "buyToken": buy_token,
        "receiver": AVATAR[network],
        "appData": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "partiallyFillable": False,
        "from": AVATAR[network],
        "priceQuality": "optimal",
        "signingScheme": "presign",
        "onchainOrder": False,
        "kind": "sell",
        "sellAmountBeforeFee": amount,
    }

    # send the get_params object to cowSwap quote endpoint
    r = requests.post(fee_and_quote, json=get_params)
    assert r.ok and r.status_code == 200

    # create a new order_payload from the "quote" section of the response 
    order_payload = r.json()["quote"]

    # Set 40 day deadline
    deadline = int(time()) + 60 * 60 * 24 * 40  # 40 days
    order_payload["validTo"] = deadline

    # Add 4% slippage - for time delay
    order_payload["buyAmount"] = str(
        int(Wei(order_payload["buyAmount"]) * 0.96))
    # Set Signing Scheme
    order_payload["signingScheme"] = "presign"
    # Set Signature
    order_payload["signature"] = "0x"
    # Set "From" to DXdao Avatar with chain as an option
    order_payload["from"] = AVATAR[network]
    if network == "GNOSIS":
        order_payload["feeAmount"] = str(int(Wei(order_payload["feeAmount"])))

    # Submit order to the Cowswap "orders" endpoint
    orders_url = COW_API[network] + "orders"
    r = requests.post(orders_url, json=order_payload)
    assert r.ok and r.status_code == 201
    # Get order id from the response object
    order_uid = r.json()
    print(f"Payload: {order_payload}")
    print(f"Order uid: {order_uid}")
    return order_uid


def token_approve(amount):
    approval = erc20.encodeABI(
        fn_name="approve", args=["0xC92E8bdf79f0507f65a392b0ab4667716BFE0110", amount]
    )
    print("\nFirst call, approval:")
    print(erc20.address)
    print(approval)
    return approval


def cowswap_signature(order_id):
    signature = cow.encodeABI(fn_name="setPreSignature", args=[order_id, True])
    print("\nSecond call, sign order:")
    print(cow.address)
    print(signature)
    return signature


def pin_text(order_id, int_amount):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    payload = json.dumps(
        {
            "pinataOptions": {"cidVersion": 0},
            "pinataContent": {
                "description": f"""This proposal places a {int_amount} {sell_token} order on 
                CowSwap for DXD. See order here: https://explorer.cow.fi/orders/{order_id}

                This order is placed as part of the [DXD buyback program]
                (https://dxvote.eth.limo/#/mainnet/proposal/0x072519e7fa7d55619fcc675c5c47e446e499ee454da1f2b370825ac447d06758).

                The order is placed at a discount on the price of DXD at the time of creating the order - 
                this is due to the time required for a multicall proposal to pass. Nevertheless, CowSwap matches at the best available price. 
                So the discount just allows some market movement - in case there is no fill for the price, the order will turn into a limit order.
                """,
                "title": f"""CowSwap Order {order_id[2:10]} {sell_token} / DXD""",
                "tags": ["cowswap", "buyback"],
                "url": "",
            },
        }
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("PINATA_JWT"),
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    cid = response.json()["IpfsHash"]
    return cid


def submit_proposal():
    # Connect to Multicall2 contract and submit proposal
    multicall_abi = json.load(open("abis/multicall2.json"))
    multicall_contract = w3.eth.contract(
        address=MULTICALL[network],
        abi=multicall_abi,
    )

    # Build transaction to propose calls
    tx = multicall_contract.functions.proposeCalls(
        [erc20.address, cow.address],
        [approval, signature],
        [0, 0],
        cid,
    ).build_transaction(
        {
            "nonce": w3.eth.get_transaction_count(
                Web3.toChecksumAddress(account.address)
            ),
            "gas": 1000000,
        }
    )

    # Sign and submit transaction with private key
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(tx_hash.hex())


if __name__ == "__main__":
    # Get user input for network
    network = input("Network (MAINNET/GNOSIS): ")
    if network.upper() not in ["MAINNET", "GNOSIS"]:
        print("Invalid network")
        exit()
    network = network.upper()  # MAINNET GNOSIS
    # Print tokens for network
    print("Tokens:")
    for i, token in enumerate(tokens[network]):
        print(f"{token}")
    # Get user input for sell token
    sell_token = input("Sell token: ")
    if sell_token.upper() not in tokens[network]:
        print("Invalid token")
        exit()
    sell = tokens[network][sell_token.upper()]
    # check how many decimals 
    decimal_check = input(f"is {sell_token.upper()} 18 decimals? (y/n): ")
    if decimal_check == "y":
        sell_decimals = 18
    else:
        # input new decimal amount if not 18 
        sell_decimals = input(f"enter {sell_token.upper()} decimals: ")
        sell_decimals = int(sell_decimals)
        print(f"decimals set to: {sell_decimals}")
    buy = DXD[network]
    # Get user input for amount
    amount = input("Amount: ")
    # turn amount into wei
    amount = Web3.toWei(amount, "ether")
    print(amount)
    # create the Cowswap Order
    order_uid = cowswap_sell(sell, buy, str(amount), network)

    # Ask user if they want to submit the order to DXdao Governance
    submit = input("Submit order? (y/n): ")
    if submit == "y":
        # Connect to RPC based off network
        w3 = Web3(Web3.HTTPProvider(os.getenv(f"{network}_RPC")))
        erc20_abi = json.load(open(f"abis/{sell.lower()}.json"))
        erc20 = w3.eth.contract(
            address=Web3.toChecksumAddress(sell), abi=erc20_abi)
        # Load cowswap ABI and create contract
        cow_abi = json.load(open("abis/cow.json"))
        cow = w3.eth.contract(
            address="0x9008D19f58AAbD9eD0D60971565AA8510560ab41", abi=cow_abi
        )
        # get the data from the previously submitted order
        order_details = requests.get(COW_API[network] + "/orders/" + order_uid)
        amount = int(order_details.json()["sellAmount"]) + int(
            order_details.json()["feeAmount"]
        )
        int_amount = int(amount / 10**sell_decimals)  
        # Load private key from env
        private_key = os.environ["PRIVATE_KEY"]
        # Setup web3 account from private key
        account = Account.from_key(private_key)
        approval = token_approve(amount)
        signature = cowswap_signature(order_uid)
        cid = pin_text(order_uid, int_amount)
        submit_proposal()
