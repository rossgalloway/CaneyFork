from helpers.constants import GOV_MODULES

network = "MAINNET"
gov_module = GOV_MODULES["MULTICALL"][{network}]


class ProposalData:
    def __init__(self, network, gov_module, account, approval, signature, cid) -> None:
        self.network = network
        self.gov_module = gov_module
        self.account = ""
        self.approval = ""
        self.signature = ""
        self.cid = ""

proposal1 = ProposalData(network, gov_module,,,,)
print(proposal1)