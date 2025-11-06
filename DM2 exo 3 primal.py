import pulp
import random

# -------------------------------------------------------------------
# DATA OF EXO 2 OKAY !
# -------------------------------------------------------------------

nodes = list(range(1, 21))
arcs= [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (2, 4), (5, 8), (11, 18), (10, 19), (4, 15), (13, 20), (11, 16), (16, 19), (10, 20), (14, 16), (15, 20), (9, 16), (17, 20), (15, 19), (2, 12), (11, 20), (6, 11), (18, 20), (10, 17), (4, 10), (1, 4), (9, 12), (14, 19), (10, 13), (2, 10), (1, 16), (2, 8), (7, 14), (4, 7), (3, 17), (7, 11), (10, 12), (3, 19), (1, 12), (4, 9), (1, 15), (16, 18), (9, 13), (6, 15), (6, 18), (2, 15), (8, 19), (6, 10), (11, 15), (2, 19), (5, 7), (15, 17), (17, 19), (12, 18), (5, 15), (16, 20), (15, 18), (13, 17), (9, 15), (6, 8), (9, 18), (4, 19), (4, 12), (8, 20), (6, 17), (5, 12), (7, 13), (5, 9), (11, 13), (12, 15), (1, 11), (1, 10), (6, 13), (13, 16), (5, 19)]
# C: Costes variables 
Cv = {(1, 2): 9, (2, 3): 28, (3, 4): 6, (4, 5): 16, (5, 6): 7, (6, 7): 7, (7, 8): 6, (8, 9): 18, (9, 10): 26, (10, 11): 21, (11, 12): 26, (12, 13): 24, (13, 14): 24, (14, 15): 21, (15, 16): 30, (16, 17): 15, (17, 18): 27, (18, 19): 23, (19, 20): 22, (2, 4): 30, (5, 8): 28, (11, 18): 12, (10, 19): 28, (4, 15): 13, (13, 20): 18, (11, 16): 20, (16, 19): 7, (10, 20): 17, (14, 16): 28, (15, 20): 29, (9, 16): 30, (17, 20): 28, (15, 19): 30, (2, 12): 30, (11, 20): 27, (6, 11): 27, (18, 20): 11, (10, 17): 27, (4, 10): 23, (1, 4): 22, (9, 12): 21, (14, 19): 13, (10, 13): 26, (2, 10): 9, (1, 16): 16, (2, 8): 7, (7, 14): 21, (4, 7): 22, (3, 17): 13, (7, 11): 8, (10, 12): 24, (3, 19): 8, (1, 12): 10, (4, 9): 6, (1, 15): 14, (16, 18): 26, (9, 13): 10, (6, 15): 12, (6, 18): 15, (2, 15): 26, (8, 19): 6, (6, 10): 19, (11, 15): 26, (2, 19): 24, (5, 7): 21, (15, 17): 15, (17, 19): 21, (12, 18): 7, (5, 15): 19, (16, 20): 15, (15, 18): 22, (13, 17): 11, (9, 15): 7, (6, 8): 17, (9, 18): 9, (4, 19): 6, (4, 12): 22, (8, 20): 10, (6, 17): 29, (5, 12): 15, (7, 13): 19, (5, 9): 15, (11, 13): 28, (12, 15): 15, (1, 11): 12, (1, 10): 13, (6, 13): 13, (13, 16): 19, (5, 19): 30}
# P: Productos
products = [f"P{i}" for i in range(1, 11)]
# O: Origines (per productos)
O = [12,14,2,15,3,8,19,19,17,8] 
# D: Destinacion (per productos)
D = [20,19,8,20,9,17,20,20,20,10] 

Start = {}
End = {}
o=0
d=0
for p in products:
    origin = O[o]
    destination = D[d]
    Start[p] = origin
    End[p] = destination
    print("Produit",p, origin, "->", destination)
    o+=1
    d+=1
    
#----------------------------------------------------------------------
#Modifier pour rendre chemin tangible ?? PAS OKAY
#-----------------------------------------------------------------
def generer_y_bar_simple(arcs):
    print("Génération d'un y_bar aléatoire simple...")
    y_bar = {} 
    for a in arcs:
        y_bar[a] = random.choice([0, 1])
    arcs_ouverts_count = sum(y_bar.values())
    print(f"-> y_bar simple généré ({arcs_ouverts_count} arcs ouverts sur {len(arcs)})")
    
    return y_bar

            

# 2. Exécuter la procédure pour obtenir nos valeurs y_bar fixes 
y_bar = generer_y_bar_simple(arcs)


# -------------------------------------------------------------------


print("\nConstruction du modèle Primal SPs(y_bar)...")

# C'est un problème de minimisation [cite: 40]
model_primal = pulp.LpProblem("SPs_Primal", pulp.LpMinimize)

x = pulp.LpVariable.dicts("Flujo", [(p, a) for p in products for a in arcs],lowBound=0, cat='Continuous')
                         
model_primal += pulp.lpSum(Cv[a] * x[(p, a)] for a in arcs for p in products)

# --- Contraintes Primales ---

for p in products:
    for i in nodes:
        flow_out = pulp.lpSum(x[(p, (i, j))] for (i_j, j) in arcs if i_j == i)
        flow_in = pulp.lpSum(x[(p, (j, i))] for (j, i_i) in arcs if i_i == i)
        
        balance = 0
        if i == Start[p]: balance = 1  
        elif i == End[p]: balance = -1 
        model_primal += (flow_out - flow_in == balance)


for p in products:
    for a in arcs :
        model_primal += x[(p, a)] <= y_bar[a]



# -------------------------------------------------------------------

print("Résolution du modèle Primal...")
model_primal.solve()

print("Solution Status :", pulp.LpStatus[model_primal.status])
print("-"*20)
print("Optimal Total Cost =", pulp.value(model_primal.objective),"euros")

