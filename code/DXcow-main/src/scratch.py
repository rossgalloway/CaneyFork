import os
import dotenv
from web3 import Web3, Account

dotenv.load_dotenv()

proposer_pk = os.environ["PRIVATE_KEY"]
print(proposer_pk)
assert proposer_pk is not None, "You must set PRIVATE_KEY environment variable"
assert proposer_pk.startswith(
     "0x"), "Private key must start with 0x hex prefix"
 # Setup web3 account from private key
proposer = Account.from_key(proposer_pk) # pylint: disable=E1120:no-value-for-parameter
print(proposer.address)