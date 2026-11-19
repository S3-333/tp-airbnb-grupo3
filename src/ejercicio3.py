"""Ejercicio 3: Cantidad de reseñas y precio (Regresión Lineal Simple).

Analiza si la cantidad de reseñas acumuladas (number_of_reviews) permite
estimar por sí sola el precio nocturno (price) de los anuncios en Buenos Aires.

Ejecución directa:
    python src/ejercicio3.py
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

try:
    from pipeline import (
        cargar_datos,
        evaluar,
        guardar_datos_procesados,
        guardar_figura,
        preparar,
    )
except ImportError:
    from src.pipeline import (
        cargar_datos,
        evaluar,
        guardar_datos_procesados,
        guardar_figura,
        preparar,
    )


def ejecutar_ejercicio3():
    print("=" * 65)
    print("EJERCICIO 3: ANÁLISIS DE RESEÑAS VS PRECIO (REGRESIÓN LINEAL)")
    print("=" * 65)

    # 1. Carga de datos
    df = cargar_datos()
    predictores = ["number_of_reviews"]
    print(f"Total de registros originales: {len(df):,}")

    # 2 y 3. Limpieza y recorte de valores extremos
    datos = preparar(df, predictores)
    print(f"Registros tras limpieza y filtro [p1, p99]: {len(datos):,}")

    # Guardar dataset procesado
    guardar_datos_procesados(datos, "ej3_limpio.csv")

    X = datos[predictores]
    y = datos["price_num"]

    # 4. Partición en entrenamiento (75%) y prueba (25%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    print(f"Observaciones train: {len(X_train):,} | test: {len(X_test):,}")

    # 5. Gráfico de dispersión (muestra representativa de 1.500 observaciones)
    muestra = datos.sample(min(1500, len(datos)), random_state=42).sort_values("number_of_reviews")
    plt.figure(figsize=(8, 5))
    plt.scatter(muestra["number_of_reviews"], muestra["price_num"], alpha=0.3, color="#1f77b4")
    plt.xlabel("Cantidad de reseñas (number_of_reviews)")
    plt.ylabel("Precio nocturno ($ ARS)")
    plt.title("Dispersión: Reseñas vs. Precio")
    guardar_figura(plt, "ej3_dispersion.png")
    plt.show()
    print("-> Gráfico guardado: reports/figures/ej3_dispersion.png")

    # 6. Ajuste del modelo de Regresión Lineal Simple
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    # 7. Evaluación en conjunto de prueba
    print("\n--- Métricas del Modelo en Prueba ---")
    mae, rmse, r2 = evaluar(y_test, y_pred)
    print(f"Intercepto: {modelo.intercept_:,.2f}")
    print(f"Pendiente:  {modelo.coef_[0]:,.2f} pesos por reseña")


    # 8. Estimación para anuncio con 50 reseñas
    caso_50 = pd.DataFrame({"number_of_reviews": [50]})
    pred_50 = modelo.predict(caso_50)[0]
    print(f"\nEstimación para un anuncio con 50 reseñas: ${pred_50:,.2f} ARS")

    # 9. Gráfico de la recta ajustada
    plt.figure(figsize=(8, 5))
    plt.scatter(muestra["number_of_reviews"], muestra["price_num"], alpha=0.25, label="Anuncios (muestra)", color="#1f77b4")
    pred_recta = modelo.predict(muestra[["number_of_reviews"]])
    plt.plot(muestra["number_of_reviews"], pred_recta, color="#d62728", linewidth=2, label="Recta de regresión")
    plt.xlabel("Cantidad de reseñas (number_of_reviews)")
    plt.ylabel("Precio nocturno ($ ARS)")
    plt.title("Regresión Lineal: Cantidad de Reseñas vs. Precio")
    plt.legend()
    guardar_figura(plt, "ej3_recta.png")
    plt.show()
    print("-> Gráfico guardado: reports/figures/ej3_recta.png")

    # 10. Tabla comparativa real vs predicho (primeros 10 de prueba)
    comparacion = pd.DataFrame({
        "Real ($)": y_test.values[:10],
        "Predicho ($)": y_pred[:10],
        "Diferencia ($)": y_test.values[:10] - y_pred[:10]
    })
    print("\nComparación de primeras 10 observaciones de prueba:")
    print(comparacion.round(2).to_string(index=False))

    # Conclusión
    print("\n" + "=" * 65)
    print("CONCLUSIONES EJERCICIO 3:")
    print("1. La regresión lineal simple arroja un R² de 0.0001, prácticamente nulo.")
    print("2. La pendiente es de apenas -7.16 ARS por reseña, indicando ausencia de relación lineal.")
    print("3. Para 50 reseñas estima $129,989.48 ARS, prácticamente idéntico a predecir la media.")
    print("4. Por sí sola, la cantidad de reseñas acumuladas NO es un predictor útil del precio.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    ejecutar_ejercicio3()
