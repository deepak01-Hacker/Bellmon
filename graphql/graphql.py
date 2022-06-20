from unittest import skip
import requests
from datetime import datetime,timedelta
import json

url = " https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

def getQuery(skip):

  return """{
  pools(first:1000,skip:%s,where:{volumeUSD_gt:30000}){
    id
    token0{
      symbol
    }
    token1{
      symbol
    }
    token0Price
    token1Price
    mints{
      timestamp
    }
  }
}"""%(skip)


def RunQuery(query):
    
    r = requests.post(url, json = {"query": query})#"{\n  pairs(first: 10, where: {reserveUSD_gt: \"1000000\", volumeUSD_gt: \"50000\"}, orderBy: reserveUSD, orderDirection: desc) {\n    id\n    token0 {\n      id\n      symbol\n    }\n    token1 {\n      id\n      symbol\n    }\n    reserveUSD\n    volumeUSD\n  }\n}\n","variables":None}) 
    #print(r.text,r.status_code)
    json_data = json.loads(r.text)
    return json_data

def setPools(update,graph,priceArray):
  now = datetime.now()-timedelta(days=60) #

  for pool in update["data"]["pools"]:

    lastPositionTime = datetime.fromtimestamp(int(pool["mints"][-1]["timestamp"]))

    u = pool["token0"]["symbol"]
    v = pool["token1"]["symbol"]

    if lastPositionTime < now:
      #print(pool)
      continue

    # if u == "META" or v == "META":
    #   print(pool)

    priceArray[u+"-"+v] = pool["token0Price"]
    priceArray[v+"-"+u] = pool["token1Price"]

    if u not in graph.keys():
        graph[u] = set()
    if v not in graph.keys():
        graph[v] = set()
    
    graph[u].add(v)
    graph[v].add(u)



def GetPools():

    graph = {}
    priceStor = {}
    setPools(RunQuery(getQuery(0)),graph,priceStor)
    setPools(RunQuery(getQuery(1000)),graph,priceStor)
    # setPools(RunQuery(getQuery(2000)),graph,priceStor)
    # setPools(RunQuery(getQuery(3000)),graph,priceStor)
    # setPools(RunQuery(getQuery(4000)),graph,priceStor)
    # setPools(RunQuery(getQuery(5000)),graph,priceStor)

    return [graph,priceStor]
