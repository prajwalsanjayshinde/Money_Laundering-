# Python program to print topological sorting of a DAG
from collections import defaultdict
import GraphGeneration as gg
import FrequentTransactions as ft
import DisconnectedGraphs as dg
import pymongo

# Class to represent a graph
class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)  # dictionary containing adjacency List
        self.V = vertices  # No. of vertices

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # A recursive function used by topologicalSort
    def topologicalSortUtil(self, v, visited, stack):

        # Mark the current node as visited.
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)

        # Push current vertex to stack which stores result
        stack.insert(0, v)

    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        print("Topological Sort")
        visited = [False] * self.V
        stack = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)

        # Print contents of stack
        print(stack)
        return stack

def initializeGraph(edgeList):
    """
        Initializes th graph
        Input : Number of Edges
                Edges in the form of tuple
        Output: returns graph object
    """
    g = Graph(len(edgeList))
    for edges in edgeList:
        g.addEdge(edges[0],edges[1])
    print(g.graph)
    return g

def mapTopologicalStack(g):
    """
        Maps the vertices/nodes of the topologically sorted graph
        Input : vertices of the graph (3,2,1,0)
        Output : returns map of nodes (3:0,2:1,1:2,0:3)
    """
    print("Mapping Nodes")
    mapOfNodes = {}
    count = 0
    for k,v in g.graph.items():
        mapOfNodes[k] = count
        count += 1
    print(mapOfNodes)
    return mapOfNodes

def genEdgeWeights(g):
    """
            Initializes the edge weights of the graph to one
            Input : [1:[2,3], 2:[3,4], 3:[4,5,6], 4: [5,6], 5:[6]]
                    Here key is the vertex of the graph
                    and Value is a list of vertices to which the key vertex is connected,
                    forming an edge.
            Output : [{2: 1, 3: 1}, {3: 1, 4: 1}, {4: 1, 5: 1, 6: 1}, {5: 1, 6: 1}, {6: 1}]
    """
    print("Assigning Edge Weights  ")
    edgeWeights = []
    for k,v in  g.graph.items():
        if v != []:
            edgeWeight = {}
            for vertices in v:
                edgeWeight[vertices] = 1
            try:
                edgeWeights.append(edgeWeight)
            except:
                edgeWeights = [edgeWeight]
    print(edgeWeights)
    return edgeWeights

def longestDistance(nodeValues,mapOfNodes,g):
    """
    Description : Finds the Longest Distance between source Nodes and other Nodes in the graph
          Input : nodeValues = {1:0,2:-1000,3:-1000,4:-1000,5:-1000,6:-1000}
                  g = [1:[2,3], 2:[3,4], 3:[4,5,6], 4: [5,6], 5:[6]]
                  edgeWeights = [{2: 1, 3: 1}, {3: 1, 4: 1}, {4: 1, 5: 1, 6: 1}, {5: 1, 6: 1}, {6: 1}]
         Output : nodeValues = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}}
    """
    longestPathEdges = {}
    edgeWeights = genEdgeWeights(g)
    print(edgeWeights)

    print("Longest Distance Function : ")
    #print("len ",len(nodeValues.keys()))
    for node in nodeValues.keys():
        try:
            #print(edgeWeights[mapOfNodes[node]])
            print(node,edgeWeights[mapOfNodes[node]].keys())

            for key in edgeWeights[mapOfNodes[node]].keys():
                nodeVal = nodeValues[node] #0
                edgeWt = edgeWeights[mapOfNodes[node]][key] #eW[4][2] = 1
                newNodeVal = nodeVal + edgeWt #1
                if nodeValues[key] < newNodeVal:
                    nodeValues[key] = newNodeVal
                    try:
                        longestPathEdges[key].append(node,key)
                    except:
                        longestPathEdges[key] = [node,key]
        except:
            print("Exception!!!")
    print(nodeValues)
    print(longestPathEdges)
    return longestPathEdges

def getlongestPath(longestPathEdges,destNode,sourceNode):

    longestPath = [longestPathEdges[destNode]]
    prevNode = longestPathEdges[destNode][0]
    while prevNode != sourceNode:
        longestPath.append(longestPathEdges[prevNode])
        prevNode = longestPathEdges[prevNode][0]

    print(longestPath)
    return longestPath

