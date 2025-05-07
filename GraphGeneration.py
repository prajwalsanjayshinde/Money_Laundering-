
def generateGraph(tupleList):
    """
    Description : Generates a graph from the edgeList containing edges
                  in the form of tuple.
    input : [(7, 8), (8, 9), (8, 10), (9, 10)]
    output : {7: [8], 8: [9, 10], 9: [10]}
    7 has an edge to vertex 8, 8 has an edge to vertex 9 and 10, 9 has an edge to vertex 10
    """
    print("Generate Graph")
    graph = {}
    for tuple in tupleList:
        if tuple[0] not in graph.keys():
            graph[tuple[0]] = [tuple[1]]
        else:
            graph[tuple[0]].append(tuple[1])
    print(graph)
    return graph

def getVertices(tupleList):
    """
    Description : gets the vertices of the graph from the edgeList
    input : [(7, 8), (8, 9), (8, 10), (9, 10)]
    output: [7,8,9,10]
    """
    print("Get Vertices of a Graph")
    vertices = []
    for tuple in tupleList:
        if tuple[0] not in vertices:
            try:
                vertices.append(tuple[0])
            except:
                vertices = [tuple[0]]
        if tuple[1] not in vertices:
                vertices.append(tuple[1])
    vertices.sort()
    print(vertices)
    return vertices

def getIndegree(vertices,graph):
    """
    Desciption : gets the indegree Map of the vertices of the graph
    input : [7,8,9,10],{7: [8], 8: [9, 10], 9: [10]}
    output : {7 : 0, 8 : 1, 9 : 1, 10 : 2}
    """
    print("Get Indegree of all vertices")
    indegreeMap = {}
    for node in vertices:
        count = 0
        for keys in graph.keys():
            if node in graph[keys]:
                count += 1
        indegreeMap[node] = count
    print(indegreeMap)
    return indegreeMap

def getOutDegree(vertices,graph):
    """
        Desciption : gets the outdegree Map of the vertices of the graph
        input : [7,8,9,10],{7: [8], 8: [9, 10], 9: [10]}
        output : {7 : 1, 8 : 2, 9 : 1, 10 : 0}
    """
    print("Get OutDegree of all vertices")
    outDegreeMap = {}
    for node in vertices:
        if node in graph.keys():
            outDegreeMap[node] = len(graph[node])
        else:
            outDegreeMap[node] = 0
    print(outDegreeMap)
    return outDegreeMap


def genNodeValues(vertices,sourceNode):
    """
        Desciption : generates Node Values for the vertices of the graph
                     sourceNode with a indegree of zero has a value of 0
                     and remaining nodes have a value of -1000
        input : [7,8,9,10],7
        output : {7 : 0, 8 : -1000, 9 : -1000, 10 : -1000}
    """
    nodeValues = {}
    for vertex in vertices:
        if vertex == sourceNode:
            nodeValues[vertex] = 0
        else:
            nodeValues[vertex] = -1000
    print(nodeValues)
    return nodeValues
