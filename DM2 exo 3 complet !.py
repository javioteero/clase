
import pulp
import random

#DATA
liste_noeuds = list(range(20))
liste_produits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# COLLER ARC EXO 2
liste_arcs_tuples = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (6, 11), (5, 13), (7, 14), (1, 6), (8, 15), (3, 5), (11, 17), (9, 16), (2, 10), (4, 7), (5, 15), (11, 18), (9, 12), (3, 18), (17, 19), (10, 16), (7, 11), (6, 9), (2, 16), (3, 6), (5, 16), (10, 15), (12, 15), (16, 19), (4, 19), (3, 12), (14, 16), (9, 13), (11, 14), (8, 17), (13, 17), (4, 10), (13, 18), (12, 17), (8, 14), (16, 18), (2, 7), (5, 7), (1, 5), (11, 13), (7, 15), (3, 10), (1, 3), (8, 13), (7, 9), (2, 8), (2, 12), (10, 14), (8, 11), (15, 19), (12, 14), (13, 19), (1, 16), (12, 16), (11, 16), (6, 8), (7, 13), (4, 8), (3, 13), (1, 10), (15, 17), (14, 19), (3, 16), (4, 9), (9, 19), (6, 15), (6, 12), (2, 18), (7, 17)]
# COLLER CV 
Cv = {(0, 1): 8, (1, 2): 24, (2, 3): 27, (3, 4): 28, (4, 5): 25, (5, 6): 23, (6, 7): 12, (7, 8): 26, (8, 9): 28, (9, 10): 18, (10, 11): 12, (11, 12): 25, (12, 13): 20, (13, 14): 10, (14, 15): 10, (15, 16): 26, (16, 17): 25, (17, 18): 5, (18, 19): 26, (6, 11): 6, (5, 13): 8, (7, 14): 21, (1, 6): 6, (8, 15): 26, (3, 5): 25, (11, 17): 5, (9, 16): 6, (2, 10): 26, (4, 7): 9, (5, 15): 12, (11, 18): 23, (9, 12): 14, (3, 18): 25, (17, 19): 17, (10, 16): 24, (7, 11): 10, (6, 9): 10, (2, 16): 13, (3, 6): 30, (5, 16): 28, (10, 15): 14, (12, 15): 9, (16, 19): 11, (4, 19): 10, (3, 12): 24, (14, 16): 29, (9, 13): 25, (11, 14): 26, (8, 17): 12, (13, 17): 13, (4, 10): 10, (13, 18): 29, (12, 17): 26, (8, 14): 29, (16, 18): 10, (2, 7): 28, (5, 7): 13, (1, 5): 17, (11, 13): 28, (7, 15): 14, (3, 10): 28, (1, 3): 17, (8, 13): 27, (7, 9): 16, (2, 8): 6, (2, 12): 6, (10, 14): 7, (8, 11): 15, (15, 19): 7, (12, 14): 20, (13, 19): 16, (1, 16): 15, (12, 16): 11, (11, 16): 5, (6, 8): 22, (7, 13): 21, (4, 8): 20, (3, 13): 14, (1, 10): 28, (15, 17): 21, (14, 19): 14, (3, 16): 18, (4, 9): 30, (9, 19): 6, (6, 15): 10, (6, 12): 26, (2, 18): 12, (7, 17): 29}

dict_origines = {1: 2, 2: 2, 3: 2, 4: 14, 5: 16, 6: 4, 7: 13, 8: 3, 9: 14, 10: 3}
dict_destinations = {1: 14, 2: 17, 3: 9, 4: 16, 5: 19, 6: 17, 7: 17, 8: 15, 9: 17, 10: 12}



# creation of vector y ------------------------------------------------------

y_bar_reseau_ouvert = {}
for arc in liste_arcs_tuples:
    y_bar_reseau_ouvert[arc] = random.choices([0, 1], weights=[0.1, 0.8], k=1)[0]

nb_ouverts = sum(y_bar_reseau_ouvert.values())
print(f"-> {nb_ouverts} arcs ouverts sur {len(liste_arcs_tuples)}")


# PRIMAL ----------------------------------------------------------------------



modele_primal = pulp.LpProblem("PrimalMINI", pulp.LpMinimize)

var_x_flot = pulp.LpVariable.dicts("x_flot", (liste_produits, liste_arcs_tuples), lowBound=0)

modele_primal += pulp.lpSum(Cv[arc] * var_x_flot[p][arc] for p in liste_produits for arc in liste_arcs_tuples)


for p in liste_produits:
    for k in liste_noeuds:
        solde_noeud = 0
        if k == dict_origines[p]:
            solde_noeud = 1  
        elif k == dict_destinations[p]:
            solde_noeud = -1 
        
        flux_sortant = pulp.lpSum(var_x_flot[p][arc] for arc in liste_arcs_tuples if arc[0] == k)
        flux_entrant = pulp.lpSum(var_x_flot[p][arc] for arc in liste_arcs_tuples if arc[1] == k)
        modele_primal += flux_sortant - flux_entrant == solde_noeud

for p in liste_produits:
    for arc in liste_arcs_tuples:

        modele_primal += var_x_flot[p][arc] <= y_bar_reseau_ouvert[arc]



# DUAL ---------------------------------------------------------

modele_dual = pulp.LpProblem("DualMAXI", pulp.LpMaximize)


alpha = pulp.LpVariable.dicts("pi_noeud", (liste_produits, liste_noeuds)) 
beta = pulp.LpVariable.dicts("lambda_arc", (liste_produits, liste_arcs_tuples), upBound=0)


partie_obj_1 = pulp.lpSum(alpha[p][dict_origines[p]] - alpha[p][dict_destinations[p]] 
                         for p in liste_produits)
partie_obj_2 = pulp.lpSum(y_bar_reseau_ouvert[arc] * beta[p][arc] 
                         for p in liste_produits 
                         for arc in liste_arcs_tuples)
modele_dual += partie_obj_1 + partie_obj_2



for p in liste_produits:
    for arc in liste_arcs_tuples:
        i, j = arc 
        modele_dual += (alpha[p][i] - alpha[p][j] + beta[p][arc] <= Cv[arc],
                      f"Contrainte_Dual_p{p}_arc{arc}")

print("Modèle Dual construit.")





modele_primal.solve()
statut_primal = pulp.LpStatus[modele_primal.status]
obj_primal = pulp.value(modele_primal.objective) if statut_primal == 'Optimal' else None

modele_dual.solve()
statut_dual = pulp.LpStatus[modele_dual.status]
obj_dual = pulp.value(modele_dual.objective) if statut_dual == 'Optimal' else None

# --- Affichage et Comparaison ---
print("\n")
print("=" * 40)
print("--- COMPARAISON PRIMAL / DUAL ---")
print(f"Statut Primal : {statut_primal}")
print(f"Statut Dual   : {statut_dual}")
print("-" * 40)
print(f"Objectif Primal (Coût Min) : {obj_primal}")
print(f"Objectif Dual (Valeur Max) : {obj_dual}")
print("-" * 40)

