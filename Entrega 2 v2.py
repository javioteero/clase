# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 18:40:18 2025

@author: Javi
"""

import pulp as lp

#PROBLEMA

model = lp.LpProblem("Entrega2 Ej1", lp.LpMinimize)

#DATOS

nodes = [1, 2, 3, 4]
products = ["P1","P2"]
arcs = [(1, 2), (1, 4), (2, 3), (2, 4), (3, 4)]


Cf = {(1, 2): 5,
      (1, 4): 10,
      (2, 3): 25,
      (2, 4): 15,
      (3, 4): 20}


Cv = {(1, 2): 5,
      (1, 4): 30,
      (2, 3): 5,
      (2, 4): 6,
      (3, 4): 5}

Start = {"P1": 1, "P2": 1}
End = {"P1": 3, "P2": 4}


#Variables

x = lp.LpVariable.dicts("x", [(p, a) for p in products for a in arcs], lowBound=0, cat="Continuous" )

y = lp.LpVariable.dicts("y", arcs, lowBound=0, upBound=1, cat="Binary")

#Función objetivo

CF = lp.lpSum(Cf[a] * y[a] for a in arcs)

CV = lp.lpSum(Cv[a] * x[(p,a)] for p in products for a in arcs )

model += CF + CV


#Restricciones


for p in products:
    for i in nodes:
        salida = lp.lpSum(x[(p,a)] for a in arcs if a[0] == i)
        entrada = lp.lpSum(x[(p,a)] for a in arcs if a[1] == i)
        
        if i == Start[p]:
            balance = 1
        elif i == End[p]:
            balance = -1
        else:
            balance = 0
            
        
        model += salida - entrada == balance

     # Si y=0 no puede haber flujo
     
for (i, j) in arcs:
    model += lp.lpSum(x[p, (i, j)] for p in products) <= 100 * y[(i, j)]



#Resolver

model.solve()

print("\n Estado del problema: ", lp.LpStatus[model.status])
print("\n Objetivo: ", lp.value(model.objective))


print("\n Arcos abiertos:")
for a in arcs:
    if y[a].varValue > 0.001:
        print(f"  {a}: abierto ({y[a].varValue})")

print("\n Flujos por producto:")
for p in products:
    print(f"Producto {p}:")
    for a in arcs:
        val = x[(p, a)].varValue
        if val and val > 1e-6:
            print(f"  Flujo {val:.2f} por arco {a}")









