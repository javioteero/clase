import pulp
import random


print("Génération de l'instance (20 nœuds, 10 produits)...")

NUM_EXTRA_ARCS = 70 


nodes = list(range(20))
products = [1, 2, 3, 4, 5, 6, 7, 8, 9,10]

arcs = []

#path seguro
for i in range(0, 19):
    arcs.append((i, i + 1))
    
#raccourcie
while len(arcs) < (19 - 1) + NUM_EXTRA_ARCS:
    i = random.randint(1, 19 - 1)
    j = random.randint(i + 1, 19) # j doit être après i
    if (i, j) not in arcs:
        arcs.append((i, j))

print("Instance créée avec", len(nodes), "nœuds", "et", {len(arcs)}, "arcs.")


Cf = {}
Cv = {}

for a in arcs:
        Cf[a] = random.randint(5, 100)
        Cv[a] = random.randint(5, 30)

# 1.4. Origines (Start) et Destinations (End)
# Garanti faisable car on choisit toujours Start < End
Start = {}
End = {}
for p in products:
    origin = random.randint(1, 19 - 1)
    destination = random.randint(origin + 1, 19)
    Start[p] = origin
    End[p] = destination
    print("Produit",p, origin, "->", destination)

print("")    
print("list arc pour exo 3")
print(arcs)
print("")    
print("list Cv pour exo 3")
print(Cv)
print("")    
print("list start pour exo 3")
print(Start)
print("")    
print("list End pour exo 3")
print(End)


model = pulp.LpProblem("Minicost2", pulp.LpMinimize)


z = pulp.LpVariable.dicts("Open", arcs, cat='Binary')
x = pulp.LpVariable.dicts("Flujo", [(p, a) for p in products for a in arcs], cat='Binary')


Cf_tot = pulp.lpSum(Cf[a] * z[a] for a in arcs)
Cv_tot = pulp.lpSum(Cv[a] * x[(p, a)] for a in arcs for p in products)

model += Cv_tot + Cf_tot


for p in products:
    for i in nodes:
        flow_out = pulp.lpSum(x[(p, (i, j))] for (i_j, j) in arcs if i_j == i)
        flow_in = pulp.lpSum(x[(p, (j, i))] for (j, i_i) in arcs if i_i == i)
        
        balance = 0
        if i == Start[p]:
            balance = 1  
        elif i == End[p]:
            balance = -1 
            
        model += (flow_out - flow_in == balance)

for p in products:
    for a in arcs :
        model += x[(p, a)] <= z[a]

model.solve()
print("Solution Status :", pulp.LpStatus[model.status])
print("-"*20)
print("Optimal Total Cost =", pulp.value(model.objective),"euros")

for a in arcs :
    if pulp.value(z[a])>0:
        print("The arc",a,"is open with a variable cost of", Cv[a], "euros")

print("")        
print("-"*20)        
for p in products:
    print("path of the product :", p)
    for a in arcs:
        if pulp.value(x[(p, a)]) > 0 : 
            cost = Cv[a]
            print("Uses Arc",a)
    print("")        
    print("-"*20)
    
print("Variable Cost is", pulp.value(Cv_tot), "euros")
print("-"*20)
print("Fixe Cost is", pulp.value(Cf_tot), "euros")