def getTransactionInformation(longestPath):
    transactionList = []
    client = pymongo.MongoClient()
    db = client.MoneyLaundering
    mappedTransactions = db.mappedTransactions
    print("Transactions involved in longest Path : \n")
    for path in longestPath:
        transactionInfo  = {}
        orig = mappedTransactions.find({'tupleId' : path[0]}, {'customerId': 1,'_id': 0})
        dest = mappedTransactions.find({'tupleId' : path[1]}, {'customerId': 1,'_id': 0})

        transactionInfo["nameOrig"] = orig[0]['customerId']
        transactionInfo["nameDest"] = dest[0]['customerId']

        transactInfo = db.bankingTransactions.find({'nameOrig' : orig[0]['customerId'],'nameDest' : dest[0]['customerId']})

        for info in transactInfo:
            for k,v in info.items():
                transactionInfo[k] = v
        try:
            transactionList.append(transactionInfo)
        except:
            transactionList = [transactionInfo]
    return transactionList

def getCustomerId(node):
    client = pymongo.MongoClient()
    db = client.MoneyLaundering
    customer = db.mappedTransactions.find({'tupleId' : node},{'customerId':1,'_id':0})
    customerId = None
    for info in customer:
        for k,v in info.items():
            print(v)
            customerId = v
    return customerId

def get_edge_list():
    
    tupleList = [tuple(el) for el in ft.get_tuple_list()[0]["tupleList"]]
    print("Total Number of Transactions : ", len(tupleList))

    print("Actual Frequency of Transactions : ")
    actualTransFreq = ft.actualCount(tupleList)

    print("Hash Based Bucket Count : ")
    bucketContainer = ft.hashBasedBucketCount(tupleList)

    print("Filtered transactions(On Basis of Bucket Count) : ")
    filteredBucketTuples = ft.filterOnBucketCount(tupleList, bucketContainer, 2)

    print("Filtered Transactions(On Basis of actual Frequency) : ")
    actualCount = ft.filterOnActualCount(filteredBucketTuples, actualTransFreq, 0)
    print(actualCount)
    
    edgeList=  [edge for edge in tupleList if edge in actualCount.keys()]
    print("Edge List:{}".format(edgeList))
    return edgeList


def compute_graph_analysis():
    # Get the edge list
    edgeList = get_edge_list()

    # Initialize the graph with the edge list
    g = initializeGraph(edgeList)
    graph = gg.generateGraph(edgeList)
    vertices = gg.getVertices(edgeList)
    indegreeMap = gg.getIndegree(vertices,graph)
    outdegreeMap = gg.getOutDegree(vertices,graph)
    
    # rest of the function remains unchanged...


    #Getting the sourceNodes
    sourceNodes = dg.getSourceNodes(indegreeMap)
    newEdgeList = dg.splitEdgeList(edgeList,graph,sourceNodes)

    print("Vertex Set after splitting")
    vertexSet = []
    count = 0
    for edgeList in newEdgeList:
        try:
            vertexSet.append(dg.depthFirstSearch(edgeList,graph,sourceNodes[count]))
        except:
            vertexSet = [dg.depthFirstSearch(edgeList,graph,sourceNodes[count])]
        count += 1

    print("New Node Values after splitting")
    newNodeValues = []
    count = 0
    for vertices in vertexSet:
        try:
            newNodeValues.append(gg.genNodeValues(vertices,sourceNodes[count]))
        except:
            newNodeValues = [gg.genNodeValues(vertices,sourceNodes[count])]
        count += 1

    count = 0
    for edgeList in newEdgeList:
        getTransactionInformation(edgeList)
        g = initializeGraph(edgeList)
        g.topologicalSort()
        mapOfNodes = mapTopologicalStack(g)
        longestDistance(newNodeValues[count],mapOfNodes,g)
        count += 1

    print("Longest Path for dest = %d and source = %d" %(10,7))
    longestPath = getlongestPath({8: [7, 8], 9: [8, 9], 10: [9, 10]},10,7)
    getTransactionInformation(longestPath)

    print("Longest Path for dest = %d and source = %d" % (6, 1))
    longestPath  = getlongestPath({2: [1, 2], 3: [2, 3], 4: [3, 4], 5: [4, 5], 6: [5, 6]}, 6, 1)
    getTransactionInformation(longestPath)

if __name__ == "__main__":
    compute_graph_analysis()