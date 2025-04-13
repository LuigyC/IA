# generar_dataset.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# -------------------------------
# Configuración Inicial y Generación de Datos Sintéticos
# -------------------------------
np.random.seed(42)  # Para reproducibilidad

# Definir número de estaciones que simularán la red de transporte
num_estaciones = 50

# Generar coordenadas (x, y) aleatorias que simulan la ubicación de cada estación
x = np.random.uniform(0, 100, num_estaciones)
y = np.random.uniform(0, 100, num_estaciones)

# Generar el número de conexiones: entre 1 y 10
conexiones = np.random.randint(1, 11, num_estaciones)

# Generar tiempo promedio de espera (minutos): simula variabilidad operacional
tiempo_espera = np.random.uniform(2, 15, num_estaciones)

# Simular el flujo de pasajeros (usuarios por hora)
flujo_pasajeros = np.random.randint(50, 500, num_estaciones)

# Crear el DataFrame final
dataset_estaciones = pd.DataFrame({
    'x': x,
    'y': y,
    'conexiones': conexiones,
    'tiempo_espera': tiempo_espera,
    'flujo_pasajeros': flujo_pasajeros
})

# Guardar el dataset en formato CSV
dataset_estaciones.to_csv("dataset_estaciones.csv", index=False)
print("Dataset generado y guardado como 'dataset_estaciones.csv'.")

# Visualización: Distribución espacial de las estaciones
plt.figure(figsize=(8, 6))
plt.scatter(dataset_estaciones['x'], dataset_estaciones['y'], alpha=0.7)
plt.title('Distribución de Estaciones en el Plano')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.grid(True)
plt.show()
