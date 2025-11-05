# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 18:40:18 2025

@author: Javi
"""

import pulp as lp

#PROBLEMA

model = lp.LpProblem("Entrega2", lp.LpMinimize)

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

x = lp.LpVariable.dicts("x", [(p, a) for p in products for a in arcs], lowBound=0, cat="Integer" )

y = lp.LpVariable.dicts("y", arcs, lowBound=0,upBound=1, cat="Binary")

#Función objetivo

CF = lp.lpSum(Cf[i] * y[i] for i in arcs)

CV = lp.lpSum(Cv[i] * x[(i,j)] for i in arcs for j in products)

model += CF + CV


#Parámetros












