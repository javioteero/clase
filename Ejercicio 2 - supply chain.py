# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 19:50:08 2025

@author: Javi
"""

from pulp import *

model = Lpproblem("Simulacro2", LpMinimize)

#Datos

A = {"A1", "A2", "A3"}
C = {"C1", "C2"}

#Parámetros

costes_fijos = {"A1": 100, "A2": 80, "A3": 90}
capacidades = {"A1": 50, "A2": 50, "A3": 40}
costes_unit = {("A1","C1"): 3, ("A1","C2"): 2,("A2","C1"): 1,("A2","C2"): 3,("A3","C1"): 2,("A3","C2"): 2}

demanda = {"C1": 30, "C2": 40}


#Variables

z = LpVariable.dicts("z", A, lowBound = 0, cat="Binary")

x = LpVariable.dicts("x", [(c1, c2) for c1 in A for c2 in C], lowBound = 0, cat="Integer")


#Función objetivo

model += lpSum(costes_fijos(c1)*z(c1) for c1 in A) + lpSum(costes_unit[(c2,c3)]*x[(c2,c3)] for c2 in A for c3 in C)


#Restricciones

