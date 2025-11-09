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

#random.seed(0)  #LUEGO QUITAR


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

#Problema

model = lp.LpProblem("Entrega2 ej2", lp.LpMinimize)

#Variables

x = lp.LpVariable.dicts("x", [(p, a) for p in productos for a in arcos], lowBound=0, cat="Continuous" )

y = lp.LpVariable.dicts("y", arcos, lowBound=0, upBound=1, cat="Binary")

#Función objetivo

CF = lp.lpSum(Cf[a] * y[a] for a in arcos)

CV = lp.lpSum(Cv[a] * x[(p,a)] for p in productos for a in arcos )

model += CF + CV


#Restricciones

for p in productos:
    for i in nodos:
        salida = lp.lpSum(x[(p,a)] for a in arcos if a[0] == i)
        entrada = lp.lpSum(x[(p,a)] for a in arcos if a[1] == i)
        
        if i == Start[p]:
            balance = 1
        elif i == End[p]:
            balance = -1
        else:
            balance = 0
            
        
        model += salida - entrada == balance

     # Si y=0 no puede haber flujo
     
for (i, j) in arcos:
    model += lp.lpSum(x[p, (i, j)] for p in productos) <= 100 * y[(i, j)]
    

#Resolver

model.solve()

print("\n Estado del problema: ", lp.LpStatus[model.status])
print("\n Objetivo: ", lp.value(model.objective))


print("\n Arcos abiertos:")
for a in arcos:
    if y[a].varValue > 0.001:
        print(f"  {a}: abierto")

print("\n Flujos por producto:")
for p in productos:
    print(f"Producto {p}:")
    for a in arcos:
        val = x[(p, a)].varValue
        if val and val > 1e-6:
            print(f"  Flujo {val:.2f} por arco {a}")



