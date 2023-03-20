
# DXD avatar addresses on different chains
AVATAR = {
    "MAINNET": "0x519b70055af55a007110b4ff99b0ea33071c720a",
    "GNOSIS": "0xe716ec63c5673b3a4732d22909b38d779fa47c3f",
}

# DXD token addresses on different chains
DXD = {
    "MAINNET": "0xa1d65E8fB6e87b60FECCBc582F7f97804B725521",
    "GNOSIS": "0xb90D6bec20993Be5d72A5ab353343f7a0281f158",
}

# CowSwap api addresses on different chains
# https://api.cow.fi/docs/
COW_API = {
    "MAINNET": "https://api.cow.fi/mainnet/api/v1/",
    "GNOSIS": "https://api.cow.fi/xdai/api/v1/",
}

COW_RELAYER = {
    "MAINNET": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    "GNOSIS": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
}

# Multicall modules on different chains
GOV_MODULES = {
    "MULTICALL": {
        "MAINNET": "0x34c42c3ee81a03fd9ea773987b4a6ef62f3fc151",
        "GNOSIS": "0xaFE59DF878E23623A7a91d16001a66A4DD87e0c0",
    }
}


# Token Addresses on different chains
# TODO: set decimals. break tokens into separate objects with address and decimal keys.
TOKENS = {
    "MAINNET": {
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "DAI" : "0x6b175474e89094c44da98b954eedeac495271d0f",
        "LUSD": "0x5f98805a4e8be255a32880fdec7f6728c6568ba0",
        "SUSD": "0x57ab1ec28d129707052df4df418d58a2d46d5f51",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",

    },
    "GNOSIS": {
        "WETH" : "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
        "WXDAI": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
    },
}