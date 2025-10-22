# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 18:33:46 2025

@author: Javi
"""

import pulp as lp


model = lp.LpProblem("Examen", lp.LpMaximize)

P = ["Camisa", "Pantalon", "Falda"]

HN = {"Camisa":3, "Pantalon":2, "Falda":6}

HT = 80

MT = {"Camisa":4, "Pantalon":3, "Falda":4}

MTT = 200

PVP = {"Camisa":12, "Pantalon":8, "Falda":13}

CU = {"Camisa":4, "Pantalon":3, "Falda":4}

CA = {"Camisa":200, "Pantalon":150, "Falda":100}


#Variables


y = lp.LpVariable.dicts("y", MT,  lowBound=0, upBound=1, cat="Binary")

x = lp.LpVariable.dicts("x", MT ,lowBound=0, cat="Integer")

ts = lp.LpVariable("ts", lowBound=0, cat="Integer")
#Función objetivo

model += lp.lpSum((PVP[i]-CU[i])*x[i] for i in P) - lp.lpSum(CA[i]*y[i] for i in P)

#Restricciones

model += lp.lpSum(MT[i]*x[i] for i in P) <= MTT

for i in P:
    model += HN[i] * x[i] <= HT * y[i]
    


model += ts == MTT - lp.lpSum(MT[i]*x[i] for i in P)
    
#Resolver

model.solve()

print("\n Estado del problema: ", lp.LpStatus[model.status])

print("\n Variables: ")
for v in model.variables():
    print( v.name, " = ", v.value())

          
print("\n Función objetivo: ", lp.value(model.objective))





