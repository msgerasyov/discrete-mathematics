# -----------------------------------------------------------------------------
# egonet.py
#
# Finding 10 ego network centers
# -----------------------------------------------------------------------------


import networkx as nx

# Read data from the dataset, and create graph G_fb
G_fb = nx.read_edgelist("facebook_combined.txt", create_using = nx.Graph(), nodetype=int)

# -----------------------------------------------------------------------------
# Group degree centrality of a group of nodes S is the fraction of non-group
# members connected to group members. Notice that if S={centers of ego network},
# then group degree centrality = 1. If some of the centers are not in S, then
# it's highly likely that group degree centrality is less than 1. At least it
# holds for this particular dataset.
# -----------------------------------------------------------------------------

test = {0, 107, 348, 414, 612, 686, 698, 1684, 1912, 3437, 3980}

#compute 11 gdc's for groups of 10 elements with 1 element removed
#if by removing a certain vertex from a group we get gdc=1,
#than this vertex isn't a center.

gdc = []
for t in test:
    gdc.append((t, nx.group_degree_centrality(G_fb, test - {t})))
sorted_gdc = list(reversed(sorted(gdc, key=lambda x: x[1])))
print("Added 11th vertex:", sorted_gdc[0][0])
