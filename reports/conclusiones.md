# Conclusiones del Proyecto

Resultados obtenidos sobre el conjunto de prueba (25 % de los datos, `random_state=42`) a partir del dataset de Inside Airbnb Buenos Aires (extracción de septiembre de 2026). Todos los valores monetarios se expresan en pesos argentinos (**$ ARS**).

---

## Resumen Ejecutivo

- El modelo **k‑NN** (k = 15, `weights="distance"`) alcanza **R² ≈ 0,192** y reduce el RMSE respecto al baseline en casi 10 000 ARS.
- La regresión lineal con `number_of_reviews` como único predictor no mejora el baseline (R² ≈ 0,0001).
- Las variables del anuncio (capacidad, dormitorios, camas, noches mínimas y reseñas) son útiles para **aproximar** el precio, pero no explican la mayor parte de su variabilidad.

---

## Tabla comparativa de rendimiento

| Modelo / Enfoque | MAE ($ ARS) | RMSE ($ ARS) | R² |
| :--- | ---: | ---: | ---: |
| **Ej. 3:** Regresión lineal (number_of_reviews) | *57 809,62* | *92 849,61* | *0,0001* |
| Ej. 3: Baseline (predicción de la media) | 57 818,16 | 92 855,47 | -0,0000 |
| **Ej. 6:** k‑NN (k = 15, `weights="distance"`) | *49 440,98* | *80 753,06* | *0,1921* |
| Ej. 6: Baseline (predicción de la media) | 56 735,63 | 89 883,16 | -0,0009 |

---

## Ejercicio 3: Cantidad de reseñas y precio

- **Ajuste del modelo:** Regresión lineal simple con `number_of_reviews` como predictor y `price_num` como objetivo (después de recortar extremos `[p1, p99]`, *27 086* observaciones).
- **Parámetros estimados:**
  - Intercepto ($\beta_0$): *$130 347,45 ARS*
  - Pendiente ($\beta_1$): *‑7,16 ARS* por reseña adicional.
- **Predicción (50 reseñas):** *$129 989,48 ARS* (cercano al precio medio del dataset).
- **Interpretación:**
  - $R^2 = 0,0001$ ⇒ menos del 0,01 % de la variabilidad explicada.
  - RMSE indistinguible del baseline.
- **Conclusión técnica:** La cantidad de reseñas **no** es un predictor útil del precio nocturno; la correlación observada es insignificante.

---

## Ejercicio 6: Estimación con k‑NN y selección de *k*

- **Metodología:** Validación cruzada (5‑fold) probando $k \in \{3,5,7,9,11,15\}$ con `StandardScaler` y `KNeighborsRegressor(weights="distance")`.
- **Resultados de validación:**
  - $k=3$: RMSE = $90 463,63 ARS$
  - $k=5$: RMSE = $87 297,92 ARS$
  - $k=7$: RMSE = $86 123,09 ARS$
  - $k=9$: RMSE = $85 439,58 ARS$
  - $k=11$: RMSE = $84 894,88 ARS$
  - **$k=15$ (mejor):** RMSE = $84 456,45 ARS$
- **Evaluación en conjunto de prueba (k = 15):**
  - MAE = *49 440,98 ARS*
  - RMSE = *80 753,06 ARS*
  - $R^2$ = *0,1921*
- **Impacto de `weights="distance"`:**
  $$ w_i = \frac{1}{d_i} $$
  Pondera más los vecinos estructuralmente cercanos, mejorando significativamente el rendimiento respecto al baseline.
- **Estimación puntual:** Primer anuncio de prueba → *$157 077,61 ARS* (real: *$238 143,09 ARS*; error ≈ $81 065,48 ARS*).
- **Conclusión técnica:**
  - Existe una **relación moderada** entre características del alojamiento y el precio, lo que permite **aproximar** el valor pero no explicarlo con alta precisión.
  - El modelo *k‑NN* sirve para estimar, **no** para explicar la causalidad del precio.

---
