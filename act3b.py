from pyagrum import BayesNet

# Normalmente usaríamos una librería como 'agrum' para redes bayesianas,
# pero aquí implementaremos una solución simple para el problema planteado.
#Nodos Hoja 
e1 = dict(tipo = "evento" , nombre = "E1" , prob = 0.2 , hijos = [])
e2 = dict(tipo = "evento" , nombre = "E2" , prob = 0.25 , hijos = [])
e3 = dict(tipo = "evento" , nombre = "E3" , prob = 0.3 , hijos = [])
#Nodos Intermedios
e1e2 = dict(tipo = "OR" , nombre = "None" , prob = None, hijos = [e1 , e2])
e4 = dict (tipo = "evento" , nombre = "E4" , prob = None, hijos = [e1e2])
e4e3 = dict (tipo = "AND" , nombre = "None", prob = None, hijos = [e4 , e3])
e5 = dict(tipo = "evento" , nombre = "E5" , prob = 0.4 , hijos = [e4e3])


## Propagación de probabilidades, no retorna nada, modifica el diccionario original 
# He aplicado una estrategia Bottom-Up clásica.
def propagacion(nodo : dict) -> None:
    # Caso base: si no tiene hijos, es hoja
    if not nodo["hijos"]:
        return
    
    # Procesar todos los hijos PRIMERO (recursión dentro del bucle)
    for hijo in nodo["hijos"]:
        propagacion(hijo)  
    
    # Ahora sí calcular después de que los hijos estén listos
    if nodo["tipo"] == "AND":
        nodo["prob"] = 1.0
        for hijo in nodo["hijos"]:
            nodo["prob"] *= hijo["prob"]
    
    elif nodo["tipo"] == "OR":
        complemento = 1.0
        for hijo in nodo["hijos"]:
            complemento *= (1 - hijo["prob"])
        nodo["prob"] = 1 - complemento
    
    elif nodo["tipo"] == "evento" and nodo["hijos"]:
        nodo["prob"] = nodo["hijos"][0]["prob"]



# ==========================================
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_--_-_-_-_-
# ==========================================

## Función para devolver todos los nodos de un árbol
def nodos(nodo : dict) -> list: 
    lista = list()
    for (hijo) in nodo["hijos"]:
        lista.append(hijo["nombre"])
    return lista

## Dado un árbol, devolver una lista con todos los nodos de tipo evento 
def eventos(nodo : dict) -> list: 
    lista = list()
    for hijo in nodo["hijos"]:
        if hijo["tipo"] == "evento": 
            lista.append(hijo["nombre"]) 
    return lista

## Dado un árbol y el nombre el evento de un nodo, devuelva la puerta lógica que esté justo por debajo 
def evento_info(nodo : dict , nombre : str) -> tuple:
    for hijo in nodo["hijos"] : 
        if hijo["nombre"] == nombre : 
            return (hijo["tipo"] , hijo["hijos"])
 
 
 
## Función que transforme el árbol de fallos en una red bayesiana usando pyagrum, hacer inferencia después
##  para comprobar que funciona correctamente  
def transformar(nodo:dict) -> BayesNet:
    # Crear una red bayesiana vacía
    bn = BayesNet()

    # Recorrer todos los nodos del árbol y agregarlos a la red bayesiana
    def agregar_nodo(n: dict):
        # Agregar nodo como variable binaria
        bn.add(n["nombre"])
        
        for hijo in n["hijos"]:
            agregar_nodo(hijo)

    agregar_nodo(nodo)

    # Establecer las relaciones de dependencia entre nodos
    def establecer_relaciones(n: dict):
        if n["tipo"] == "evento":
            pass
        elif n["tipo"] == "AND" or n["tipo"] == "OR":
            for hijo in n["hijos"]:
                bn.addArc(hijo["nombre"], n["nombre"])
            
            for hijo in n["hijos"]:
                establecer_relaciones(hijo)

    establecer_relaciones(nodo)

    return bn

