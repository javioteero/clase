import pulp 


nodes = [1, 2, 3, 4]
products = ["1","2"]
arcs = [(1, 2), (1, 4), (2, 3), (2, 4), (3, 4)]


Cf = {(1, 2): 5,
      (1, 4): 10,
      (2, 3): 25,
      (2, 4): 15,
      (3, 4): 20}


Cv = { (1, 2): 5,
      (1, 4): 30,
      (2, 3): 5,
      (2, 4): 6,
      (3, 4): 5}

Start = {"1": 1, "2": 1}
End = {"1": 3, "2": 4}


model = pulp.LpProblem("Minicost", pulp.LpMinimize)


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
            
        model += (flow_out - flow_in == balance) #todo lo que entra sale


for p in products:
    for a in arcs :
        model += x[(p, a)] <= z[a]



model.solve()


print("Solution Status :", pulp.LpStatus[model.status])
print("-"*20)
print("Optimal Total Cost =", pulp.value(model.objective),"euros")

for a in arcs :
    if pulp.value(z[a])>0:
        print("The arc",a,"is open")

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
                
