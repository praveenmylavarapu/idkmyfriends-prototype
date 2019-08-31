# IDKmyFriends

import networkx as nx
import math
import csv
import random as rand
import sys
import matplotlib.pyplot as plt

#for saving plots
global_cnt = 0
k0 = -1
k1 = -1
DICT = dict()


#Function to build graph
def buildGraph(G, delimiter_):
    
    reader = csv.reader(open("input.csv"), delimiter=delimiter_)
    for line in reader:
        if len(line) > 2:
            if float(line[2]) != 0.0:
                #u,v,w in input file
                G.add_edge(int(line[0]),int(line[1]),weight=float(line[2]))
        else:
            #u,v in input file
            G.add_edge(int(line[0]),int(line[1]),weight=1.0)

#Compute edge betweenness and split the component into more more components based on EB.
def EBGirvanNewman(G):

    print("Inside EBGirvanNewman")
    initcomp = nx.number_connected_components(G)
    ncomp = initcomp
    print("Initial ncomp, ", ncomp)
    while ncomp <= initcomp:
        bw = nx.edge_betweenness_centrality(G, weight='weight')
        #print(bw)
        #find the edge with max centrality
        max_ = max(bw.values())
        print(".....................",max_)
        #find the edge with the highest centrality and remove all of them-more than one
        #for k, v in bw.iteritems():
        for k, v in bw.items():
            if float(v) == max_:
                G.remove_edge(k[0],k[1])
                global k1
                k1=k[1]
                global k0
                k0=k[0]
        #recalculate the no of components
        ncomp = nx.number_connected_components(G)
        print("No. of components",ncomp)
    print("Over............")
                             
#compute the modularity of current split
def GirvanNewmanGetModularity(G, deg_, totaldeg):
    New_A = nx.adj_matrix(G)
    #New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())
    #print(New_deg)
    #Computing Q Function
    comps = nx.connected_components(G)       
    #print ('No of communities in decomposed G: %d' % nx.number_connected_components(G))
    Mod = 0    
    for c in comps:
        #no of edges within a community
        EWC = 0
        #no of random edges
        RE = 0    
        for u in c:
            #print(u-1)
            EWC += New_deg[u]
            RE += deg_[u]
        Mod += ( float(EWC) - float(RE*RE)/float(2*totaldeg) )
    Mod = Mod/float(2*totaldeg)

    print ("Modularity: %f" % Mod)
    return Mod

#Optimized Update Degree for improving time complexity: Update degree only for vertices affected trough removal of edges..
def UpdateDeg(A, nodes):
    if k0 == -1 and k1 == -1:
        nodes = list(nodes)
        deg_dict = dict()
        n = len(nodes)
        print(n)
        B = A.sum(axis = 1)
        #print(B)
        #print("hello")
        for i in range(n):
            #deg_dict[i] = B[i, 0] ### MISTAKE???
            deg_dict[nodes[i]] = B[i, 0]
        #print(deg_dict)
        global DICT
        DICT = deg_dict
        return deg_dict
    else:
        S = A[k0-1].sum(axis = 1)
        #global DICT
        DICT[k0-1] = S[0,0]
        S = A[k1-1].sum(axis=1)
        DICT[k1-1] = S[0,0]

        return DICT


#GirvanNewman algorithm: find the best community split by maximizing modularity measure
def GirvanNewman(G, Orig_deg, totaldeg):
    #Find the best split of the graph
    BestQ = 0.0
    Q = 0.0
    while True:    
        EBGirvanNewman(G)
        nx.draw(G,with_labels=True)
        global global_cnt
        plt.savefig("graph " + str(global_cnt) + ".png")
        plt.clf()
        
        global_cnt += 1
        #break##
        
        print("over, check folder for png image") ##
        Q = GirvanNewmanGetModularity(G, Orig_deg, totaldeg);
        print ("Modularity of decomposed G: %f" % Q)
        if G.number_of_edges() == 0:
            break
        if Q > BestQ:
            #cnt=cnt+1
            BestQ = Q
            Bestcomps = nx.connected_components(G)    
            print ("Components:", Bestcomps)
            print("No. of edges :",G.number_of_edges())
            #if G.number_of_edges()  == 0:
            #global cnt
            #if cnt > 2:
        else:
                break
    if BestQ > 0.0:
        print ("Max modularity (Q): %f" % BestQ)
        #print ("Graph communities:", list(Bestcomps))
    else:
        print ("Max modularity (Q): %f" % BestQ)

#Main
G = nx.Graph()  #let's create the graph first
buildGraph(G, ',')
nx.draw(G,with_labels=True)
plt.savefig("inputGraph.png")
plt.clf()
                                 
nodes = G.nodes()
n = G.number_of_nodes() 
A = nx.adj_matrix(G)
#print('G nodes:', nodes)
print('G no of nodes:', n)
#print(A)

#Total weighted degree of graph
totaldeg = 0.0
for i in range(0,n):
    for j in range(0,n):
        totaldeg += A[i,j]
totaldeg = totaldeg/2.0
print(totaldeg)

#calculate the weighted degree for each node
Orig_deg = {}
Orig_deg = UpdateDeg(A, nodes)

#run Newman alg
print("calling GN")
GirvanNewman(G, Orig_deg, totaldeg)

