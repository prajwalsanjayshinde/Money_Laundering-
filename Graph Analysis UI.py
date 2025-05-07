from tkinter import *
import GraphAnalysis as ga
from GeneratePdf import generatePdf

def getGraphAnalysisResults():
    edgeList = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6), (7, 8), (8, 9), (8, 10),
                (9, 10),(11,12),(11,13),(12,14),(13,14)]
    g = ga.initializeGraph(edgeList)
    graph = ga.gg.generateGraph(edgeList)
    vertices = ga.gg.getVertices(edgeList)
    indegreeMap = ga.gg.getIndegree(vertices, graph)
    outdegreeMap = ga.gg.getOutDegree(vertices, graph)

    #inserting sourceNodes into the list
    print("Source Nodes ID from Mapped transactions : ")
    sourceNodes = ga.dg.getSourceNodes(indegreeMap)
    for sn in sourceNodes :
        customer = ga.getCustomerId(sn)
        list2.insert(END,str(customer) + "\n")

    #Inserting destNodes into the list
    print("Destination Nodes ID from Mapped transactions : ")
    destNodes = ga.dg.getDestNodes(outdegreeMap)
    for dn in destNodes:
        customer = ga.getCustomerId(dn)
        list3.insert(END, str(customer) + "\n")


    newEdgeList = ga.dg.splitEdgeList(edgeList, graph, sourceNodes)

    print("Vertex Set after splitting")
    vertexSet = []
    count = 0
    for edgeList in newEdgeList:
        try:
            vertexSet.append(ga.dg.depthFirstSearch(edgeList, graph, sourceNodes[count]))
        except:
            vertexSet = [ga.dg.depthFirstSearch(edgeList, graph, sourceNodes[count])]
        count += 1

    print("New Node Values after splitting")
    newNodeValues = []
    count = 0
    for vertices in vertexSet:
        try:
            newNodeValues.append(ga.gg.genNodeValues(vertices, sourceNodes[count]))
        except:
            newNodeValues = [ga.gg.genNodeValues(vertices, sourceNodes[count])]
        count += 1

    count = 0

    for edgeList in newEdgeList:
        #list to store pdf info
        data1 = [["Mapping of Nodes",""],["Node","CustomerId"]]
        data2 = [["Edges involved in transactions","","","","",""],["nameOrig","nameDest","type","amt","newBalOrig","newBalDest"]]
        data3 = [["SourceNode","DestinationNode"]]
        data4 = [["Edges involved in Longest Path"],["nameOrig","nameDest","type","amt","newBalOrig","newBalDest"]]
        data5 = []

        sub_data1 = []
        for vertex in vertexSet[count]:
               print("Vertex : "+ str(vertex))
               sub_data1 = [str(vertex)]
               sub_data1.append(str(ga.getCustomerId(vertex)))
               print(sub_data1)
               data1.append(sub_data1)
        print(data1)

        transactInfo = ga.getTransactionInformation(edgeList)
        for transactions in transactInfo:
            sub_data2 = []
            for k,v in transactions.items():
                list1.insert(END, str(k) + " "  + str(v))
                try:
                    sub_data2.append(str(v))
                except:
                    sub_data2 = [str(v)]
            list1.insert(END,"\n")
            data2.append(sub_data2)

        g = ga.initializeGraph(edgeList)
        g.topologicalSort()
        mapOfNodes = ga.mapTopologicalStack(g)
        longestPathInfo = ga.longestDistance(newNodeValues[count], mapOfNodes, g)

        print("Longest Path for dest = %d and source = %d" % (destNodes[count],sourceNodes[count]))

        agentIntegrator = [ga.getCustomerId(sourceNodes[count]),ga.getCustomerId(destNodes[count])]
        data3.append(agentIntegrator)

        longestPath = ga.getlongestPath(longestPathInfo,destNodes[count],sourceNodes[count])
        #For Calculating the total amount involved in transactions
        total_amount = 0
        sub_data5 = ["Total Transaction Amount"]    
        for items in ga.getTransactionInformation(longestPath):
            sub_data4 = []
            for k,v in items.items():
                list4.insert(END,str(k) + " " + str(v))
                try:
                    sub_data4.append(str(v))
                except:
                    sub_data4 = [str(v)]
                if k == "amount" and (v != None or v != 0):
                    total_amount += v

            list4.insert(END,"\n")
            data4.append(sub_data4)
        sub_data5.append(str(total_amount))
        data5.append(sub_data5)

        print("Total_amount : " + str(total_amount))


        generatePdf("Graph" + str(count) + ".png",data1,data2,data3,data4,data5,"Graph" + str(count) + ".pdf")
        count += 1


window = Tk()
window.geometry("600x1000")

l4 = Label(window,text = "Graphs : ")
l4.grid(row = 0, column = 0,columnspan = 2,pady = 5,padx = 20)
list1 = Listbox(window,width = 40,height = 10)
list1.grid(row = 0,column = 2,columnspan=2,pady = 5,padx = 20)
sb1 = Scrollbar(window)
sb1.grid(row = 0,column = 4, rowspan = 5,pady = 5)

l5 = Label(window,text = "Agents : ")
l5.grid(row = 1, column = 0,columnspan = 2,pady = 5,padx = 20)
list2 = Listbox(window,width = 40,height = 5)
list2.grid(row = 1,column = 2,columnspan=2,pady = 5,padx = 20)

l6 = Label(window,text = "Integrators : ")
l6.grid(row = 2, column = 0,columnspan = 2,pady = 5,padx = 20)
list3 = Listbox(window,width = 40,height = 5)
list3.grid(row = 2,column = 2,columnspan=2,pady = 5,padx = 20)

l7 = Label(window,text = "Graph Analysis Result : ")
l7.grid(row = 3, column = 0,columnspan = 2,pady = 5,padx = 20)
list4 = Listbox(window,width = 40,height = 15)
list4.grid(row = 3,column = 2,columnspan=2,pady = 5,padx = 20)

button1 = Button(window, text = "Get Graph Analysis Result",command = getGraphAnalysisResults)
button1.grid(row = 4,column = 2,columnspan = 2,pady = 5,padx = 20)

window.title("Graph Analysis")
window.mainloop()