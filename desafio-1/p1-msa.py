# -*- coding: utf-8 -*-
"""
Created on 01/03/2017

@author: Perez Ernesto Rafael
"""
import hashlib
from time import time


def my_func(r, n):
    dicc = {}
    dicc_valores = {}
    tiempo_inicial = time()
    uno = False
    posicion_equivalente = 9999999
    for i in xrange(9999999):
        if dicc.get(r[:9], 0) != 0:
            if uno == False:
                dist = (i - dicc.get(r[:9], 0))
                uno = True
                posicion_equivalente = inferir(i - 1, dist, n)
        if i == posicion_equivalente + 1:
            print 'my_func("00000000000000000000000000000000", 2017201720172017) =', dicc_valores.get(
                posicion_equivalente)
            break
        else:
            dicc[r[:9]] = i
            dicc_valores[i] = r
        r = hashlib.md5(r[:9]).hexdigest()
    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print 'El tiempo de ejecucion fue:', tiempo_ejecucion
    return r


def inferir(i, dist, n):
    intervalo_repeticion = n - i
    desp = intervalo_repeticion % dist
    posicion_equivalente = i + desp
    return posicion_equivalente


my_func("000000000", 2017201720172017)  # solo necesito 9
