# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 13:26:48 2025

@author: otero
"""

import networkx as nx

G = nx.Graph()
 
G.add_node(1)
# Anadir un nodo
G.add_nodes_from([2, 3])
G.add_nodes_from([
(4, {"color": "red"}),
(5, {"color": "green"})
])
H = nx.path_graph(10)
G.add_nodes_from(H)
# Anadir varios nodos desde un iterable
# Anadir con atributos de nodo
# Incorporar nodos de otro grafo
# G contiene todos los nodos de H, ademas de los que ya tuviese
G.add_node(H)
# Usar el grafo H como un nodo dentro de G