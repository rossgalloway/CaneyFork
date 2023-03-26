import os
import json
from web3 import Web3
import dotenv
import emoji

# Load .env
dotenv.load_dotenv()

def submit_proposal(proposal_data, proposer_pk, w3):
    """function to submit a proposal to DXdao governance"""
    gov_module_name = proposal_data["GOV MODULE NAME"]
    gov_module_address = proposal_data["GOV MODULE ADDRESS"]
    proposer = proposal_data["PROPOSER"]
    approval = proposal_data["APPROVAL"]
    signature = proposal_data["SIGNATURE"]
    cid = proposal_data["CID"]
    cow = proposal_data["COW SETTLEMENT CONTRACT"]
    sell_token = proposal_data["SELL TOKEN CONTRACT"]
    # Connect to Multicall2 contract and submit proposal
    # Pylint: disable=W1514:unspecified-encoding
    multicall_abi = json.load(open("src/abis/multicall2.json"))  
    multicall_contract = w3.eth.contract(
        address=gov_module_address,
        abi=multicall_abi,
    )

    # Build transaction to propose calls
    tx = multicall_contract.functions.proposeCalls(
        [sell_token.address, cow.address],
        [approval, signature],
        [0, 0],
        cid,
    ).build_transaction(
        {
            "nonce": w3.eth.get_transaction_count(
                Web3.toChecksumAddress(proposer.address)
            ),
            "gas": 1000000,
        }
    )

    print("\nTransaction Created! Please review the details:")
    print("---------------------------------------------------")
    print(f"Governance Module being used: {gov_module_name} ({gov_module_address})")
    print(f"Proposer Address: {proposer.address}")
    print("---------------------------------------------------")

    submit = input("\n>>>Ready to Sign and Submit Transaction? (y/n): ")
    if submit.upper() == "Y":

        # Sign and submit transaction with private key
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=proposer_pk)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        confetti_emoji = emoji.emojize(":party_popper:")
        print("\n--------------------------")
        print(f"Transaction Sent! {confetti_emoji}")
        print("--------------------------")
        print(f"Transaction hex: {tx_hash.hex()}")
        print(
            f"view your transaction at: https://etherscan.io/tx/{tx_hash.hex()}")
        