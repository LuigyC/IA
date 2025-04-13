# clustering_estaciones.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# -------------------------------
# Cargar el Dataset y Preprocesamiento
# -------------------------------
# Leer el dataset previamente generado
dataset_estaciones = pd.read_csv("dataset_estaciones.csv")
print("Primeras filas del dataset:")
print(dataset_estaciones.head())

# Seleccionar variables relevantes para el clustering
variables = ['x', 'y', 'conexiones', 'tiempo_espera', 'flujo_pasajeros']
datos = dataset_estaciones[variables]

# Estandarizar los datos
scaler = StandardScaler()
datos_scaled = scaler.fit_transform(datos)

# -------------------------------
# Determinar el Número Óptimo de Clusters: Método del Codo
# -------------------------------
inercia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(datos_scaled)
    inercia.append(kmeans.inertia_)

# Graficar el Método del Codo
plt.figure(figsize=(8, 6))
plt.plot(k_range, inercia, marker='o')
plt.xlabel("Número de Clusters (k)")
plt.ylabel("Inercia")
plt.title("Método del Codo para determinar el número óptimo de clusters")
plt.grid(True)
plt.show()

# -------------------------------
# Aplicar K-Means con el Número Óptimo Identificado (ejemplo: k = 3)
# -------------------------------
k_optimo = 3
kmeans_final = KMeans(n_clusters=k_optimo, random_state=42)
clusters = kmeans_final.fit_predict(datos_scaled)
dataset_estaciones['cluster'] = clusters

# Resumen estadístico por cluster
print("\nResumen de clusters:")
print(dataset_estaciones.groupby('cluster').mean())

# -------------------------------
# Visualizar los Clusters
# -------------------------------
plt.figure(figsize=(8, 6))
for cluster in range(k_optimo):
    subset = dataset_estaciones[dataset_estaciones['cluster'] == cluster]
    plt.scatter(subset['x'], subset['y'], label=f'Cluster {cluster}', alpha=0.7, edgecolor='k')
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.title("Clusters de Estaciones en el Sistema de Transporte")
plt.legend()
plt.grid(True)
plt.show()

# Guardar el dataset con la asignación de clusters
dataset_estaciones.to_csv("dataset_estaciones_cluster.csv", index=False)
print("Dataset con clusters guardado como 'dataset_estaciones_cluster.csv'.")
