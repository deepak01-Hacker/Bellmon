
from dataclasses import dataclass
from graphql.graphql import GetPools
from paths import GetAllPaths

"""


H2O->UST->SLP->WETH->H2O
arb_bps = (endingSize-startingSize / startingSize) * 10000

PLSD->HEX->USDC->PLSD
1 ->  57.1852 -> 2.0915 -> 1.00208 

WETH->SHI->USDT->WETH




-> pools object ()
-> unrealesitc number (ex : 10000_gt)
                                                                                             
80560719727.78055    Path :  USDC->WETH->META->USDC  Price_Path :  1->0.0008866069724954159->8142232616.107479->8056072.972778055
{'id': '0x9f68f80c210831a6b87ab9633e158fd99c326660', 'token0': {'symbol': 'META'}, 'token1': {'symbol': 'USDC'}, \
'token0Price': '1010.69499291038723770433950846131', 'token1Price': '0.0009894181795839414988949696655670498', 'mints': [{'timestamp': '1651395310'}]}

"""

def calculateArb(priceStor,paths,n):

    for i in range(0,len(paths)):
        startingSize = 1
        size = 1
        v = paths[i][0]
        
        pricePath = [str(size)]
        for j in range(1,len(paths[i])):
            u = paths[i][j]
            size = size * float(priceStor[u+"-"+v])
            v = u
            pricePath.append(str(size))

        symbol = paths[i][0] +"-"+v

        if symbol in priceStor and len(paths[i]) > 2 and len(paths[i]) < n:
            size= size * float(priceStor[symbol])
            pricePath.append(str(size))

            if size < 1:
                continue

            _arbBps = ((size-startingSize)/startingSize)*10000
            _arbBps = str(_arbBps) 
            _arbBps += " "*(20-len(_arbBps))
            
            print(_arbBps,"Path : ","->".join(paths[i])+"->"+paths[i][0]," Price_Path : ","->".join(pricePath))


if __name__ == "__main__":
    zip = GetPools() # all pools retrive from uniswap
    graph = zip[0]   # graph of assets
    priceStor = zip[1] # price of every asset in term of quote asset
    pathLength = 6

    paths = GetAllPaths(graph)

    calculateArb(priceStor,paths,pathLength)


    

