 # https://api.thegraph.com/subgraphs/name/adamazad/dxdao-dxd-redemption-ethereum
 
 {
 query 
 dxdcirculatingSupplySnapshots(
     block: { number: 16693284 }
      orderBy: id
      orderDirection: desc
      first: 1
      ) {
        id
        totalSupply
        circulatingSupply
        }
        treasuryBalancesSnapshots(
            block: { number: 16693284 }
            orderBy: blockNumber
            orderDirection: desc
            first: 1
            ) {
                blockNumber
                balances {
                    address
                    amount
                    token {
                        address: id
                        symbol
                        decimals
                        }
                        }
                        }
                        }

# https://api.thegraph.com/subgraphs/name/adamazad/dxdao-dxd-redemption-gnosis

query {
    dxdcirculatingSupplySnapshots(
        block: { number: 26629017 }
        orderBy: id
        orderDirection: desc
        first: 1
        ) {
            id
            totalSupply
            circulatingSupply
            }
            treasuryBalancesSnapshots(
                block: { number: 26629017 }
                orderBy: blockNumber
                orderDirection: desc
                first: 1
                ) {
                    blockNumber
                    balances {
                        address
                        amount
                        token {
                            address: id
                            symbol
                            decimals
                            }
                            }
                            }
                            }
        