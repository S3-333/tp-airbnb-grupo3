# Decisiones de Diseño y Metodología

Este documento detalla las justificaciones teóricas y metodológicas adoptadas en el preprocesamiento, modelado y validación del proyecto.

---

## 1. Datos y Contexto

- **Fuente:** Inside Airbnb (*Detailed Listings data* para Buenos Aires, corte de septiembre de 2026).
- **Dimensiones:** 29.753 anuncios publicados y 91 columnas (incluyendo `price_num`).
- **Moneda de trabajo:** El precio publicado carece de código ISO explícito en la columna pero presenta importes consistentes con el mercado en pesos argentinos ($ ARS). Todos los errores y métricas (MAE, RMSE) se reportan en esta unidad.
- **Valores ausentes:** 
  - La columna `price` presenta un 7,12 % de nulos (2.119 registros).
  - La columna `beds` tiene un 1,75 % de nulos (522 registros).
  - `bedrooms` presenta 13 nulos (0,04 %) y `minimum_nights` 1 nulo (0,00 %).
  - Se descartan filas con valores ausentes únicamente en las variables requeridas por cada ejercicio, preservando el máximo número de observaciones útiles.

---

## 2. Limpieza y Filtro de Extremos

- **Conversión numérica (`convertir_precio`):** Se eliminan signos de moneda, comas y espacios en blanco, transformando el texto a valores flotantes continuos mediante expresiones regulares controladas.
- **Filtrado de precios no positivos:** Se excluyen valores de precio menores o iguales a cero.
- **Recorte por percentiles [1 %, 99 %]:**
  - *Motivación:* El precio máximo en el dataset bruto asciende a $160.563.800 ARS, lo que genera una media ($277.767 ARS) más del doble de la mediana ($106.393 ARS) y una asimetría extrema (skewness = 29,72).
  - *Corte:* Se fijan el percentil 1% ($26.907,14 ARS) y el 99% ($899.463,19 ARS).
  - *Efecto:* Tras el filtro se conservan 27.086 anuncios (pérdida de apenas el 2% de los datos válidos), la media converge a $129.895 ARS y la asimetría desciende a 3,35.
- **Fuga de datos leve:** Siguiendo la consigna de la guía, los percentiles se computan sobre el conjunto limpio previo a la separación entre train y test. Se considera una fuga inofensiva y aceptable puesto que no ajusta parámetros de ningún modelo, sino que define el dominio válido de propiedades habitacionales reales.

---

## 3. Estrategia de Modelado

### Ejercicio 3: Regresión Lineal Simple
- Se utilizó `LinearRegression` de scikit-learn con un único predictor (`number_of_reviews`).
- Dado que se busca contrastar una hipótesis de relación directa e interpretable entre la cantidad de reseñas y el precio, el modelo lineal simple resulta el instrumento analítico idóneo.

### Ejercicio 6: k-NN para Regresión (`weights="distance"`)
- **Estandarización (`StandardScaler`):** El algoritmo k-NN depende críticamente de la métrica de distancia Euclidiana. Variables con escalas dispares (como `minimum_nights` hasta 365 vs `bedrooms` de 1 a 5) generarían sesgos severos si no se normalizan a media 0 y varianza 1.
- **Ponderación por distancia (`weights="distance"`):**
  - Asigna pesos proporcionales al inverso de la distancia ($w_i = 1 / d_i$).
  - Evita que vecinos alejados pero dentro del vecindario $k$ diluyan la señal de vecinos que presentan atributos prácticamente idénticos al caso a estimar.
- **Validación Cruzada (5 pliegues):**
  - Se probó la grilla $k \in \{3, 5, 7, 9, 11, 15\}$ sobre el 75 % de entrenamiento para seleccionar el hiperparámetro que minimice el RMSE.
  - La evaluación en prueba se reserva estrictamente para el modelo ganador entrenado con el $k$ óptimo ($k=15$).

### Modelo de Referencia (Baseline)
- En ambos ejercicios se ajustó un `DummyRegressor(strategy="mean")` sobre el conjunto de entrenamiento.
- Esto permite cuantificar con rigor si los modelos aportan valor predictivo real o si se limitan a predecir la media de la distribución.
