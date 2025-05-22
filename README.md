# ProyectoFinal_IC_BBBC
# Optimización de Flujo Vehicular con MGP-BBBC

Este proyecto implementa una simulación de tráfico y una metaheurística llamada **MGP-BBBC (Multiple Global Peaks Big Bang–Big Crunch)** para optimizar la secuencia de luces de semáforos en una intersección simulada.

## Objetivo

Minimizar la congestión y los tiempos de espera vehiculares mediante la búsqueda de configuraciones óptimas de semáforos en un entorno simulado.

---

## ¿Qué mide la función de fitness?

La función de fitness usada es:

```
Fitness(S) = 0.95 * (1 - M/T) + 0.0009 * E + 0.00004 * ME
```

Donde:
- **T**: Total de vehículos que ingresaron.
- **M**: Total de vehículos que salieron exitosamente.
- **E**: Tiempo total de espera acumulado.
- **ME**: Mayor tiempo de espera individual.

### Interpretación:
- `(1 - M/T)` penaliza los vehículos que **no pudieron salir**.
- `E` penaliza el **tiempo total de espera** del tráfico.
- `ME` penaliza casos extremos donde un vehículo espera demasiado tiempo.

---

## ¿Por qué se minimiza el fitness?

Un menor valor de fitness indica:
- **Mayor eficiencia en el flujo** (más vehículos logran salir).
- **Menor acumulación de espera**.
- **Menor tiempo máximo atrapado por un vehículo**.

Por lo tanto, la meta del algoritmo es **minimizar el fitness** para encontrar la mejor solución posible.

---

## Visualizaciones incluidas

- Evolución del mejor fitness por generación
- Comparación entre ejecuciones
- Distribución del fitness por generación (boxplot)

---

## Requisitos

Instala las dependencias con:

```
pip install -r requirements.txt
```

---

## Ejecución

- **Replicacion:** 
- **Optimizacion:** python main.py


