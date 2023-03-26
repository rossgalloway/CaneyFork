def get_token_balance(query_address, erc20_contract_address, erc20_abi, w3):
    # creates a contract object for the ERC20 token we want to get a quantity of
    contract = w3.eth.contract(address=erc20_contract_address, abi=erc20_abi)
    # finds the balance of tokens that the address holds
    balance = contract.functions.balanceOf(query_address).call()
    decimals = contract.functions.decimals().call()
    return balance / (10 ** decimals)


def get_eth_balance(query_address, w3):
    balance = w3.eth.getBalance(query_address)
    return w3.fromWei(balance, 'ether')
