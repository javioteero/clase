# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 12:56:15 2025

@author: otero
"""

import pulp as lp


model = lp.LpProblem("examen", lp.LpMinimize)

#Datos

F = ["Bilbao", "Vigo", "Sevilla"]

CD = ["Zaragoza", "Madrid"]

C = ["Almería", "Barcelona", "Gijón"]

CT1 = {("Bilbao", "Zaragoza"):10,("Bilbao", "Madrid"):15,("Vigo", "Zaragoza"):12,("Vigo", "Madrid"):8,("Sevilla", "Zaragoza"):20,("Sevilla", "Madrid"):14}

CT2 = {("Zaragoza", "Almería"):10,("Zaragoza", "Barcelona"):12,("Zaragoza", "Gijón"):20,("Madrid", "Almería"):15,("Madrid", "Barcelona"):8,("Madrid", "Gijón"):14}

K = {"Bilbao": 500, "Vigo": 650, "Sevilla": 500}

H = {"Bilbao": 2, "Vigo": 1.8, "Sevilla": 2.2}

S = {"Zaragoza": 1500, "Madrid":1200}

D = {"Almería": 500, "Barcelona": 1500, "Gijón": 300}


#Variables

x = lp.LpVariable.dicts("x", [(f,d,c) for f in F for d in CD for c in C], lowBound=0, cat="Integer")

BA = lp.LpVariable("BA", lowBound=0, cat="Integer")

MB = lp.LpVariable("MB", lowBound=0, cat="Integer")

#Función objetivo

model += lp.lpSum((CT1[(f,d)] + CT2[(d,c)]) * x[(f,d,c)] for f in F for d in CD for c in C)

#Restricciones

for f in F:
    model += lp.lpSum(x[(f,d,c)] for d in CD for c in C) <= H[f] * K[f]
    
for d in CD:
    model += lp.lpSum(x[(f,d,c)] for f in F for c in C) <= S[d]
    
for c in C:
    model += lp.lpSum(x[(f,d,c)] for f in F for d in CD) == D[c]
    
model += BA == lp.lpSum(x[("Bilbao",d,"Almería")] for d in CD)
    
model += MB == lp.lpSum(x[(f,"Madrid","Barcelona")] for f in F)

#Resolver

model.solve()

print("\n Estado del problema: ", lp.LpStatus[model.status])

print("\n Variables: ")
for v in model.variables():
    print(v.name, " = ", v.value())

print("\n Función objetivo: ", lp.value(model.objective))

#Las ditancias de los apartados b y c estan en las variables