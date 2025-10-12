# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 13:08:58 2025

@author: otero
"""

# Initialized model, defined decision variables and objective

from pulp import *

model = LpProblem("Simulacro", LpMinimize)


#Datos

F = ["F1", "F2", "F3"]
M = ["M1", "M2"]


#Parámetros

costes = {("F1","M1"):2, ("F1","M2"):3,("F2","M1"):1, ("F2","M2"):1,("F3","M1"):4, ("F3","M2"):2}
C = 100
capacidades = {"F1": 30, "F2": 20, "F3": 30}
demanda = {"D1": 40, "D2": 30}


#Declarar variables

x = LpVariable.dicts("x", [(c1, c2) for c1 in F for c2 in M], lowBound=0, cat="Integer")


#Función objetivo

model += lpSum(x[(c1,c2)]*costes[(c1,c2)] for c1 in F for c2 in M)


#Constraints
P = lpSum(x[(c1,c2)] for c1 in F for c2 in M)


model += P <= C

for m in M:
    model += lpSum(x[(m,c2)] for c2 in M) <= capacidades[m]

for n in F:
    model += lpSum(x[(c1, n)] for c1 in F) >= demanda[n]


#model += lpSum(x("F2",c2) for c2 in M) <= 20
#model += lpSum(x("F3",c2) for c2 in M) <= 30

#model += lpSum(x(c1,1) for c1 in F) >= 40
#model += lpSum(x(c1,2) for c1 in F) >= 30

#Solve Model
model.solve()

print(lp.LpStatus[model.status])
