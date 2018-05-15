# work
desafio-1:
Desafío para desarrolladores!
Si te interesa participar postulate a la búqueda. Por favor no olvides comentar cuál fue tu razonamiento para llegar al resultado.
El ejercicio es para resolver de forma individual, cualquier duda que tengas podrás enviarla posteriormente por email.
=====================================================
Considerando la siguiente función python:
def my_func(r, n):
for i in xrange(n): r = hashlib.md5(r[:9]).hexdigest()
return r
calcular el valor de:
my_func("00000000000000000000000000000000", 2017201720172017)
Algunos ejemplos concretos de la función:
my_func("00000000000000000000000000000000", 0) = 4c93008615c2d041e33ebac605d14b5b
my_func("00000000000000000000000000000000", 1) = c6246d2a39695fb74971b09ced30874f
my_func("00000000000000000000000000000000", 2) = 5e1c33543fbcd9dad6a3f8c07887b8d2
my_func("c6246d2a39695fb74971b09ced30874f", 0) = 5e1c33543fbcd9dad6a3f8c07887b8d2
my_func("00000000000000000000000000000000", 2017) = bc107c24b44b5a518b4286ed7e5a1bb3
=====================================================


"""Caso de uso practico: desconocida la palabra original, pero conociendo la llave generada por la misma, se aplica colisión de hash, para detectar el ciclo en el cual, en  la iteración 'n' se vuelve a obtener la llave generada por la palabra desconocida, entonces la llave hallada en la iteración "n-1" será equivalente a la palabra desconocida, ya que al ingresarla al sistema genera la misma llave que genera la palabra desconocida.
"""


