from lib2to3.pgen2 import token
from web3 import Web3
import pyperclip
import json
import requests

w3 = Web3(Web3.HTTPProvider("https://rpc.gnosischain.com"))

# Load weth ABI and create contract
weth_abi = json.load(open("abis/weth.json"))
weth = w3.eth.contract(
    address="0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1", abi=weth_abi
)

# Load cowswap ABI and create contract
cow_abi = json.load(open("abis/cow.json"))
cow = w3.eth.contract(address="0x9008D19f58AAbD9eD0D60971565AA8510560ab41", abi=cow_abi)


def token_approve(amount):
    approval = weth.encodeABI(
        fn_name="approve", args=["0xC92E8bdf79f0507f65a392b0ab4667716BFE0110", amount]
    )
    print("\nFirst call, approval:")
    print('weth address:' + weth.address)
    print('call data:' + approval)


def cowswap_signature(order_id):
    signature = cow.encodeABI(fn_name="setPreSignature", args=[order_id, True])
    print("\nSecond call, sign order:")
    print('contract address: ' + cow.address)
    print('calldata:' + signature)
    
def copy_text(order_id, int_amount):
    text = f"""CowSwap Order {order_id[2:10]} WETH / DXD
    
This proposal places a {int_amount} WETH order on CowSwap for DXD. See order here: https://explorer.cow.fi/gc/orders/{order_id}

This order is placed as part of the DXD buyback program.

The order is placed at a discount on the price of DXD at the time of creating the order - this is due to the multicall requiring 5 days to pass. Nevertheless, CowSwap matches at the best available price. So the discount just allows some market movement - in case there is no fill for the price, the order will turn into a limit order.
    """
    pyperclip.copy(text)
    print(text)

if __name__ == "__main__":
    # Ask user for order ID
    order_id = input("Enter order ID: ")
    # Get order details
    order_details = requests.get("https://api.cow.fi/mainnet/api/v1/orders/" + order_id)
    amount = int(order_details.json()["sellAmount"]) + int(
        order_details.json()["feeAmount"]
    )
    int_amount = int(amount/10**18) # ASSUMED 18 DECIMALS
    token_approve(amount)
    cowswap_signature(order_id)
    copy_text(order_id, int_amount)    
