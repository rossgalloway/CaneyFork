from web3 import Web3

def token_approve(sell_token_contract, amount):
    approval = sell_token_contract.encodeABI(
        fn_name="approve", args=["0xC92E8bdf79f0507f65a392b0ab4667716BFE0110", amount]
    )
    print("\nFirst call, approval:")
    print('weth address:' + sell_token_contract.address)
    print('call data:' + approval)
    return approval

def cowswap_signature(vault_relayer_contract, order_id):
    signature = vault_relayer_contract.encodeABI(fn_name="setPreSignature", args=[order_id, True])
    print("\nSecond call, sign order:")
    print('contract address: ' + vault_relayer_contract.address)
    print('calldata:' + signature)
    return signature
  