# ==========================================
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_--_-_-_-_-
# ==========================================

import math

# ==========================================
# PROBLEMA 2: ÁRBOL DE FALLOS DEL SERVIDOR
# ==========================================

def prob_exponencial(esperanza, tiempo):
    """Calcula P(fallo en tiempo t) con distribución exponencial"""
    lambda_param = 1 / esperanza
    return 1 - math.exp(-lambda_param * tiempo)

def prob_weibull(alfa, beta, tiempo):
    """Calcula P(fallo en tiempo t) con distribución de Weibull"""
    return 1 - math.exp(-((tiempo / beta) ** alfa))

# Nodos hoja: Tarjeta de red (esperanza = 10 años)
p_tarjeta = prob_exponencial(10, 1)
tarjeta_red = dict(tipo="evento", nombre="Tarjeta_Red", prob=p_tarjeta, hijos=[])

# Nodos hoja: Procesadores (esperanza = 3 años)
p_procesador = prob_exponencial(3, 1)
procesador1 = dict(tipo="evento", nombre="Procesador_1", prob=p_procesador, hijos=[])
procesador2 = dict(tipo="evento", nombre="Procesador_2", prob=p_procesador, hijos=[])

# Puerta OR: Fallo de al menos un procesador
fallo_procesador = dict(tipo="OR", nombre="Fallo_Procesador", prob=None, 
                        hijos=[procesador1, procesador2])

# Nodos hoja: Discos duros (Weibull: alfa=1, beta=3)
p_disco = prob_weibull(1, 3, 1)
disco1 = dict(tipo="evento", nombre="Disco_1", prob=p_disco, hijos=[])
disco2 = dict(tipo="evento", nombre="Disco_2", prob=p_disco, hijos=[])
disco3 = dict(tipo="evento", nombre="Disco_3", prob=p_disco, hijos=[])

# Puerta AND: Sistema almacenamiento falla si fallan los 3 discos
fallo_almacenamiento = dict(tipo="AND", nombre="Fallo_Almacenamiento", prob=None,
                            hijos=[disco1, disco2, disco3])

# Evento TOP: Servidor falla si tarjeta AND almacenamiento AND procesador fallan
servidor_falla = dict(tipo="AND", nombre="Servidor_Falla", prob=None,
                      hijos=[tarjeta_red, fallo_almacenamiento, fallo_procesador])

# Ejecutar propagación
propagacion(servidor_falla)

# Mostrar resultados
print("\n" + "=" * 70)
print("PROBLEMA 2: ARBOL DE FALLOS DEL SERVIDOR")
print("=" * 70)
print(f"\nNodos hijos: {nodos(servidor_falla)}")
print(f"Eventos directos: {eventos(servidor_falla)}")
print(f"\nFallo_Procesador: {evento_info(servidor_falla, 'Fallo_Procesador')[0]}")
print(f"Fallo_Almacenamiento: {evento_info(servidor_falla, 'Fallo_Almacenamiento')[0]}")
print("\nProbabilidades en 1 anio:")
print(f"  Tarjeta de red:          {tarjeta_red['prob']:.6f}")
print(f"  Procesador 1:            {procesador1['prob']:.6f}")
print(f"  Procesador 2:            {procesador2['prob']:.6f}")
print(f"  Disco 1:                 {disco1['prob']:.6f}")
print(f"  Disco 2:                 {disco2['prob']:.6f}")
print(f"  Disco 3:                 {disco3['prob']:.6f}")
print(f"  Fallo procesador (OR):   {fallo_procesador['prob']:.6f}")
print(f"  Fallo almacenamiento (AND): {fallo_almacenamiento['prob']:.6f}")
print(f"  Fallo servidor (AND):    {servidor_falla['prob']:.6f} ({servidor_falla['prob']*100:.4f}%)")

# Transformar a red bayesiana
red_servidor = transformar(servidor_falla)
print(f"\nRed bayesiana: {red_servidor.size()} nodos")
print("=" * 70)