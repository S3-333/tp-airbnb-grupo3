"""Tests unitarios para las funciones principales de src/pipeline.py."""

import numpy as np
import pandas as pd
import pytest

from pipeline import (
    convertir_precio,
    evaluar,
    preparar,
)


def test_convertir_precio_valores_normales():
    """Verifica la correcta conversión de cadenas con formato de moneda a floats."""
    entrada = pd.Series(["$186,530.00", "$50.00", "1,234.50", "99"])
    esperado = [186530.0, 50.0, 1234.5, 99.0]
    resultado = convertir_precio(entrada)

    np.testing.assert_allclose(resultado.values, esperado)


def test_convertir_precio_valores_invalidos_y_nulos():
    """Verifica que textos no numéricos o valores ausentes retornen NaN."""
    entrada = pd.Series(["gratis", "N/A", "", None, np.nan])
    resultado = convertir_precio(entrada)

    assert resultado.isna().all()


def test_preparar_filtrado_nulos_y_no_positivos():
    """Verifica que preparar() elimine filas con ausentes y precios <= 0."""
    df_prueba = pd.DataFrame({
        "accommodates": [2, np.nan, 4, 1, 3],
        "number_of_reviews": [10, 5, np.nan, 20, 0],
        "price_num": [100.0, 200.0, 150.0, 0.0, -50.0],
    })

    # Solo la fila 0 tiene accommodates, number_of_reviews válidos y price_num > 0
    df_limpio = preparar(df_prueba, ["accommodates", "number_of_reviews"], q_low=0, q_high=1)

    assert len(df_limpio) == 1
    assert df_limpio.iloc[0]["accommodates"] == 2
    assert df_limpio.iloc[0]["number_of_reviews"] == 10
    assert df_limpio.iloc[0]["price_num"] == 100.0


def test_preparar_recorte_percentiles():
    """Verifica que el filtro por cuantiles descarte los valores extremos."""
    # Generar 100 valores del 1 al 100
    precios = list(range(1, 101))
    df_prueba = pd.DataFrame({
        "number_of_reviews": [5] * 100,
        "price_num": precios,
    })

    df_limpio = preparar(df_prueba, ["number_of_reviews"], q_low=0.05, q_high=0.95)

    # El cuantil 0.05 de 1..100 es ~5.95 y el 0.95 es ~95.05
    assert df_limpio["price_num"].min() >= 5
    assert df_limpio["price_num"].max() <= 96
    assert len(df_limpio) < 100


def test_preparar_valida_columnas_faltantes():
    """Verifica que preparar() lance ValueError si faltan columnas requeridas."""
    df_prueba = pd.DataFrame({"accommodates": [2], "price_num": [100.0]})

    with pytest.raises(ValueError, match="Columnas no presentes"):
        preparar(df_prueba, ["columna_inexistente"])


def test_evaluar_metricas_conocidas():
    """Verifica el cálculo de MAE, RMSE y R² con valores de prueba controlados."""
    y_real = np.array([100.0, 200.0, 300.0])
    y_pred_perfecto = np.array([100.0, 200.0, 300.0])

    mae, rmse, r2 = evaluar(y_real, y_pred_perfecto, verbose=False)
    assert mae == pytest.approx(0.0)
    assert rmse == pytest.approx(0.0)
    assert r2 == pytest.approx(1.0)

    # Predicción con error constante de +10
    y_pred_error = np.array([110.0, 210.0, 310.0])
    mae_err, rmse_err, _ = evaluar(y_real, y_pred_error, verbose=False)
    assert mae_err == pytest.approx(10.0)
    assert rmse_err == pytest.approx(10.0)
