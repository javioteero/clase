# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 19:27:48 2025

@author: Javi
"""

import pulp as lp
import random

N_nodos = 20
N_productos = 10
Prob_arco = 0.15

random.seed(0)  #LUEGO QUITAR


nodos = list(range(1, N_nodos + 1))
productos = [f"P{i}" for i in range(1, 11)]


#Red

arcos=[]

for i in nodos:
    for j in nodos:
        if i != j:
            if random.random() < Prob_arco:
                arcos.append((i, j))

arcos = list(set(arcos))  #Evita duplicados

print("\n Red generada:")

print("   Nodos:", len(nodos))
print("   Productos:", len(productos))
print("   Nodos:", len(arcos))


#Costes aleatorios

Cf = {} #Coste fijo por arco
Cv = {} #Coste variable por arco

for i in arcos:
    Cf[i] = random.randint(5, 30)
    Cv[i] = random.randint(1, 10)
    

#Origenes y destinos aleatorios para cada producto

Start = {}
End = {}

for p in productos:
    s = random.choice(nodos)
    e = random.choice(nodos)
    while e==s:
        e = random.choice(nodos)
    
    Start[p] = s
    End[p] = e

print("origenes:", Start)
print("Destinos: ", End)

