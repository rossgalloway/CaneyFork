
# DXD avatar addresses on different chains
AVATAR = {
    "MAINNET": "0x519b70055af55A007110B4Ff99b0eA33071c720a",
    "GNOSIS": "0xe716EC63C5673B3a4732D22909b38d779fa47c3F",
}

# DXD token addresses on different chains
DXD = {
    "MAINNET": "0xa1d65E8fB6e87b60FECCBc582F7f97804B725521",
    "GNOSIS": "0xb90D6bec20993Be5d72A5ab353343f7a0281f158",
}

# CowSwap api addresses on different chains
# https://api.cow.fi/docs/
COW_API = {
    "MAINNET": {
        "PROD": "https://api.cow.fi/mainnet/api/v1/",
        "STAGING": "https://barn.api.cow.fi/mainnet/api/v1/",
    },
    "GNOSIS": { 
        "PROD": "https://api.cow.fi/xdai/api/v1/",
        "STAGING": "https://barn.api.cow.fi/xdai/api/v1/",
    },
}

COW_RELAYER = {
    "MAINNET": "0xC92E8bdf79f0507f65a392b0ab4667716BFE0110",
    "GNOSIS": "0xC92E8bdf79f0507f65a392b0ab4667716BFE0110",
}

COW_SETTLEMENT = {
    "MAINNET": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    "GNOSIS": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    }

# Multicall modules on different chains
GOV_MODULES = {
    "MULTICALL": {
        "MAINNET": "0x34C42c3ee81A03FD9ea773987b4a6eF62f3fc151",
        "GNOSIS": "0xaFE59DF878E23623A7a91d16001a66A4DD87e0c0",
    },
    "OTHER_MODULE": {
        "MAINNET": "0x....",
        "GNOSIS": "0x....",
    }
}

# Token Addresses on different chains
TOKENS = {
    "MAINNET": {
        "WETH": {
            "ADDRESS": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "DECIMALS": 18,
        },
        "DAI" : {
            "ADDRESS": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "DECIMALS": 18,
        },
        "LUSD": {
            "ADDRESS": "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",
            "DECIMALS": 18,
        },
        "USDC": {
            "ADDRESS": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "DECIMALS": 6,
        },
    },
    "GNOSIS": {
        "WETH" : {
            "ADDRESS": "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
            "DECIMALS": 18,
        },
        "WXDAI": {
            "ADDRESS": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
            "DECIMALS": 18
        },
        "USDC": {
            "ADDRESS": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
            "DECIMALS": 6,
        },
    }
}
