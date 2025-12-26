import pyagrum as agrum

# ==========================================
# 1. Configuración de la Red y Nodos
# ==========================================

bn = agrum.BayesNet("redPrincipal")

# --- Nodos Raíz ---
ataque = agrum.LabelizedVariable("ataque", "Ataque al Sistema", 2)
ataque.changeLabel(0, "No hay ataque")
ataque.changeLabel(1, "Hay ataque") 
bn.add(ataque) 

cortafuegosDisponible = agrum.LabelizedVariable("cortafuegosDisponible", "Disponibilidad del Cortafuegos", 2)
cortafuegosDisponible.changeLabel(0, "No disponible")
cortafuegosDisponible.changeLabel(1, "Disponible")
bn.add(cortafuegosDisponible)

sistemaRecuperacionDisponible = agrum.LabelizedVariable("sistemaRecuperacionDisponible", "Disponibilidad Sist. Recuperación", 2)
sistemaRecuperacionDisponible.changeLabel(0, "No disponible")
sistemaRecuperacionDisponible.changeLabel(1, "Disponible")
bn.add(sistemaRecuperacionDisponible)

# --- Nodos Intermedios y Finales ---
exitoCortafuegos = agrum.LabelizedVariable("exitoCortafuegos", "Eficacia del Cortafuegos", 2)
exitoCortafuegos.changeLabel(0, "No mitiga el ataque")
exitoCortafuegos.changeLabel(1, "Mitiga el ataque")
bn.add(exitoCortafuegos)

exitoSistemaRecuperacion = agrum.LabelizedVariable("exitoSistemaRecuperacion", "Eficacia de Recuperación", 2)
exitoSistemaRecuperacion.changeLabel(0, "Recuperación fallida")
exitoSistemaRecuperacion.changeLabel(1, "Recuperación exitosa") 
bn.add(exitoSistemaRecuperacion)

falloGrave = agrum.LabelizedVariable("falloGrave", "Estado Crítico del Sistema", 2)
falloGrave.changeLabel(0, "Sistema estable")
falloGrave.changeLabel(1, "Fallo crítico") 
bn.add(falloGrave)


# ==========================================
# 2. Definición de Topología (Arcos)
# ==========================================

bn.addArc("ataque", "exitoCortafuegos")
bn.addArc("cortafuegosDisponible", "exitoCortafuegos")
bn.addArc("sistemaRecuperacionDisponible", "exitoSistemaRecuperacion")
bn.addArc("exitoCortafuegos", "falloGrave")
bn.addArc("exitoSistemaRecuperacion", "falloGrave")


# ==========================================
# 3. Tablas de Probabilidad (SOLUCIÓN ROBUSTA)
# ==========================================

# --- A. Nodos Raíz (Estos sí aceptan listas simples porque no tienen padres) ---
bn.cpt("ataque")[:] = [0.8, 0.2] 
bn.cpt("cortafuegosDisponible")[:] = [0.1, 0.9]
bn.cpt("sistemaRecuperacionDisponible")[:] = [0.15, 0.85]


# --- B. Éxito Cortafuegos (Usamos Diccionario para evitar error de Shape) ---
# Caso 1: Sin ataque, Sin cortafuegos
bn.cpt("exitoCortafuegos")[{'ataque': 0, 'cortafuegosDisponible': 0}] = [0.99, 0.01]
# Caso 2: Sin ataque, Con cortafuegos
bn.cpt("exitoCortafuegos")[{'ataque': 0, 'cortafuegosDisponible': 1}] = [0.99, 0.01]
# Caso 3: Ataque SI, Cortafuegos NO
bn.cpt("exitoCortafuegos")[{'ataque': 1, 'cortafuegosDisponible': 0}] = [0.80, 0.20]
# Caso 4: Ataque SI, Cortafuegos SI
bn.cpt("exitoCortafuegos")[{'ataque': 1, 'cortafuegosDisponible': 1}] = [0.10, 0.90]


# --- C. Éxito Recuperación (Aquí estaba tu error reciente) ---
# Al usar diccionario, le decimos explícitamente qué fila rellenar.
# Caso Padre=0 (No disponible)
bn.cpt("exitoSistemaRecuperacion")[{'sistemaRecuperacionDisponible': 0}] = [0.99, 0.01]
# Caso Padre=1 (Disponible)
bn.cpt("exitoSistemaRecuperacion")[{'sistemaRecuperacionDisponible': 1}] = [0.05, 0.95]


# --- D. Fallo Grave (También con diccionario) ---
# Caso 1: Ambos fallan
bn.cpt("falloGrave")[{'exitoCortafuegos': 0, 'exitoSistemaRecuperacion': 0}] = [0.01, 0.99]
# Caso 2: Cortafuegos falla, Recuperación ok
bn.cpt("falloGrave")[{'exitoCortafuegos': 0, 'exitoSistemaRecuperacion': 1}] = [0.95, 0.05]
# Caso 3: Cortafuegos ok, Recuperación falla
bn.cpt("falloGrave")[{'exitoCortafuegos': 1, 'exitoSistemaRecuperacion': 0}] = [0.99, 0.01]
# Caso 4: Ambos ok
bn.cpt("falloGrave")[{'exitoCortafuegos': 1, 'exitoSistemaRecuperacion': 1}] = [0.99, 0.01]


# ==========================================
# 4. Verificación
# ==========================================
print("--- Red Bayesiana compilada sin errores de dimensiones ---")
print(f"Nodos: {bn.size()}")
print("\nMatriz de probabilidad para 'Fallo Grave':")
print(bn.cpt("falloGrave"))