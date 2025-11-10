# -*- coding: utf-8 -*-


import pulp as lp
import random

# --------------------------------------------------------
#         DATOS
# --------------------------------------------------------

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

Cv = {} #Coste variable por arco

for i in arcos:
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


# y aleatorio

ybar = {}
for i in arcos:
    ybar[i] = 1 if random.random() < 0.7 else 0

print("|n Valores de ybar: ")
for i in arcos:
    print(f"ybar{i}= {ybar[i]}")


# --------------------------------------------------------------------------------------------------------
#  PROBLEMA PRIMAL
# --------------------------------------------------------------------------------------------------------

primal = lp.LpProblem("Primal", lp.LpMinimize)


#Variables

x = lp.LpVariable.dicts("x", [(p, a) for p in productos for a in arcos], lowBound=0, cat="Continuous")

#Función objetivo

primal += lp.lpSum(Cv[a] * x[(p,a)] for p in productos for a in arcos )


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
            
        primal += salida - entrada == balance

for (i, j) in arcos:
    primal += lp.lpSum(x[p, (i, j)] for p in productos) <= 100 * ybar[(i, j)]

#Resolver

primal.solve()

print("\n Estado del problema primal: ", lp.LpStatus[primal.status])
print("\n Objetivo primal: ", lp.value(primal.objective))

# --------------------------------------------------------------------------------------------------------------
#  PROBLEMA DUAL
# --------------------------------------------------------------------------------------------------------------

dual = lp.LpProblem("Dual", lp.LpMaximize)


#Variables

xi = lp.LpVariable.dicts("xi", [(p, i) for p in productos for i in nodos], lowBound=None, cat="Continuous")

yi = lp.LpVariable.dicts("yi", [(p, a) for p in productos for a in arcos], lowBound=0, cat="Continuous")


#Función objetivo

b = {}
for p in productos:
    for i in nodos:
        if i == Start[p]:
            b[(p, i)] = 1
        elif i == End[p]:
            b[(p, i)] = -1
        else:
            b[(p, i)] = 0


dual += (
    lp.lpSum(b[(p, i)] * xi[(p, i)] for p in productos for i in nodos) +
    lp.lpSum(ybar[a] * yi[(p, a)] for p in productos for a in arcos)
)


#Restricción

for p in productos:
    for (i,j) in arcos:
        dual += (xi[(p,j)] - xi[(p,j)] + yi[(p, (i,j))]) <= Cv[(i,j)]



#Resolver

dual.solve()

print("\n Estado del problema dual: ", lp.LpStatus[primal.status])
print("\n Objetivo dual: ", lp.value(primal.objective))











