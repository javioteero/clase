# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 19:50:08 2025

@author: Javi
"""

from pulp import lp

model = lp.LpProblem("Simulacro2", lp.LpMinimize)

#Datos

A = {"A1", "A2", "A3"}
C = {"C1", "C2"}

#Parámetros

costes_fijos = {"A1": 100, "A2": 80, "A3": 90}
capacidades = {"A1": 50, "A2": 50, "A3": 40}
costes_unit = {("A1","C1"): 3, ("A1","C2"): 2,("A2","C1"): 1,("A2","C2"): 3,("A3","C1"): 2,("A3","C2"): 2}

demanda = {"C1": 30, "C2": 40}


#Variables

z = lp.LpVariable.dicts("z", A, lowBound = 0, upBound=1, cat="Binary")

x = lp.LpVariable.dicts("x", [(c1, c2) for c1 in A for c2 in C], lowBound = 0, cat="Integer")


#Función objetivo

model += lp.lpSum(costes_fijos(c1)*z(c1) for c1 in A) + lp.lpSum(costes_unit[(c2,c3)]*x[(c2,c3)] for c2 in A for c3 in C)


#Restricciones
for c in C:
    model += lp.lpSum(x[(c1,c)] for c1 in A) >= demanda[c]

for a in A:
    model += lp.lpSum(x[(a, c2)] for c2 in C) <= costes_fijos[a]


model.solve()

print("\nEstado del problema: ", lp.LpStatus[model.status])

print("\nValor de las variables: ")
for v in model.variables():
    print(v.name," = ", v.value())
print("\nValor de la función objetivo: ", lp.value(model.objective))




#%% V2


import pulp as lp

model = lp.LpProblem("Ejer2v2", lp.LpMinimize)


A = ["A1", "A2", "A3"]
C = ["C1", "C2"]

cost_f = {"A1":100, "A2":80,"A3":90}

cap = {"A1":50, "A2":50,"A3":40}

cost_unit = {("A1","C1"):3,("A1","C2"):2,("A2","C1"):1,("A2","C2"):3,("A3","C1"):2,("A3","C2"):2}

demand = {"C1": 30, "C2": 40}


#Variables

z = lp.LpVariable.dicts("z", A, lowBound=0, upBound=1, cat="Binary")

x = lp.LpVariable.dicts("x", cost_unit, lowBound=0,cat="Integer")


#Restricciones

for j in C:
    model += lp.lpSum(x[(i,j)] for i in A) >= demand[j]
    
for i in A:
    model += lp.lpSum(x[(i,j)] for j in C) <= cap[i]*z[i]
    

#Función objetivo

model += lp.lpSum(cost_f[i]*z[i] for i in A) + lp.lpSum(cost_unit[(i,j)] * x[(i,j)] for i in A for j in C)    


#Resolver


model.solve()


print("\n Estado del problema: ", lp.LpStatus[model.status])

print("\n Valores de variables: ")

for v in model.variables():
    print(v.name, " = ", v.value())

print("\n Función objetivo", lp.value(model.objective))






















#%% V3

import pulp as lp


model = lp.LpProblem("V3", lp.LpMinimize)

A = ["A1", "A2", "A3"]
C = ["C1", "C2"]

F = {"A1": 100, "A2": 80, "A3": 90}

Cap = {"A1": 50, "A2": 50, "A3": 40}

S = {("A1","C1"): 3,("A1","C2"): 2,("A2","C1"): 1,("A2","C2"): 3,("A3","C1"): 2,("A3","C2"): 2}

D = {"C1":30, "C2":40}


#Variables

z = lp.LpVariable.dicts("z", F, lowBound=0, upBound=1, cat="Binary")

x = lp.LpVariable.dicts("x", S, lowBound=0, cat= "Integer")


#Restricciones

for j in C:
    model += lp.lpSum(x[(i,j)] for i in A) >= D[j]
    
for i in A:
    model += lp.lpSum(x[(i,j)] for j in C) <= Cap[i] * z[i]

#Función objetivo

model += lp.lpSum(F[i]*z[i] for i in A) + lp.lpSum(S[(i,j)] * x[(i,j)] for i in A for j in C)


#Resolver

model.solve()

print("\n Estado del problema: ", lp.LpStatus[model.status])

print("\n Variables: ")

for v in model.variables():
    print(v.name, " = ", v.value())
    
print("Función objetivo: ", lp.value(model.objective))
















