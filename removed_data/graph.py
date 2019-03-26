import networkx as nx
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt


import matplotlib as mpl


# Read the vector file
import glob


def processData(name1):
    mydata = genfromtxt(name1, delimiter=',')
    adjacency = mydata[0:, 1:]
    processNumbers = mydata[0:, 0]
    # print "Number of processes:"+ str(len(adjacency))
    rows, cols = np.where(adjacency > 0)
    edges = zip(rows.tolist(), cols.tolist())
    # print processNumbers
    # Constract the DiGraph G
    G = nx.DiGraph()
    G.add_edges_from(edges)
    for u, v, a in G.edges(data=True):
        G.add_edge(u, v, weight=adjacency[u][v])
        # print u,v,adjacency[u][v]
    # print list(G.edges.data())

    # In order to find disconnected graph
    gr = nx.Graph()
    gr.add_edges_from(edges)

    # print out the disconected subgraph
    graphs = list(nx.connected_component_subgraphs(gr))

    # print "###################################################"
    # print "Number of subgraph:" + str(len(graphs))
    # for i in range(len(graphs)):
    # print "------------ Subgraph  "+str(i)+"  ------------"
    # print graphs[i-1].nodes()

    top = []
    indexTop = 5
    # Computer the rank of Graph G, G is digraph
    pr = nx.pagerank(G, weight="weight", alpha=0.9)
    for key, value in sorted(pr.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        if (indexTop == 0):
            break
        indexTop -= 1
        # print "%s:   %s   : %s" % (key, processNumbers[key], value)
        top.append(processNumbers[key])
    # print top
    # print "###################################################"
    # print "Page rank of our processes"
    # print pr

    # print gr.edges.data()

    subgraphNumber = 0

    # make the size of nodes bigger based on their rank
    node_sizes = [500 + 6000 * pr[i]
                  for i in range(len(graphs[subgraphNumber]))]

    # Color of edges and nodes

    pos = nx.spring_layout(graphs[subgraphNumber])
    colors = range(len(graphs[subgraphNumber]))
    edgeColors = range(graphs[subgraphNumber].number_of_edges())

    # Plot the graph based on page rank
    fig = plt.figure()
    ax = nx.draw(graphs[subgraphNumber], pos, node_color="#1a9641", edge_color=edgeColors, width=3,
                 node_size=node_sizes, edge_cmap=plt.cm.Set1, with_labels=True, 		font_color="#ffffff", alpha=0.95)
    fig.set_facecolor("#ffffbf")
    # plt.show()
    return top


def processCR3(name, topCR3v, dirName, CPUName, vcpu):
    print("----- Enter Process CR3 ----")
    raw_data = []
    labels = np.genfromtxt(name, delimiter=',', usecols=0, dtype=str)
    # print(labels)
    raw_data = np.genfromtxt(name, delimiter=',')[:, 1:]
    labelsOfvcpu = np.genfromtxt(vcpu, delimiter=',', usecols=0, dtype=str)

    print(labelsOfvcpu)
    # print(raw_data)
    vmName = []
    process = []
    for label in labels:
        vmName.append(label.split('/')[0])
        process.append(label.split('/')[1])
    sumRawData = []
    for cr3 in topCR3v:
        if str(int(cr3)) in process:
            indexOfProcess = process.index(str(int(cr3)))
            for i in range(0, len(raw_data[indexOfProcess])):
                if len(sumRawData) < len(raw_data[indexOfProcess]):
                    sumRawData.append(raw_data[indexOfProcess][i])
                else:
                    sumRawData[i] += raw_data[indexOfProcess][i]
    file = open(CPUName, "w")

    eightZero = ",0,0,0,0,0,0,0,0"

    if (labelsOfvcpu.ndim != 0):
        for indexvcpu in labelsOfvcpu[1:]:
            stringItem = indexvcpu + eightZero
            file.write(stringItem+"\n")
    if (labelsOfvcpu.ndim != 0):
        stringItem = labelsOfvcpu[0]
    else:
        stringItem = str(labelsOfvcpu)
    for iteminRaw_data in sumRawData:
        stringItem = stringItem + "," + str(int(iteminRaw_data))
    print(stringItem)
    file.write(stringItem+"\n")
    print(sumRawData)
    print("--------------------------------")

    # processes = mydata[0:, 1:]
    # processNames = mydata[0:, 0]

    # for cr3 in topCR3v:
    #    print cr3
    # print processNames

    # print processes
    # print topCR3v


def processCPU(CPUName):
    # print(labels)
    print(CPUName)
    raw_data = np.genfromtxt(CPUName, delimiter=',')[:, 1:]
    print(raw_data)


i = 0
topCR3 = []
for name in glob.glob('data/*'):
    print("--------------------------------------")
    print(name)
    for adjacenName in glob.glob(name+'/processAdjacencyMatrix*'):
        topCR3 = processData(adjacenName)
    for processName in glob.glob(name+'/processInternal*'):
        # print adjacenName
        for CPUName in glob.glob(name+'/cpuInternal*'):
            for vcpu in glob.glob(name+'/cpuFrequency*'):
                processCR3(processName, topCR3, name, CPUName, vcpu)
