import os
import json
import time
import dotenv
import requests
from web3 import Web3, Account
from helpers.constants import AVATAR, DXD, COW_API, GOV_MODULES, TOKENS, COW_RELAYER, COW_SETTLEMENT
from helpers.cowswap_liquidity_order import cowswap_liquidity_order
from helpers.calls import token_approve, cowswap_signature
from helpers.submit_proposal import submit_proposal
from helpers.proposal_text import generate_proposal_text, pin_proposal_text
from helpers.token_functions import get_token_balance

# Load .env
dotenv.load_dotenv()

if __name__ == "__main__":

    # set networks
    network = "MAINNET"
    cow_network = "PROD"
    # set network based variables for chosen network
    BUY_TOKEN_NAME = "DXD"
    GOV_MODULE = "MULTICALL"
    GOV_MODULE_ADDRESS = GOV_MODULES[GOV_MODULE][network]
    AVATAR = AVATAR[network]
    COW_API = COW_API[network][cow_network]
    COW_SETTLEMENT_ADDRESS = COW_SETTLEMENT[network]
    COW_RELAYER_ADDRESS = COW_RELAYER[network]
    BUY_TOKEN_ADDRESS = DXD[network]

    print("\n--------------------------------------------")
    print(f"Creating new BuyBack Proposal on {network}")
    print("--------------------------------------------")

    # Create new proposal object
    proposal_data = {}
    # initialize new web3 instance for chosen network
    w3 = Web3(Web3.HTTPProvider(os.getenv(f"{network}_RPC")))

    # add network based variables to proposal object
    proposal_data["NETWORK"] = network
    proposal_data["GOV MODULE ADDRESS"] = GOV_MODULE_ADDRESS
    proposal_data["GOV MODULE NAME"] = GOV_MODULE
    proposal_data["AVATAR"] = AVATAR
    proposal_data["COW API"] = COW_API
    proposal_data["COW SETTLEMENT"] = COW_SETTLEMENT_ADDRESS
    proposal_data["COW RELAYER"] = COW_RELAYER_ADDRESS
    proposal_data["BUY TOKEN NAME"] = BUY_TOKEN_NAME
    proposal_data["BUY TOKEN ADDRESS"] = BUY_TOKEN_ADDRESS

    # Display available tokens for chosen network
    print(f"\nAvailable tokens for buybacks on {network}:")
    # Get token amounts in treasury and print token choices
    erc20_abi = json.load(open('src/abis/ERC20.json'))
    for key, value in TOKENS[network].items():
        NAME = key
        TOKEN_ADDRESS = value["ADDRESS"]
        # print(f"name: {name}, token_address: {token_address}, avatar: {avatar_address}")
        balance = get_token_balance(AVATAR, TOKEN_ADDRESS, erc20_abi, w3)
        print(f"     {NAME}: {balance}")

    # Get user input for sell token
    sell_token_name = input("\n>>> Choose Sell token (type in name): ")
    if sell_token_name.upper() not in TOKENS[network]:
        print(">>>Invalid token! try again! 2 tries left...")
        sell_token_name = input(">>> Choose Sell token (type in name): ")
        if sell_token_name.upper() not in TOKENS[network]:
            print(">>>Invalid token! try again! 1 tries left...")
            sell_token_name = input(">>> Choose Sell token (type in name): ")
            if sell_token_name.upper() not in TOKENS[network]:
                print(">>> Invalid token! You lose, restart the program and work on your typography")
                exit()
    
    # get sell token address and decimals and write to proposal data object
    sell_token_address = TOKENS[network][sell_token_name.upper()]["ADDRESS"]
    sell_decimals = TOKENS[network][sell_token_name.upper()]["DECIMALS"]

    # load the sell token ABI and create a new contract instance for the sell token
    # Pylint: disable=W1514:unspecified-encoding
    sell_token_abi = json.load(open(f"src/abis/{sell_token_name.lower()}.json"))  
    sell_token_contract = w3.eth.contract(
        address=Web3.toChecksumAddress(sell_token_address), abi=sell_token_abi)

    # Get user input for sale price 
    buy_token_price = float(
        input(f"\n>>> input your desired {sell_token_name.upper()}/DXD price: "))
    formatted_buy_token_price = f"{buy_token_price:,}"
    sell_token_price = 1 / buy_token_price

    # add buy and sell token prices as well as sell token info to proposal object
    proposal_data["BUY TOKEN PRICE"] = buy_token_price
    proposal_data["SELL TOKEN PRICE"] = sell_token_price
    proposal_data["SELL TOKEN NAME"] = sell_token_name.upper()
    proposal_data["SELL TOKEN ADDRESS"] = sell_token_address
    proposal_data["SELL TOKEN CONTRACT"] = sell_token_contract
    proposal_data["SELL TOKEN DECIMALS"] = sell_decimals

    # Load cowswap ABI and create contract
    # Pylint: disable=W1514:unspecified-encoding
    cow_settlement_abi = json.load(open("src/abis/cow-settlement.json"))  
    cow_settlement_contract = w3.eth.contract(
        address=COW_SETTLEMENT_ADDRESS, abi=cow_settlement_abi)
    # add contract to proposal object
    proposal_data["COW SETTLEMENT CONTRACT"] = cow_settlement_contract

    # Get user input for number of tokens to sell
    sell_amount = float(
        input(f"\n>>> Input amount of {sell_token_name.upper()} to sell: "))
    sell_amount_full_decimals = int(sell_amount * 10**sell_decimals)
    formatted_sell_amount = f"{sell_amount:,}"
    # add sell amount to proposal object
    proposal_data["ORDER SELL AMOUNT"] = sell_amount_full_decimals

    print("\n")
    print("Order Details:")
    print(
        f"Selling: {formatted_sell_amount} {sell_token_name.upper()} for {BUY_TOKEN_NAME.upper()}")
    print(
        f"At a price of: {formatted_buy_token_price} {sell_token_name.upper()}/{BUY_TOKEN_NAME.upper()}")
    print(f"Sourced from: {AVATAR}")
    print("As a liquidity order on CowSwap.")

    # Ask user if they want to create a new CowSwap order
    submit = input("\n>>> Do you want to create a new CowSwap order? (y/n): ")
    if submit.upper() == "Y":

        # create the Cowswap Order
        order_uid = cowswap_liquidity_order(proposal_data)
        # add order_uid amount to proposal object
        proposal_data["ORDER ID"] = order_uid

        # get the data from the just submitted order
        order_details = requests.get(
            COW_API + "/orders/" + order_uid, timeout=10)
        # get total amount including fee
        total_sell_amount = int(order_details.json()["sellAmount"]) + int(
            order_details.json()["feeAmount"]
        )
        total_sell_amount_readable = total_sell_amount / 10**sell_decimals
        # change back to total_sell_amount after testing
        proposal_data["TOTAL WITH FEE"] = total_sell_amount

        # Ask user if they want to submit the order to DXdao Governance
        submit = input(
            "\n>>> Do you want to submit a DXdao proposal to sign the order? (y/n): ")
        if submit.upper() == "Y":

            # Load private key from env
            proposer_pk = os.environ["PRIVATE_KEY"]
            assert proposer_pk is not None, "You must set PRIVATE_KEY environment variable"
            assert proposer_pk.startswith(
                "0x"), "Private key must start with 0x hex prefix"
            # Setup web3 account from private key
            # pylint: disable=E1120:no-value-for-parameter
            proposer = Account.from_key(proposer_pk)
            proposal_data["PROPOSER"] = proposer
            # Get call data to approve relayer to spend sell token
            print("\n")
            print("Getting call data...")
            time.sleep(1)
            approval = token_approve(proposal_data)
            proposal_data["APPROVAL"] = approval
            time.sleep(1)
            # Get call data to sign cowswap order
            signature = cowswap_signature(proposal_data)
            proposal_data["SIGNATURE"] = signature
            # generate proposal text and pin to pinata
            print("\n")
            print("Generating proposal and pinning it...")
            time.sleep(1)
            proposal_text = generate_proposal_text(proposal_data)
            cid = pin_proposal_text(proposal_text)
            proposal_data["CID"] = cid
            # submit proposal to DXdao governance
            print("\n")
            print("Creating new transaction...")
            time.sleep(1)
            submit_proposal(proposal_data, proposer_pk, w3)
