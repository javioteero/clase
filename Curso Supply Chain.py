# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 14:16:11 2025

@author: otero
"""

#%% Ejercicio 1
"""
Continue the case study of the Capacitated Plant Location model of a car manufacture. 
You are given four Pandas data frames demand, var_cost, fix_cost, and cap containing the regional demand (thous. of cars), 
variable production costs (thous. $US), fixed production costs (thous. $US), and production capacity (thous. of cars). 
All these variables have been printed to the console for your viewing.

Dmd
Supply_Region        
USA            2719.6
Germany          84.1
Japan          1676.8
Brazil          145.4
India           156.4
               USA  Germany  Japan  Brazil  India
Supply_Region                                    
USA              6       13     20      12     17
Germany         13        6     14      14     13
Japan           20       14      3      21      9
Brazil          12       14     21       8     21
India           22       13     10      23      8
               Low_Cap  High_Cap
Supply_Region                   
USA               6500      9500
Germany           4980      7270
Japan             6230      9100
Brazil            3230      4730
India             2110      3080
               Low_Cap  High_Cap
Supply_Region                   
USA                500      1500
Germany            500      1500
Japan              500      1500
Brazil             500      1500
India              500      1500
"""

from pulp import *

# Initialize Class
model = LpProblem("Capacitated Plant Location Model", LpMinimize)

# Define Decision Variables
loc = ['USA', 'Germany', 'Japan', 'Brazil', 'India']
size = ['Low_Cap','High_Cap']
x = LpVariable.dicts("production_",
                     [(i,j) for i in loc for j in loc],
                     lowBound=0, upBound=None, cat='Continuous')
y = LpVariable.dicts("plant_", 
                     [(i,s) for s in size for i in loc], cat='Binary')

# Define objective function
model += (lpSum([fix_cost.loc[i,s] * y[(i,s)] 
                 for s in size for i in loc])
          + lpSum([var_cost.loc[i, j] * x[(i, j)] 
                   for i in loc for j in loc]))


#%% Ejercicio 2
"""
Your customer has ordered six products to be delivered over the next month. 
You will need to ship multiple truck loads to deliver all of the products. 
There is a weight limit on your trucks of 25,000 lbs. For cash flow reasons you desire to ship 
the most profitable combination of products that can fit on your truck.

Product	Weight (lbs)	Profitability ($US)
A	12,583	102,564
B	9,204	130,043
C	12,611	127,648
D	12,131	155,058
E	12,889	238,846
F	11,529	197,030
Two Python dictionaries weight, and prof, and a list prod have been created for you containing the weight, 
profitability, and name of each product. You can explore them in the console.

"""
from pulp import *
# Initialized model, defined decision variables and objective
model = LpProblem("Loading Truck Problem", LpMaximize)
x = LpVariable.dicts('ship_', prod, cat='Binary')
model += lpSum([prof[i] * x[i] for i in prod])

# Define Constraint
model += lpSum([weight[i] * x[i] for i in prod]) <= 25000
model += x['D'] + x['E'] + x['F'] <= 1

model.solve()
for i in prod:
    print("{} status {}".format(i, x[i].varValue))
    
    
#%% Ejercicio 3 - local constraints 2
"""
You work at a trucking distribution center and you need to decide which of 6 customer
 locations you will send a truck to. Your goal is to minimize the distance a truck travels.

Location	Distance
A	86
B	95
C	205
D	229
E	101
F	209
A dictionary dist, and a list cust have been created for you containing the distance, 
and name of each customer location. These inputs have been printed in console for you.

