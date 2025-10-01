# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 13:17:34 2025

@author: otero
"""

#%% Ejercicio 1

calificaciones = [4, 9, 6, 8, 7, 10, 3, 5, 8, 9]


#calificaciones_altas = [x for x in calificaciones if x>=8]
#print(calificaciones_altas)


minimo = float(input("Dame un valor mínimo: "))

def contar_calificaciones(lista, minimo):
    return len([x for x in lista if x > minimo])


print(contar_calificaciones(calificaciones, minimo))

#%% Ejercicio dataframe

import pandas as pd

