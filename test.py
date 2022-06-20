
"""

->[]->[]->[]->[]->[]->


{
  swaps{
    token0{
      symbol
    }
    token1{
      symbol
    }
    pool{
      token0Price
      token1Price
    }
  }
}


"""



import graphlib
from os import path

from graphql.graphql import GetPools


paths = []

def calculateArb(priceArr):

    for i in range(0,len(paths)):
        price = 1
        v = paths[i][0]

        for j in range(1,len(paths[i])):
            u = paths[i][j]
            price = price * float(priceArr[u+"-"+v])
            v = u

        symbol = paths[i][0] +"-"+v
        #print(symbol,paths[i],v)
        if symbol in priceArr and len(paths[i]) > 2:
            price = price * float(priceArr[symbol])

            p = str(price) 
            p += " "*(18-len(p))
            
            print(p,"Path : ","->".join(paths[i])+"->"+paths[i][0])
        # else:
        #     print("Path : ","->".join(paths[i])+"->"+paths[i][0])

            #startingValue = 10**(len(str(price)))



def dfs(graph,visited,key,cnt,path):
    singlePath = tuple(path)
    paths.append(singlePath)
    #print(visited,key,cnt)
    # print("->".join(path))
    # if (len(set(path)) >= 3 and len(set(path))) == len(path) :
    #     singlePath = tuple(path)
    #     paths.append(singlePath)
    #     #print("->".join(path))
    # elif key in visited:
    #     print("YES -> visited check asset pair : ",key) #this condition will never happen its already handled
    #     return

    visited.add(key)

    for nxt in list(graph[key]):
        #print(graph[key])
        if nxt in visited:
            continue
        path.append(nxt)

        dfs(graph,visited,nxt,cnt-1,path)
        path.pop()


def setPools(k,graph,priceArray):

  for pool in k["data"]["pools"]:
    u = pool["token0"]["symbol"]
    v = pool["token1"]["symbol"]

    priceArray[u+"-"+v] = pool["token0Price"]
    priceArray[v+"-"+u] = pool["token1Price"]

    if u not in graph.keys():
        graph[u] = set()
    if v not in graph.keys():
        graph[v] = set()
    
    graph[u].add(v)
    graph[v].add(u)



def arb(s):

    graph = {}
    priceArray = {}
    setPools(s,graph,priceArray)
    
    for key in graph.keys():
        path = [key]
        visited = set()
        dfs(graph,visited,key,3,path)

    print(graph,len(graph.keys()))

    calculateArb(priceArray)
    



if __name__ == "__main__":
    
    print(arb(GetPools()))