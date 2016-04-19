#!/usr/bin/env python

'''
load MODEL strokes

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
import csv

# load model strokes
model_strokes_filename = "./accel_x model_strokes.csv"
print("reading data...")

all_data = []
f = open(model_strokes_filename)
data_file = csv.reader(f)

for row in data_file:
    all_data.append(row)

# get odd rows
strokes = []
for i in range(0, len(all_data), 2):
    strokes.append(all_data[i+1])


G=nx.Graph()
G.name = "cross-correlation stroke network"

print("adding nodes to " + G.name)

#G.add_nodes_from(stroke_ids)

# add strokes as nodes
for stroke in strokes:
#    G.add_node(list(set(node.Stroke_ID))[0], label=list(set(node.label))[0], dataframe = node)
    G.add_node(stroke[0], param = stroke[1], signal = np.array(stroke[2:], dtype = float))


print("adding edges using cross-correlation... (patience)")

# # add weights using cross-correlation between strokes (accel_x only)
# #for from_node in range(0, len(stroke_ids)):
# for from_node in range(0, 3):
#     print("adding edges to node " + str(from_node))
#     from_node_sig = strokes[from_node]['accel_x']
#     for to_node in range(from_node, len(stroke_ids)):
#         to_node_sig = strokes[to_node]['accel_x']
#         edge_weight = max(signal.correlate(from_node_sig, to_node_sig))
#         G.add_edge(from_node, to_node, weight=edge_weight )


for from_stroke in strokes:
    from_stroke_key = from_stroke[0]
    from_stroke_sig = np.array(from_stroke[2:], dtype = float)
    for to_stroke in strokes:
        to_stroke_key = to_stroke[0]
        to_stroke_sig = np.array(to_stroke[2:], dtype = float)
        edge_weight = max(signal.correlate(from_stroke_sig, to_stroke_sig))
        G.add_edge(from_stroke_key, to_stroke_key, weight=edge_weight )




# shift by min and normalize weights by max
max_weight = -1
min_weight = 1000000000000000000000
all_weights = []
adj_list = G.adj.values()
for item in adj_list:
    for sub_item in item.iteritems():
        #print(sub_item)
        s = sub_item[1]
        #print s.values()[0]
        weight = s.values()[0]
        all_weights.append(weight)


all_weights = np.array(all_weights, dtype = float)
min_all_weights = min(all_weights)
max_all_weights = max(all_weights)
all_weights = all_weights - min(all_weights)
all_weights = all_weights / max(all_weights)

i = 0
for item in adj_list:
    for sub_item in item.iteritems():
        #print(sub_item)
        sub_item[1]['weight'] = all_weights[i]
        #print s.values()[0]
        #weight = s.values()[0]
        #all_weights.append(weight)
        i = i + 1




# histogram of weights
plt.hist(all_weights, bins = 30)
plt.show()


    #    item['K1']['weight']


pos=nx.spring_layout(G, iterations = 500) # positions for all nodes
#pos=nx.spring_layout(G, iterations = 500) # positions for all nodes
#pos = nx.circular_layout(G)
#pos = nx.spectral_layout(G)


# nodes
nx.draw_networkx_nodes(G,pos,node_size=7)

# edges
nx.draw_networkx_edges(G,pos)

# labels
nx.draw_networkx_labels(G,pos,font_size=20,font_color='r', font_family='times-roman')

plt.axis('off')
#plt.savefig("weighted_graph.png") # save as png
plt.show() # display

############### TRY ADDING A FEW INDIVIDUAL STROKES ###############

# load some individual strokes
file_name = "../data/segmented_flat.csv"

print("reading data...")

data = pd.read_csv(file_name)


# insert each indiv_stroke into a list 
indiv_stroke_ids = set(data['Stroke_ID'])

indiv_strokes = []
for indiv_stroke_id in indiv_stroke_ids:
    indiv_strokes.append(data[data['Stroke_ID'] == indiv_stroke_id])


name = set(indiv_strokes[0].label).pop() + "_"+ str(set(indiv_strokes[0].Stroke_ID).pop()) 
sig_data = np.array(indiv_strokes[0])[:,3]

G.add_node(name, param = "accel_x", signal = sig_data)

for key in G.node.keys():
    to_key = key
    to_signal = (G.node[key]['signal'])
    edge_weight = max(signal.correlate(sig_data, to_stroke_sig))
    edge_weight = edge_weight - min_all_weights
    edge_weight = edge_weight / max_all_weights
    G.add_edge(name, to_key, weight=edge_weight )
