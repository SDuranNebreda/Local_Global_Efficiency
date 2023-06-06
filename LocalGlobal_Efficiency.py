#Local-Global Efficiency calculation following (Latora and Marchiori, 2001) algorithm using NetworkX
#Code by Salva Duran-Nebreda 2023
import networkx as nx


#Function Declaration for Local-Global Efficiency
def Compute_Efficiency(Target_Graph):

    Graph_Set = list(Target_Graph.nodes())
    Efficiency = 0

    for n in list(Target_Graph.nodes()):
        Explored_Set = list()
        Explored_Set.append(n)
        Last_Set = list()
        for k in Target_Graph.neighbors(n):
            Last_Set.append(k)

        Distance_Counter = 1
        while (len(Graph_Set) > len(Explored_Set)):
            Future_Last_Set = list()
            while (len(Last_Set) > 0):
                L = Last_Set.pop()
                Explored_Set.append(L)
                Efficiency += (1 / Distance_Counter) / (Target_Graph.number_of_nodes() * (Target_Graph.number_of_nodes() - 1))
                for k in Target_Graph.neighbors(L):
                    if (k not in Explored_Set and k not in Last_Set and k not in Future_Last_Set):
                        Future_Last_Set.append(k)
            Last_Set.extend(Future_Last_Set)
            Distance_Counter += 1
    return [Efficiency]


#Initialize Graph
path = 'Graph_path_placeholder.csv'
G = nx.read_edgelist(path, delimiter=',')
Graph_Size = G.number_of_nodes()

#Compute Global Efficiency
Global_Efficiency = Compute_Efficiency(G)[0]

#Compute Local Efficiency
Local_Efficiency = 0
for i in list(G.nodes()):
    SubGraph_list = list()
    SubGraph_list.append(i)
    
    #Local Efficiency requires creating subgraphs with "damaged" nodes (removed)
    #These following lines of code create subgraphs with missing neighboring nodes
    Damaged_SubGraph_list = list()
    for j in G.neighbors(i):
        if (j not in SubGraph_list):
            SubGraph_list.append(j)
            Damaged_SubGraph_list.append(j)

    SubGraph = nx.subgraph(G, SubGraph_list)
    Damaged_SubGraph = nx.subgraph(G, Damaged_SubGraph_list)

    #Once the subgraphs are created (and if they are not empty or disconnected) compute efficiency
    if (len(Damaged_SubGraph.nodes()) > 1):
        if (nx.is_connected(Damaged_SubGraph)):
            Local_Efficiency+=(Compute_Efficiency(Damaged_SubGraph)[0]/Compute_Efficiency(SubGraph)[0])/G.number_of_nodes()

