import os
import json
import dotenv
import requests
from web3 import Web3, Account
from helpers.constants import AVATAR, DXD, COW_API, GOV_MODULES, TOKENS, COW_RELAYER 
from helpers.cowswap_submit_order import cowswap_submit_order
from helpers.calls import token_approve, cowswap_signature
from helpers.submit_proposal import submit_proposal

# Load .env
dotenv.load_dotenv()

class ProposalData:
    def __init__(self) -> None:
        pass

def pin_text(order_id, int_amount, sell_token):
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

if __name__ == "__main__":

    # Create new proposal object 
    NewProposal = {}
    print(f"\nCreating new BuyBack Proposal")

    # Get user input for network
    network = input("\n>>>Choose Network (MAINNET/GNOSIS): ")
    if network.upper() not in ["MAINNET", "GNOSIS"]:
        print("Invalid network")
        exit()
    network = network.upper()  # MAINNET || GNOSIS
    gov_module = GOV_MODULES["MULTICALL"][network]
    avatar = AVATAR[network]
    cow_api = COW_API[network]
    cow_relayer = COW_RELAYER[network]

    # add network and governance module to proposal object
    NewProposal["NETWORK"] = network
    NewProposal["GOV MODULE"] = gov_module
    NewProposal["AVATAR"] = avatar
    NewProposal["COW API"] = cow_api
    NewProposal["COW RELAYER"] = cow_relayer
    print(NewProposal)

    # Display available tokens for chosen network
    # TODO add quantities in the Avatar
    print(f"\nAvailable {network} Tokens:")
    for i, token in enumerate(TOKENS[network]):
        print(f"{token}")

    # Get user input for sell token
    sell_token_name = input("\n>>>Choose Sell token: ")
    if sell_token_name.upper() not in TOKENS[network]:
        print(">>>Invalid token! try again! 2 tries left...")
        sell_token_name = input(">>>Choose Sell token: ")
    if sell_token_name.upper() not in TOKENS[network]:
        print(">>>Invalid token! try again! 1 tries left...")
        sell_token_name = input(">>>Choose Sell token: ")
    if sell_token_name.upper() not in TOKENS[network]:
        print(">>>Invalid token! You lose, restart the program and work on your typography")
        exit() 
    sell_token_address = TOKENS[network][sell_token_name.upper()]

    ## TODO add decimals check
    # check how many decimals 
    decimal_check = input(f"\n>>>Is {sell_token_name.upper()} 18 decimals? (y/n): ")
    if decimal_check == "y":
        sell_decimals = 18
        print(f"decimals set to: {sell_decimals}")
    else:
        # input new decimal amount if not 18 
        sell_decimals = input(f">>>enter {sell_token_name.upper()} decimals: ")
        sell_decimals = int(sell_decimals)
        print(f"decimals set to: {sell_decimals}")
    buy_token_address = DXD[network]

    # Get user input for amount
    sell_amount = input("\n>>>Amount to sell: ")
    # add decimals to sell amount
    sell_amount_full_decimals = int(sell_amount) * int(10**int(sell_decimals))
    print(f"Amount to sell: {sell_amount} {sell_token_name.upper()} ({sell_amount_full_decimals})")
    exit()

    # create the Cowswap Order
    order_uid = cowswap_submit_order(
        sell_token_address, buy_token_address, str(sell_amount_full_decimals), network, avatar, COW_API[network])

    # Ask user if they want to submit the order to DXdao Governance
    submit = input("Submit order? (y/n): ")
    if submit == "y":
        # Connect to RPC based off network
        w3 = Web3(Web3.HTTPProvider(os.getenv(f"{network}_RPC")))
        erc20_abi = json.load(open(f"abis/{sell_token_address.lower()}.json"))
        sell_token_contract = w3.eth.contract(
            address=Web3.toChecksumAddress(sell_token_address), abi=erc20_abi)
        # Load cowswap ABI and create contract
        cow_relayer_abi = json.load(open("abis/cow.json"))
        cow_relayer_contract = w3.eth.contract(
            address=COW_RELAYER[network], abi=cow_relayer_abi
        )
        # get the data from the previously submitted order
        order_details = requests.get(COW_API[network] + "/orders/" + order_uid)
        cow_sell_amount = int(order_details.json()["sellAmount"]) + int(
            order_details.json()["feeAmount"]
        )
        cow_sell_amount_readable = int(cow_sell_amount / 10**sell_decimals)  
        # Load private key from env
        proposer_pk = os.environ["PRIVATE_KEY"]
        # Setup web3 account from private key
        proposer = Account.from_key(proposer_pk)
        approval = token_approve(cow_sell_amount)
        signature = cowswap_signature(order_uid)
        cid = pin_text(order_uid, cow_sell_amount_readable, sell_token_address)
        submit_proposal(network, gov_module, proposer, approval, signature, cid)
