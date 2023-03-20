from time import time
import json
import requests
from web3 import Web3, Account
from brownie import Wei
import dotenv
import os


# Load .env
dotenv.load_dotenv()


def submit_proposal(network, gov_module, account, approval, signature, cid):
    w3 = Web3(Web3.HTTPProvider(os.getenv(f"{network}_RPC")))
    # Connect to Multicall2 contract and submit proposal
    multicall_abi = json.load(open("abis/multicall2.json"))
    multicall_contract = w3.eth.contract(
        address=gov_module[network],
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