""" 
model = LpProblem("Loading Truck Problem", LpMinimize)
x = LpVariable.dicts('ship_', cust, cat='Binary')
model += lpSum([dist[i]*x[i] for i in cust])

# Define Constraint
model += x['A'] + x['B'] + x['C'] + x['D'] + x['E'] + x['F'] >= 1
model += x['A'] - x['D'] <= 0
model += x['B'] - x['E'] <= 0

model.solve()
for i in cust:
    print("{} status {}".format(i, x[i].varValue)) 
    
#%% Bakery

import pulp as lp

model = lp.LpProblem("Bakery", sense = lp.LpMaximize)

num_oven = 1
num_bakers = 2
num_packaging = 1 #(pero solo trabaja 22dias/mes)

#Variables

A = lp.LpVariable("A", lowBound=0, cat="Integer")
B = lp.LpVariable("B", lowBound=0, cat="Integer")

#Función objetivo

model += 20*A + 40*B



#Restricciones
model += 0.5*A + B <= 30
model += A + 2.5*B <= 60
model += A + 2*B <= 22

#Resolver

model.solve()

print("\nEstado del problema: ", lp.LpStatus[model.status])
print("Produce {} Cake A".format(A.varValue))
print("Produce {} Cake B".format(B.varValue))

#%% Logistics planning problem
#You are consulting for kitchen oven manufacturer helping to plan their logistics for next month. 
#There are two warehouse locations (New York, and Atlanta), and four regional customer locations 
#(East, South, Midwest, West). The expected demand next month for East it is 1,800, for South it 
#is 1,200, for the Midwest it is 1,100, and for West it is 1000. The cost for shipping each of the
#warehouse locations to the regional customer's is listed in the table below. Your goal is to 
#fulfill the regional demand at the lowest price.

#Inicio

import pulp as lp

model = lp.LpProblem("logistics planning", lp.LpMinimize)



#Datos

costs = {('New York', 'East'): 211, ('New York', 'South'): 232, ('New York', 'Midwest'): 240, ('New York', 'West'): 300, ('Atlanta', 'East'): 232, ('Atlanta', 'South'): 212, ('Atlanta', 'Midwest'): 230, ('Atlanta', 'West'): 280}

warehouses = ['New York', 'Atlanta']
customers = ['East', 'South', 'Midwest', 'West']

demanda = {'East':1800, 'South': 1200, 'Midwest':1100, 'West':1000}

#Variables

num_viajes = lp.LpVariable.dicts("num_viajes",[(c1,c2) for c1 in warehouses for c2 in customers], lowBound=0, cat="Integer" )

#coste = lp.LpVariable("coste", lowBound=0, cat="Continuous")

#Función objetivo

model += lp.lpSum([num_viajes[(i,j)] * costs[i,j] for i in warehouses for j in customers])

#Restricciones


for j in customers:
    model += lp.lpSum(num_viajes[(i,j)] for i in warehouses) == demanda[j]
        

#Resolver

model.solve()

print("\nEstado del problema: ", lp.LpStatus[model.status])

print("\nValor de las variables: ")
for v in model.variables():
    print(v.name," = ", v.value())
print("\nValor de la función objetivo: ", lp.value(model.objective))

#%% Traveling salesman

import pulp as lp

#cities =     0   1   2   3   4   ...  10  11  12  13  14
#0    0  29  82  46  68  ...  29  74  23  72  46
#1   29   0  55  46  42  ...  41  51  11  52  21
#2   82  55   0  68  46  ...  79  21  64  31  51
#3   46  46  68   0  82  ...  21  51  51  43  64
#4   68  42  46  82   0  ...  82  58  46  65  23
#5   52  43  55  15  74  ...  33  37  51  29  59
#6   72  43  23  72  23  ...  77  37  51  46  33
#7   42  23  43  31  52  ...  37  33  33  31  37
#8   51  23  41  62  21  ...  62  46  29  51  11
#9   55  31  29  42  46  ...  51  21  41  23  37
#10  29  41  79  21  82  ...   0  65  42  59  61
#11  74  51  21  51  58  ...  65   0  61  11  55
#12  23  11  64  51  46  ...  42  61   0  62  23
#13  72  52  31  43  65  ...  59  11  62   0  59
#14  46  21  51  64  23  ...  61  55  23  59   0
model = lp.LpProblem("Travelingsalesman", lp.LpMinimize)
# Define Decision Variables
x = lp.LpVariable.dicts('X', [(c1, c2) for c1 in cities for c2 in cities], 
                     cat='Binary')
u = lp.LpVariable.dicts('U', [c1 for c1 in cities], 
                     lowBound=0, upBound=(n-1), cat='Integer')

# Define Objective
model += lp.lpSum([dist.iloc[c1, c2] * x[(c1, c2)] 
                for c1 in cities for c2 in cities])

# Define Constraints
for c2 in cities:
    model += lpSum([x[(c1, c2)] for c1 in cities]) == 1
for c1 in cities:
    model += lpSum([x[(c1, c2)] for c2 in cities]) == 1
    
#%% Decision variables of case study
#Continue the case study of the Capacitated Plant Location model of a car manufacture. 
#You are given four Pandas data frames demand, var_cost, fix_cost, and cap containing 
#the regional demand (thous. of cars), variable production costs (thous. $US), fixed 
#production costs (thous. $US), and production capacity (thous. of cars). All these 
#variables have been printed to the console for your viewing.

loc = ['USA', 'Germany', 'Japan', 'Brazil', 'India']

demanda = {'USA': 2719.6, 'Germany': 84.1, 'Japan': 1676.8, 'Brazil': 145.4, 'India':156.4}


# (...)


#%% Logical constraints Example1
#Select most profitable product to ship without exceeding weight limit
#Decision variables: Xi=1 product_i_ is selected else 0
#Objetive: maximize profitability
#Constraint: Weight <= 20000


import pulp as lp

model = lp.LpProblem("logicalconstraints", lp.LpMaximize)


product = ["A", "B", "C", "D", "E", "F"]
weight = {"A":12800, "B":10900, "C":11400, "D":2100, "E":11300, "F":2300}
profitability = {"A":77878, "B":82713, "C":82728, "D":68423, "E":84119, "F":77765}

#Variables

x = lp.LpVariable.dicts("x", [i for i in product], lowBound=0, upBound=1, cat="Binary")

#Función objetivo

model += lp.lpSum(x[i]*profitability[i] for i in product)

#Restricciones

model += lp.lpSum(x[i]*weight[i] for i in product) <= 20000

#Logical contraint Ex. 1
#Either product E is selected or product D is selected, but not both

model += x["E"] + x["D"] <= 1

#Logical constraint Ex. 2
#If product D is selected then product B must also be selected

model += x["D"] == x["B"]



#Resolver

model.solve()

print("\nEstado del problema: ", lp.LpStatus[model.status])

print("\nValor de las variables: ")
for v in model.variables():
    print(v.name," = ", v.value())
print("\nValor de la función objetivo: ", lp.value(model.objective))



#%%Logical contraints ex. 2
#You work at a trucking distribution center and you need to decide which of 6 customer
#locations you will send a truck to. Your goal is to minimize the distance a truck travels.

import pulp as lp

model = lp.LpProblem("logicalconstraints2", lp.LpMinimize)

location = ['A', 'B', 'C', 'D', 'E', 'F']
distancia = {'A': 86, 'B': 95, 'C': 205, 'D': 229, 'E': 101, 'F': 209}


#Variables

x = lp.LpVariable.dict("x", location, lowBound=0, upBound=1, cat="Binary")

#Función objetivo

model += lp.lpSum(x[i]*distancia[i] for i in location)

#Resticciones

model += lp.lpSum(x[i] for i in location) >= 1

model += x["A"] == x["D"]

model += x["B"] == x["E"]


#Resolver

model.solve()

print("\nEstado del problema: ", lp.LpStatus[model.status])

print("\nValor de las variables: ")
for v in model.variables():
    print(v.name," = ", v.value())
print("\nValor de la función objetivo: ", lp.value(model.objective))


#%% Contraint combination exercise


import pulp as lp

model = lp.LpProblem("contraintcomb", lp.LpMinimize)


W = ["W1","W2"]
P =["A", "B", "C"]
C = ["C1", "C2", "C3", "C4"]


#W1 is small and can either ship 10 products A
#per a week or 15 products B per a week or 20
#products C per a week.


demanda = {("A","C1"):10,("A","C2"):8,("A","C3"):28,("A","C4"):0,("B","C1"):17,("B","C2"):11,("B","C3"):10,("B","C4"):6,("C","C1"):23,("C","C2"):20,("C","C3"):25,("C","C4"):13}













































