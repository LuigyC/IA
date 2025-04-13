
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# -------------------------------
# Configuración Inicial y Generación del Dataset Sintético
# -------------------------------
np.random.seed(42)  # Para reproducibilidad

# Definir el número de muestras (datos)
num_samples = 200

# Generar variables predictoras:
# Distancia (en km) entre estaciones
distancia = np.random.uniform(1, 20, num_samples)
# Número de conexiones (entre 1 y 5)
conexiones = np.random.randint(1, 6, num_samples)
# Hora del día (6 a 21 hrs, representada de forma numérica)
hora = np.random.randint(6, 22, num_samples)

# Generar la variable objetivo: tiempo de viaje en minutos
# Se define una relación lineal con las variables predictoras y se añade ruido
tiempo_viaje = 2.5 * distancia + 5 * conexiones + np.random.normal(0, 3, num_samples)

# Crear un DataFrame con los datos generados
datos = pd.DataFrame({
    'distancia': distancia,
    'conexiones': conexiones,
    'hora': hora,
    'tiempo_viaje': tiempo_viaje
})

# Guardar el dataset en formato CSV para futuros analisis
datos.to_csv("dataset_supervisado.csv", index=False)
print("Dataset supervisado generado y guardado como 'dataset_supervisado.csv'.")

# -------------------------------
# División del Dataset: Entrenamiento y Prueba
# -------------------------------
X = datos[['distancia', 'conexiones', 'hora']]
y = datos['tiempo_viaje']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# Entrenamiento del Modelo Supervisado: Regresión Lineal
# -------------------------------
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Predicciones sobre el conjunto de prueba
y_pred = modelo.predict(X_test)

# -------------------------------
# Evaluación del Modelo
# -------------------------------
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Error Absoluto Medio (MAE):", mae)
print("Error Cuadratico Medio (MSE):", mse)

# -------------------------------
# Visualización: Comparación entre Valores Reales y Predichos
# -------------------------------
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Tiempo de Viaje Real (min)')
plt.ylabel('Tiempo de Viaje Predicho (min)')
plt.title('Comparación entre Tiempo de Viaje Real y Predicho')
plt.grid(True)
plt.show()
