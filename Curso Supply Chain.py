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