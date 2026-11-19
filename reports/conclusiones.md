# Conclusiones del Proyecto

Resultados obtenidos sobre el conjunto de prueba (25 % de los datos, `random_state=42`) a partir del dataset de Inside Airbnb Buenos Aires (extracción de septiembre de 2026). Todos los valores monetarios se expresan en pesos argentinos ($ ARS).

---

## Tabla Comparativa de Rendimiento

| Modelo / Enfoque | MAE ($ ARS) | RMSE ($ ARS) | R² |
| :--- | :---: | :---: | :---: |
| **Ej. 3: Regresión Lineal (number_of_reviews)** | **57.809,62** | **92.849,61** | **0,0001** |
| *Ej. 3: Baseline (predicción de la media)* | *57.818,16* | *92.855,47* | *-0,0000* |
| **Ej. 6: k-NN (k = 15, weights="distance")** | **49.440,98** | **80.753,06** | **0,1921** |
| *Ej. 6: Baseline (predicción de la media)* | *56.735,63* | *89.883,16* | *-0,0009* |

---

## Ejercicio 3: Cantidad de Reseñas y Precio

- **Ajuste del modelo:** Se ajustó una regresión lineal simple con `number_of_reviews` como único predictor y `price_num` como variable objetivo tras recortar los extremos [p1, p99] (27.086 observaciones).
- **Parámetros estimados:**
  - Intercepto ($\beta_0$): **$130.347,45 ARS**
  - Pendiente ($\beta_1$): **-7,16 ARS** por reseña acumulada.
- **Predicción para 50 reseñas:** **$129.989,48 ARS**, prácticamente indistinguible del valor medio de los alquileres (~$130.000 ARS).
- **Interpretación y Hallazgo:**
  - El coeficiente de determinación $R^2 = 0,0001$ demuestra que la cantidad de reseñas explica menos del 0,01 % de la variabilidad del precio.
  - La métrica de error (RMSE $92.849,61) es idéntica a la del modelo ingenuo o baseline que predice constantemente la media (RMSE $92.855,47).
  - **Conclusión técnica:** La cantidad de reseñas no sirve, por sí sola, como predictor del precio nocturno. Además, debe recordarse que correlación no implica causalidad: acumular comentarios no altera el valor del inmueble ni justifica una tarifa diferente.

---

## Ejercicio 6: Estimación con k-NN y Selección de k

- **Metodología:** Se evaluaron los valores $k \in \{3, 5, 7, 9, 11, 15\}$ mediante validación cruzada con 5 pliegues (`cross_val_score`, métrica RMSE) sobre el 75 % de entrenamiento (19.949 observaciones), utilizando `StandardScaler` y `KNeighborsRegressor` con ponderación por distancia (`weights="distance"`).
- **Resultados de Validación Cruzada:**
  - $k = 3$: RMSE = $90.463,63 ARS
  - $k = 5$: RMSE = $87.297,92 ARS
  - $k = 7$: RMSE = $86.123,09 ARS
  - $k = 9$: RMSE = $85.439,58 ARS
  - $k = 11$: RMSE = $84.894,88 ARS
  - **$k = 15$:** **RMSE = $84.456,45 ARS** (menor error de validación)
- **Evaluación en Prueba (k = 15, weights="distance"):**
  - **MAE:** $49.440,98 ARS
  - **RMSE:** $80.753,06 ARS
  - **$R^2$:** **0,1921**
- **Impacto de `weights="distance"`:**
  - Ponderar por la inversa de la distancia euclidiana ($w_i = 1 / d_i$) permite que aquellos anuncios vecinos estructuralmente más cercanos tengan un peso prioritario en la predicción.
  - El modelo supera netamente al baseline (reducción de RMSE de $89.883 a $80.753 ARS, pasando de $R^2 = 0$ a $R^2 \approx 0,192$).
- **Estimación puntual:** Para el primer anuncio del conjunto de prueba (5 huéspedes, 3 dormitorios, 4 camas, 45 noches mínimas, 0 reseñas), el modelo estimó **$157.077,61 ARS** frente a un valor real de **$238.143,09 ARS** (diferencia de $81.065,48 ARS).
- **Conclusión técnica:** Las variables físicas del alojamiento (`accommodates`, `bedrooms`, `beds`) aportan información sustancial respecto al tamaño y capacidad, capturando casi un 20 % de la varianza. Para alcanzar capacidades predictivas superiores se requiere incorporar variables de localización geográfica (barrio, latitud/longitud) y tipología de la propiedad (*entire home* vs *private room*).
