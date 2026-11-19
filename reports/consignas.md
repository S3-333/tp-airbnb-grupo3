# Consignas del Trabajo Práctico

Guía de ejercicios del curso **Python para Ciencia de Datos**.

- **Dataset:** Inside Airbnb Buenos Aires (*Detailed Listings data* - `listings.csv.gz`).
- **Variable objetivo:** Precio por noche (`price`).

---

## Preparación Común

1. Entorno con `pandas`, `numpy`, `matplotlib` y `scikit-learn`.
2. Descarga del archivo comprimido `listings.csv.gz` en `data/raw/`.
3. Verificación de columnas del dataset.
4. Conversión de `price` a variable numérica flotante.
5. Limpieza de valores ausentes en las variables requeridas por cada ejercicio.
6. Filtrado de precios no positivos y recorte justificado de valores atípicos.
7. Partición en 75 % entrenamiento y 25 % prueba con `random_state=42`.
8. Evaluación con MAE, RMSE y R² expresando las unidades monetarias.

---

## Ejercicio 3: Cantidad de Reseñas y Precio

- **Caso:** Comprobar si la cantidad de reseñas acumuladas (`number_of_reviews`) puede emplearse, por sí sola, para estimar el precio nocturno con una relación interpretable.
- **Variables:** `number_of_reviews` (predictor) y `price` (objetivo).
- **Pasos:**
  1. Cargar el dataset y comprobar la presencia de las columnas.
  2. Limpiar ausentes y precios no positivos.
  3. Aplicar y justificar el filtro de extremos.
  4. Partición train/test (75/25, semilla 42).
  5. Inspeccionar la dispersión, entrenar el modelo lineal, evaluar métricas, discutir utilidad (R²) sin confundir correlación con causalidad y estimar el precio para un anuncio con 50 reseñas.
  6. Presentar tabla comparativa real vs predicho y conclusiones.

---

## Ejercicio 6: Selección del Número de Vecinos (k) en k-NN

- **Caso:** Se ha decidido estimar precios buscando alojamientos similares (vecinos más cercanos), pero se desconoce cuántos consultar. Probar varios valores de $k$ y seleccionar el de menor error de validación.
- **Variables:** `accommodates`, `bedrooms`, `beds`, `minimum_nights`, `number_of_reviews` (predictores) y `price` (objetivo).
- **Pasos:**
  1. Cargar el dataset y verificar columnas.
  2. Limpieza de ausentes y precios no positivos.
  3. Recorte justificado de extremos en el precio.
  4. Partición train/test (75/25, semilla 42).
  5. Probar $k \in [3, 5, 7, 9, 11, 15]$ con validación cruzada (5 pliegues) sobre el entrenamiento. Seleccionar el mejor $k$, reevaluar en prueba y graficar $k$ vs RMSE.
  6. Estimar el precio para el primer anuncio del conjunto de prueba.
  7. Presentar tabla comparativa real vs predicho y conclusiones.
