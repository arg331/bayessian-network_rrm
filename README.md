# Fault Tree Analysis & Bayesian Networks

This project is a basic implementation of **Fault Tree Analysis** and **Bayesian Networks** using Python. The main purpose is to test, comprehend, and simulate probabilistic scenarios using the `pyAgruM` library. (**Also starting to comprehend Python**)

## Problems Solved

### Problem 1: Web Server Attack Scenario (In spanish)
Un servidor web recibe cada hora una media de 1000 peticiones HTTP, de las cuales se estima que 200 son **ataques**. Se estima que el 50 % de los ataques pueden suponer **un fallo grave** para la integridad del sistema. Se instala un **cortafuegos** que, según especificaciones del fabricante, no conseguirá bloquear 1 de cada 4 ataques. Además, dicho cortafuegos se **actualizará** una vez cada hora, lo cual tardará 6 minutos y durante este tiempo no estará activo. Por otro lado, se instalará un **sistema de recuperación** *que estará en funcionamiento el 85 % del tiempo* y que evitará la mitad de los fallos graves.

### Problem 2: Server Fault Tree Analysis (In spanish)
El servidor de una organización deja de funcionar cuando ocurre una avería en al menos uno de los siguientes componentes: tarjeta de red, sistema de almacenamiento o procesador. El servidor dispone de dos procesadores (redundancia), de modo que la avería de uno no interrumpe el servicio. El sistema de almacenamiento cuenta con tres discos duros redundantes. Los tiempos de vida están modelados por distribuciones exponenciales (tarjeta y procesadores) y Weibull (discos).

**Result:** Probability of server failure in 1 year: **0.1055%** (highly reliable due to redundancy)

## Implementation Details

- **Bottom-Up probability propagation** through fault tree
- **AND/OR logic gates** for component failures
- **Exponential and Weibull distributions** for component lifetimes
- **Bayesian Network transformation** using pyAgruM

## Key Functions

- `propagacion()` - Bottom-up probability propagation
- `nodos()` - List all child nodes
- `eventos()` - List all event nodes
- `evento_info()` - Get node type and children
- `transformar()` - Transform fault tree to Bayesian Network

## References

**The pyAgrum bibliography ->** *pyagrum.gitlab.io/reference/*

*Made by a software preEngineer from University of Almería* 

**Last updated:** December 27, 2025