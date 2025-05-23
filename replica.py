import numpy as np
import random
import matplotlib.pyplot as plt


#Clases 

class Semaforo:
    def __init__(self, longitud_gen=48):
        self.genotipo = [random.choice(['r', 'v']) for _ in range(longitud_gen)]


class Individuo:
    def __init__(self):
        self.semaforos = [Semaforo() for _ in range(4)]  
        self.objetivo = None  
        self.esperas = (0, 0)  
        

class Simulador:
    def __init__(self, tiempo_simulacion=480, vehiculos_por_via=96, num_vias=4):
        self.tiempo_simulacion = tiempo_simulacion
        self.vehiculos_por_via = vehiculos_por_via
        self.num_vias = num_vias
        self.vehiculos_entrados = vehiculos_por_via * num_vias

    def simular(self, individuo):
        vehiculos_salieron = 0
        tiempo_espera_total = 0
        max_tiempo_espera = 0
        vehiculos_esperando = {i: 0 for i in range(self.num_vias)}

        for t in range(self.tiempo_simulacion):
            for i in range(self.num_vias):
                semaforo = individuo.semaforos[i]
                estado = semaforo.genotipo[t // 10]

                if estado == 'v' and vehiculos_esperando[i] > 0:
                    vehiculos_esperando[i] -= 1
                    vehiculos_salieron += 1
                    tiempo_espera_total += t
                    max_tiempo_espera = max(max_tiempo_espera, t)
                elif estado == 'r':
                    vehiculos_esperando[i] += 1

        return {
            'T': self.vehiculos_entrados,
            'M': vehiculos_salieron,
            'E': tiempo_espera_total,
            'ME': max_tiempo_espera
        }
        
        
#Funciones 
 
def seleccion(poblacion, n_seleccionados=50):
    poblacion.sort(key=lambda x: x.objetivo, reverse=False)  # menor el fitness = mejor la solucion
    return poblacion[:n_seleccionados]

def cruce(padre1, padre2):
    punto_corte = random.randint(0, len(padre1.semaforos) - 1)
    hijo1 = Individuo()
    hijo2 = Individuo()
    hijo1.semaforos = padre1.semaforos[:punto_corte] + padre2.semaforos[punto_corte:]
    hijo2.semaforos = padre2.semaforos[:punto_corte] + padre1.semaforos[punto_corte:]
    return hijo1, hijo2

def mutacion(individuo, probabilidad_mutacion=0.2):
    for semaforo in individuo.semaforos:
        if random.random() < probabilidad_mutacion:
            idx_mutar = random.randint(0, len(semaforo.genotipo) - 1)
            semaforo.genotipo[idx_mutar] = 'v' if semaforo.genotipo[idx_mutar] == 'r' else 'r'

def generar_nueva_generacion(poblacion):
    seleccionados = seleccion(poblacion)
    nueva_poblacion = seleccionados[:]
    while len(nueva_poblacion) < len(poblacion):
        padre1, padre2 = random.sample(seleccionados, 2)
        hijo1, hijo2 = cruce(padre1, padre2)
        mutacion(hijo1)
        mutacion(hijo2)
        nueva_poblacion.extend([hijo1, hijo2])
    return nueva_poblacion[:len(poblacion)]



#main 

simulador = Simulador()


tam_poblacion = 100
max_generaciones = 50


poblacion = [Individuo() for _ in range(tam_poblacion)]


mejores_fitness = []
promedio_fitness = []
tiempos_espera_promedio = []

for gen in range(max_generaciones):
    for individuo in poblacion:
        resultados = simulador.simular(individuo)
        T = resultados['T']
        M = resultados['M']
        E = resultados['E']
        ME = resultados['ME']

     
        fitness = 0.95 * (T / M) + 0.0009 * (E / T) + 0.00004 * ME if M > 0 else float('inf')
        individuo.objetivo = fitness
        individuo.esperas = (E, ME)

    fitness_valores = [ind.objetivo for ind in poblacion if ind.objetivo != float('inf')]
    esperas_promedio = [ind.esperas[0] / simulador.vehiculos_entrados for ind in poblacion if ind.objetivo != float('inf')]

    mejores_fitness.append(min(fitness_valores))  
    promedio_fitness.append(sum(fitness_valores) / len(fitness_valores))
    tiempos_espera_promedio.append(sum(esperas_promedio) / len(esperas_promedio))

    poblacion = generar_nueva_generacion(poblacion)

    print(f"Generación {gen + 1}/{max_generaciones} - Mejor fitness: {mejores_fitness[-1]}")


#1 Chart
plt.figure(figsize=(10, 5))
plt.plot(range(max_generaciones), mejores_fitness, label="Mejor solución", linewidth=2, color='blue')
plt.plot(range(max_generaciones), promedio_fitness, label="Promedio de población", linewidth=2, linestyle='--', color='orange')
plt.title("Evolución del Grado de Adaptación")
plt.xlabel("Generación")
plt.ylabel("Fitness")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#2 Chart
plt.figure(figsize=(10, 5))
plt.plot(range(max_generaciones), tiempos_espera_promedio, label="Promedio tiempo de espera", color='green', linewidth=2)
plt.title("Promedio del Tiempo de Espera por Generación")
plt.xlabel("Generación")
plt.ylabel("Tiempo promedio de espera (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
