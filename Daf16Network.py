import json
import plotly.graph_objects as go
import networkx as nx
from pyvis.network import Network
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import xlrd

f = open('gene_WBGene00000912_interactions.json')
workbook = xlrd.open_workbook("Literature_Gene_Network.xlsx")
f1 = workbook.sheet_by_index(0)

data = json.load(f)
j=1


'''
for i in data["fields"]["interactor_types"]["data"]:
    print(i["interactor"]["label"])
    j+=1
'''
sources = []
targets = []
types = []
for i in range(1,28):
    sources.append(f1.cell_value(i,0).lower())
    targets.append(f1.cell_value(i,1).lower())
    types.append(f1.cell_value(i,2))
        
sources.append(data["fields"]["interactions"]["data"]["edges"][0]["effector"]["label"])
targets.append(data["fields"]["interactions"]["data"]["edges"][0]["affected"]["label"])
for i in data["fields"]["interactions"]["data"]["edges"]:
    #print(i["effector"]["label"] + " -> " + i["affected"]["label"] + "       " + i["type"])
    if (i["effector"]["label"]!=sources[j-1] and i["affected"]["label"]!=targets[j-1]):
        sources.append(i["effector"]["label"])
        targets.append(i["affected"]["label"])
        types.append(i["type"].split(':'))
        j+=1



 
g = Network(directed=True, bgcolor="white", font_color="black", select_menu=True, filter_menu=True)

edge_data = zip(sources, targets, types)

stop=0
for e in edge_data:
    stop+=1
    if stop==28: #stopping before adding gene interactions
        break
    col='cyan'
    src = e[0]
    tgt = e[1]
    typ = e[2]
    if (typ=="IIS "):
        col='orange'
    elif (typ=="JKN"):
        col='red'
    elif (typ=="AMPK"):
        col='purple'
    elif (typ=="germline"):
        col='green'
    elif (typ=="TOR"):
        col='yellow'
    if src=="daf-16":
        g.add_node(src, src, title=src, value = 4)
        g.add_node(tgt, tgt, title=tgt, value = 1, color=col)
    elif tgt=="daf-16":
        g.add_node(src, src, title=src, value = 1, color=col)
        g.add_node(tgt, tgt, title=tgt, value = 4)
    else:
        g.add_node(src, src, title=src, value = 1, color=col)
        g.add_node(tgt, tgt, title=tgt, value = 1, color=col)
    g.add_edge(src, tgt)

g.show_buttons(filter_=['nodes', 'edges', 'physics', 'manipulation', 'layout'])
g.toggle_physics(False)





g.write_html("daf16.html")


