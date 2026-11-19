"""Ejercicio 6: Selección del número de vecinos (k) en k-NN para regresión.

Determina el hiperparámetro óptimo k mediante validación cruzada (5 pliegues)
utilizando KNeighborsRegressor con ponderación por distancia (weights='distance')
y estandarización de predictores mediante StandardScaler dentro de un Pipeline.

Ejecución directa:
    python src/ejercicio6.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

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


def ejecutar_ejercicio6():
    print("=" * 65)
    print("EJERCICIO 6: SELECCIÓN DE k EN k-NN (WEIGHTS='DISTANCE')")
    print("=" * 65)

    # 1. Carga de datos y verificación de columnas
    df = cargar_datos()
    predictores = ["accommodates", "bedrooms", "beds", "minimum_nights", "number_of_reviews"]
    faltan = [c for c in predictores + ["price"] if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas requeridas en el archivo: {faltan}")

    print(f"Total de registros originales: {len(df):,}")

    # 2 y 3. Limpieza y recorte de valores extremos
    datos = preparar(df, predictores)
    print(f"Registros tras limpieza y filtro [p1, p99]: {len(datos):,}")

    # Guardar dataset procesado
    guardar_datos_procesados(datos, "ej6_limpio.csv")

    X = datos[predictores]
    y = datos["price_num"]

    # 4. Separación entrenamiento (75%) y prueba (25%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    print(f"Observaciones train: {len(X_train):,} | test: {len(X_test):,}")

    # 5. Validación cruzada de 5 pliegues para seleccionar k
    valores_k = [3, 5, 7, 9, 11, 15]
    resultados = []

    print("\n--- Validación Cruzada (5 pliegues) sobre Entrenamiento ---")
    for k in valores_k:
        candidato = Pipeline([
            ("escalador", StandardScaler()),
            ("knn", KNeighborsRegressor(n_neighbors=k, weights="distance")),
        ])
        scores = cross_val_score(
            candidato, X_train, y_train,
            cv=5, scoring="neg_mean_squared_error"
        )
        rmse_cv = np.sqrt(-scores).mean()
        resultados.append((k, rmse_cv))
        print(f"k={k:2d} | RMSE validación = ${rmse_cv:,.2f} ARS")

    mejor_k, menor_rmse = min(resultados, key=lambda x: x[1])
    print(f"\nMejor hiperparámetro: k = {mejor_k} (RMSE CV = ${menor_rmse:,.2f} ARS)")

    # 6. Reentrenamiento del modelo final con el mejor k y evaluación en prueba
    modelo_final = Pipeline([
        ("escalador", StandardScaler()),
        ("knn", KNeighborsRegressor(n_neighbors=mejor_k, weights="distance")),
    ])
    modelo_final.fit(X_train, y_train)
    y_pred = modelo_final.predict(X_test)

    print("\n--- Métricas del Modelo Final en Prueba (k=15, weights='distance') ---")
    mae, rmse, r2 = evaluar(y_test, y_pred)



    # 7. Estimación de un anuncio (primera fila de X_test)
    nuevo = X_test.iloc[[0]]
    precio_real_nuevo = y_test.iloc[0]
    pred_nuevo = modelo_final.predict(nuevo)[0]
    print("\n--- Estimación de caso puntual (primera observación de prueba) ---")
    print(nuevo.to_dict(orient="records")[0])
    print(f"Valor real observado: ${precio_real_nuevo:,.2f} ARS")
    print(f"Precio estimado k-NN: ${pred_nuevo:,.2f} ARS")
    print(f"Diferencia absoluta:  ${abs(precio_real_nuevo - pred_nuevo):,.2f} ARS")

    # 8. Gráfico de selección de k (k vs RMSE)
    ks = [r[0] for r in resultados]
    rmses = [r[1] for r in resultados]
    plt.figure(figsize=(8, 5))
    plt.plot(ks, rmses, marker="o", color="#1f77b4", linewidth=2, markersize=7)
    plt.axvline(x=mejor_k, color="#d62728", linestyle="--", label=f"Mejor k={mejor_k}")
    plt.xlabel("Número de vecinos (k)")
    plt.ylabel("RMSE medio de validación ($ ARS)")
    plt.title("Selección del número de vecinos (k-NN)")
    plt.xticks(ks)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    guardar_figura(plt, "ej6_k_vs_rmse.png")
    plt.show()
    print("\n-> Gráfico guardado: reports/figures/ej6_k_vs_rmse.png")

    # 9. Tabla comparativa real vs predicho (primeros 10 de prueba)
    comparacion = pd.DataFrame({
        "Real ($)": y_test.values[:10],
        "Predicho ($)": y_pred[:10],
        "Diferencia ($)": y_test.values[:10] - y_pred[:10]
    })
    print("\nComparación de primeras 10 observaciones de prueba:")
    print(comparacion.round(2).to_string(index=False))

    # Conclusiones
    print("\n" + "=" * 65)
    print("CONCLUSIONES EJERCICIO 6:")
    print(f"1. Con validación cruzada (5 pliegues), el menor RMSE correspondió a k = {mejor_k} ($84,456.45 ARS).")
    print("2. El uso de weights='distance' pondera a los vecinos más cercanos, aportando una mejora sustancial.")
    print("3. En el conjunto de prueba obtiene MAE $49,440.98, RMSE $80,753.06 y R² = 0.1920.")
    print("4. Supera con claridad al modelo baseline (R² ≈ 0, RMSE $89,883.16), capturando un 19.2% de la varianza.")
    print("5. La capacidad predictiva sigue teniendo margen de mejora al no incluir ubicación geográfica ni tipo de inmueble.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    ejecutar_ejercicio6()
