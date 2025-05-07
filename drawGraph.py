import networkx as nx
import matplotlib.pyplot as plt


def drawGraph(edgeList, imageFileName):
    G = nx.Graph()
    # adding a list of edges:
    G.add_edges_from(edgeList)

    print("Nodes of graph: ")
    print(G.nodes())
    print("Edges of graph: ")
    print(G.edges())

    plt.figure()
    plt.ion()
    plt.show()  # display
    nx.draw_networkx(G)
    plt.savefig(imageFileName)  # save as png
    plt.draw()
    plt.pause(0.001)
