
# the vault relayer contract needs approval to spend the sell tokens
def token_approve(proposal_data):
    """approve tokens to be spent by GP2 vault relayer"""
    sell_token_name = proposal_data["SELL TOKEN NAME"]
    sell_token_contract = proposal_data["SELL TOKEN CONTRACT"]
    amount = proposal_data["TOTAL WITH FEE"]
    cow_relayer = proposal_data["COW RELAYER"]

    # Get approval call data - requires web3 to be initialized in calling file
    approval = sell_token_contract.encodeABI(
        fn_name="approve", args=[cow_relayer, amount]
    )

    print("\nFirst call; approval to spend funds")
    print("--------------------------------------")
    print(f"Spending contract: {cow_relayer}")
    print(f'Token to be spent: {sell_token_name.upper()} ({sell_token_contract.address})')
    print(f"Amount approved to be spent: {amount}:")
    print(f"\nCalldata: \n{approval}")
    return approval

def cowswap_signature(proposal_data):
    """ create signature to be signed by DXdao governance"""
    vault_relayer_contract = proposal_data["COW SETTLEMENT CONTRACT"]
    order_id = proposal_data["ORDER ID"]
    # Get signature call data
    signature = vault_relayer_contract.encodeABI(fn_name="setPreSignature", args=[order_id, True])
    print("\nSecond call; sign order:")
    print("--------------------------------------")
    print(f"contract address: {vault_relayer_contract.address}")
    print(f"\ncalldata: \n{signature}")
    return signature
  
