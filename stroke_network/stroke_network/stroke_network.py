#!/usr/bin/env python

'''
load strokes

compute edges using cross-correlation

display network!
'''


"""
An example using Graph as a weighted network.
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
#try:
import matplotlib.pyplot as plt
#except:
#    raise
    
import networkx as nx
import pandas as pd
from scipy import signal

file_name = "../data/segmented_flat.csv"

print("reading data...")

data = pd.read_csv(file_name)


# insert each stroke into a list 
stroke_ids = set(data['Stroke_ID'])

strokes = []
for stroke_id in stroke_ids:
    strokes.append(data[data['Stroke_ID'] == stroke_id])


G=nx.Graph()
G.name = "cross-correlation stroke network"

print("adding nodes to " + G.name)

#G.add_nodes_from(stroke_ids)

# add strokes as nodes
for node in strokes:
#    G.add_node(list(set(node.Stroke_ID))[0], label=list(set(node.label))[0], dataframe = node)
    G.add_node(list(set(node.Stroke_ID))[0], label=list(set(node.label))[0])


print("adding edges using cross-correlation... (patience)")

# add weights using cross-correlation between strokes (accel_x only)
#for from_node in range(0, len(stroke_ids)):
for from_node in range(0, 3):
    print("adding edges to node " + str(from_node))
    from_node_sig = strokes[from_node]['accel_x']
    for to_node in range(from_node, len(stroke_ids)):
        to_node_sig = strokes[to_node]['accel_x']
        edge_weight = max(signal.correlate(from_node_sig, to_node_sig))
        G.add_edge(from_node, to_node, weight=edge_weight )




pos=nx.spring_layout(G) # positions for all nodes

# nodes
nx.draw_networkx_nodes(G,pos,node_size=700)

# edges
nx.draw_networkx_edges(G,pos)

# labels
#nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

plt.axis('off')
#plt.savefig("weighted_graph.png") # save as png
plt.show() # display
