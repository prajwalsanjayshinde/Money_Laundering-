
import drawGraph as dG

#edgeList = [(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(3,6),(4,5),(4,6),(5,6),(7,8),(8,9),(8,10),(9,10)]

#This File contains methods which deal with
#identifying various graphs from the given
#set of edge List

#Algorithm
    #Identify all the source Nodes of various graph(Source Nodes are nodes in the graph with indegree = 0)
        #sourceNodes = [1,7]
    #Apply BFS or DFS from the source Node and identify all the vertices belonging to that graph containing source Node
        #vertices = [1,2,3,4,5,6] (Graph 1)
        #vertices = [7,8,9,10] (Graph 2)
    #Split the Edge List based on the vertices obtained from various graph
        #edgeList1 = [ (1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(3,6),(4,5),(4,6),(5,6) ]
        #edgeList2 = [ (7,8),(8,9),(8,10),(9,10) ]

def depthFirstSearch(edgeList,graph,sourceNode):
    dfsStack = []
    exploredStack = [sourceNode]
    while exploredStack != []:
        visitedNode = exploredStack.pop()
        if visitedNode not in dfsStack:
            try:
                dfsStack.append(visitedNode)
            except:
                dfsStack = [visitedNode]
        if visitedNode in graph.keys():
                for val in graph[visitedNode]:
                    try:
                        exploredStack.append(val)
                    except:
                        exploredStack =[val]

    print("Vertices in Graph")
    dfsStack.sort()
    print(dfsStack)
    return dfsStack

def getSourceNodes(indegreeMap):
    print("Source Nodes")
    sourceNodes = []
    for k,v in indegreeMap.items():
        if v == 0:
            try:
                sourceNodes.append(k)
            except:
                sourceNodes = [k]
    print(sourceNodes)
    return sourceNodes

def getDestNodes(outdegreeMap):
    print("Destination Nodes")
    destNodes = []
    for k,v in outdegreeMap.items():
        if v == 0:
            try:
                destNodes.append(k)
            except:
                destNodes = [k]
    print(destNodes)
    return destNodes


def splitEdgeList(edgeList,graph,sourceNodes):
    newEdgeList = []
    for sourceNode in sourceNodes:
        vertexSet = depthFirstSearch(edgeList,graph,sourceNode)
        row = []
        for edge in edgeList:
            if edge[0] in vertexSet and edge[1] in vertexSet:
                try:
                    row.append(edge)
                except:
                    row = [edge]
        try:
            newEdgeList.append(row)
        except:
            newEdgeList =[row]
    print("New Edge Lists after splitting")
    i = 0
    for row in newEdgeList:
        print(row)
        dG.drawGraph(row,"Graph"+str(i)+".png")
        i += 1
    return newEdgeList



#splitEdgeList()
#indegreeMap  = {1: 0, 2: 1, 3: 2, 4: 2, 5: 2, 6: 3, 7: 0, 8: 1, 9: 1, 10: 2}
#getSourceNodes(indegreeMap)
