#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
diciembre 2017

@author: Rafael Ernesto Perez

"""

#from numpy import loadtxt, zeros, ones, array, linspace, logspace
#from pylab import scatter, show, title, xlabel, ylabel, plot, contour
import numpy as np
from scipy import optimize
import math,random,os

class RedNeuronal(object):
    def __init__(self):
        #Definimos los parametros generales
        self.numeroNeuronasEntrada = 6
        self.numeroNeuronasSalida = 1
        self.numeroNeuronasEscondidas1 = 6
        self.numeroNeuronasEscondidas2 = 6
        #se definen los pesos de manera aleatoria
        #los pesos w1 estanentre la capa de entrada y la escondida con randn es posible
        # generar una matriz de valores aleatorios
        # entre 0 y 1 de tamao esperado
        #Primerparametros filas seundo columans

        self.W1 = np.random.randn(self.numeroNeuronasEntrada, self.numeroNeuronasEscondidas1)
        #Los pesos w2 estan entre la nerona escondida y la de salida
        self.W2 = np.random.randn(self.numeroNeuronasEscondidas1, self.numeroNeuronasEscondidas2)
        self.W3 = np.random.randn(self.numeroNeuronasEscondidas2, self.numeroNeuronasSalida)


        # X es la matriz de entraada
        # W es la matriz de pesos
        # Z sera el resultado de la actividad neuronal(filas como nerornas oculta tenga ycolumas como ...
    def avanzar(self,x):
        #Entrgaremos muchos parametros en forma de matriz
        #dot permite multiplicar matrices

        #Primero calculamos Z2 (paso a)
        self.Z2 = np.dot(x, self.W1)

        #Calculamos las activacionesde la capa2 (paso b)
        self.A2 = self.sigmoide(self.Z2)

        #Calculamos Z3 (paso c)
        self.Z3 = np.dot(self.A2, self.W2)

        self.A3 = self.sigmoide(self.Z3)

        # Calculamos Z4 (paso c)
        self.Z4 = np.dot(self.A3, self.W3)

        ySombrero = self.sigmoide(self.Z4)

        return ySombrero

    def sigmoide(self, z):
        #Aplica funcion sigmoide sobre una matiz
        return 1 / (1 + np.exp(-z))
    #Es necesariominimizar el coste del error provocado porlos pesos,
    #para esto es necesario corregirlos mediante<<<<<<<el decensodel gradiente
    #para esto es necesario derivr el coso con respecto al peso dC/dN = minimo con ..
    #lo calcularemos de manera separada para los pesos W1 y W2

    #Obtenemos la derivada de la funcion

    def sigmoidePrima(self,z):
        #Gradient of sigmoid
        return np.exp(-z)/((1+np.exp(-z))**2)

    def funcionDeCosto(self, X, y):
        # Compute cost for given X,y(esperado), use weights already stored in class.
        self.ySombrero = self.avanzar(X)
        J = 0.5 * sum((y - self.ySombrero) ** 2)
        return J

    def funcionDeCostoPrima(self, x, y):
        # Compute derivative with respect to W and W2 for a given X and y:
        self.ySombrero = self.avanzar(x)

        #Error en cada uno de los datos evaluados

        E = y - self.ySombrero
        delta3 = np.multiply(-(E), self.sigmoidePrima(self.Z4))
        djdw3 = np.dot(self.A3.T, delta3)


        delta2 = np.dot(delta3, self.W3.T) * self.sigmoidePrima(self.Z3)
        djdw2 = np.dot(self.A2.T, delta2)

        delta1 = np.dot(delta2, self.W2.T) * self.sigmoidePrima(self.Z2)
        djdw1 = np.dot(x.T, delta1)


        return djdw1, djdw2, djdw3

    def obtenerParametros(self):
        #transforma la maices de pesos a un solo vector
        W1_vector = self.W1.ravel()
        W2_vector = self.W2.ravel()
        W3_vector = self.W3.ravel()
        parametros = np.concatenate((W1_vector,W2_vector,W3_vector))
        return parametros

    def setearParametros(self,parametros):
        #El vector obtenido con obtenerParametros, se vuelve a configurar a matrices con el fin de reempar los esos antiguos
        #Se definen los indices del vetor, en el que se encuentra cada uno de los pesos W1,W2,W3

        W1_start = 0
        W1_end = self.numeroNeuronasEntrada * self.numeroNeuronasEscondidas1

        W2_start = W1_end
        W2_end = W1_end + self.numeroNeuronasEscondidas1 * self.numeroNeuronasEscondidas2

        W3_start = W2_end
        W3_end = W2_end + self.numeroNeuronasEscondidas2 * self.numeroNeuronasSalida

        #Se transforman en matrices
        self.W1 = np.reshape(parametros[W1_start:W1_end], (self.numeroNeuronasEntrada , self.numeroNeuronasEscondidas1))
        self.W2 = np.reshape(parametros[W2_start:W2_end], (self.numeroNeuronasEscondidas1 , self.numeroNeuronasEscondidas2))
        self.W3 = np.reshape(parametros[W3_start:W3_end], (self.numeroNeuronasEscondidas2, self.numeroNeuronasSalida))


    def calcularGradientes(self,x,y):
        #se obtienen las derivadas
        djdw1,djdw2,djdw3 = self.funcionDeCostoPrima(x,y)

        #se transforman a vectores
        djdw1_vector = djdw1.ravel()
        djdw2_vector = djdw2.ravel()
        djdw3_vector = djdw3.ravel()

        #se concatenan enun solo vector

        derivadas_vector=np.concatenate((djdw1_vector,djdw2_vector,djdw3_vector))

        return derivadas_vector

    def calcularGradientesNumericos(self,N, x, y):
        parametrosIniciales = N.obtenerParametros()
        resultados_gradiente_numerico =np.zeros(parametrosIniciales.shape)
        perturbaciones_epsilon = np.zeros(parametrosIniciales.shape)
        e = 1e-4

        for p in range(len(parametrosIniciales)):
            #Realizamos la perturbacion solo para el peso con el que se esta trabajando
            perturbaciones_epsilon[p] = e

            #Relizamos la aplicacion sobre lospesos + la perturbacion(solo para el peso p)
            N.setearParametros(parametrosIniciales + perturbaciones_epsilon)

            #Calculamos el costo con  la perturbacion incluida enel peso p
            perdida2 = N.funcionDeCosto(x,y)

            #Repetimos el proceo con - la perturbacion
            N.setearParametros(parametrosIniciales - perturbaciones_epsilon)

            perdida1 = N.funcionDeCosto(x,y)

            #Calculamos el valor del gradiente para esepeso p mediantela derivada deepsilon

            a = (perdida2 - perdida1 / (2*e))

            resultados_gradiente_numerico[p] =a

            #Se regresa a a la pertubacion paraese peso, csa que no afecte a lossiguientes
            perturbaciones_epsilon[p]=0

        #Debido a que esto es con fines de comprobacion
        #Una vez recolectados los valores numericos correctos de gradiente
        #Volvemos  a dejar tal como estaban los vlores de loas pesos de la red neuronal
        N.setearParametros(parametrosIniciales)

        #Retornamos los valores de gradiente que pudimos calcular para poder comparlos

        return resultados_gradiente_numerico


class Entrenador(object):

    def __init__(self,N):
        self.N=N
    def costFunctionWrapper(self,params,X,y):
        #El arreglo unidimensional de pesos ahoras vuelve a tansformar a matricescon setearparmetos
        self.N.setearParametros(params)

        #Sevuelve a obtener el valor de costos con los nuevos pesos configuradospor la funcionde optimizacion
        cost=self.N.funcionDeCosto(X,y)

        #Se calculan los valores derivados de la funcion de costo
        grad = self.N.calcularGradientes(X,y)

        #Se retornan ambos valores
        return cost, grad

    def callbackF(self,params):
        #Con setearParametros volvemos #todo un arreglo unidimensional (los pesos)

        self.N.setearParametros(params)

        #Agregamos a los costos locales los costosde lared neuronal
        self.J.append(self.N.funcionDeCosto(self.X,self.y))
    def train (self,x,y):
        #Nos traemos la informcion proporcionada (x) ylos valores que deberiantener con respecto aesos valores (y)
        self.X=x
        self.y=y

        #Tramsformamos mediante obtener parametros a un arreglo unidimensional todos los pesos de la red
        params0=self.N.obtenerParametros()

        #Creamos un arreglo en el que se guarden los costos
        self.J = []

        #Se configurn las opciones delprocesos de optimizacion el numerode iterciones (maxiter)  y se informa por pantalla el proceso disp
        options ={'maxiter' : 200, 'disp' : True}

        #minimize es la funcion que nospermite minimizar el valor de los cosos obenidos eb la red, preso es necesario entregarle una funcion que permita reordenar
        #los valores de los nuevos pesos a matrices y que vuelvaa obtener elcosto de estos nuevospesos
        #los pesos en cuestion para que puedan se modificados, decirle si es que eutiizada el jacobiano, el metodo en vuestion los valors a omparar
        #las opciones de funcionamiento definidas arriba, ypor ultimouna funcion iterativa
        _res = optimize.minimize(self.costFunctionWrapper, params0,jac=True,method='BFGS',args=(x,y),options=options,callback=self.callbackF)
        self.N.setearParametros(_res.x)
        self.optimizarResults=_res

########################### PRUEBA CONSTRUCTOR #################################
#Realizamos una nstanciae la red neuronal
if __name__ == "__main__":
    redNeuronal = RedNeuronal()

    #Comprobamos los valores de los pesos 1
    print ( "Valores de los pesos W1")
    input(redNeuronal.W1)

    #Comprobamos los  valores de los pesos 2
    print ( "Los valores de los pesos W2")
    input(redNeuronal.W2)

    #Comprobamos los valores de los pesos 3
    print ( "Los valores de los pesos W3")
    input(redNeuronal.W3)

    #################PRUEBA DE PROPAGACION ############################


    X = np.array(([2,3,4,5],[5,1,2,6],[10,2,1,6],[6,7,2,4]), dtype=float)
    # Anos de vida restante
    resultados = np.array(([75],[82],[93],[70]), dtype=float)
    X = X / 24
    resultados = resultados / 100
    print ( "Valores delas entradas X sin normalizar")
    input(X)
    print ( "Valores de los resultados esperados sin normalizar")
    input(resultados)

    #Normalizcion de lo valores

    #Consiedando que el maximo puede ser 24 horas
    #Coniderndo que el maximo de anosdevidarestante son 100


    print ( "Valores de las entradas X normalizadas")
    input(X)
    print ( "Valores deos resultados esperados normalizados")
    input(resultados)

    print ( "La prediccion de la red neuronal es")
    input(redNeuronal.avanzar(X))

    ################## Cost Funcion ################

    print ( "Valores de la funcion costo son")
    input(redNeuronal.funcionDeCosto(X,resultados))

    ##################### Backpropagation ################
    print ( "Los valores de la derivada son")
    a,b,c =redNeuronal.funcionDeCostoPrima(X,resultados)

    print ( "La primera derivada es")
    input(a)

    print ( "La segunda derivada es")
    input(b)

    print ( "La tercera derivada es")
    input(c)

    ################# Test gradient numbers ########################
    print ( "El vector con todos los pesos es")
    input(redNeuronal.obtenerParametros())

    print ( "El vector con todas las drivadas es ")
    input(redNeuronal.calcularGradientes(X,resultados))

    print ( "Los valores numericos de los gradientes son ")
    input(redNeuronal.calcularGradientesNumericos(redNeuronal,X,resultados))
    ####################### Training ##########################################

    entrenador = Entrenador(redNeuronal)
    entrenador.train(X,resultados)
    input(redNeuronal.avanzar(X))



############################Overfitting##################

