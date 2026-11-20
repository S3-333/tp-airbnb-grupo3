"""Pipeline y funciones compartidas para el proyecto de estimación de precios de Airbnb en Buenos Aires.

Centraliza la carga de datos, la limpieza, el recorte de valores extremos
y las métricas de evaluación para los ejercicios y modelos del proyecto.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ---------------------------------------------------------------------------
# Rutas relativas a la raíz del repositorio
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[1]
RUTA_RAW = RAIZ / "data" / "raw" / "listings.csv.gz"
RUTA = RUTA_RAW  # alias para compatibilidad
RUTA_PROCESSED = RAIZ / "data" / "processed"
RUTA_FIGURAS = RAIZ / "reports" / "figures"


def convertir_precio(serie: pd.Series) -> pd.Series:
    """Convierte textos monetarios a valores numéricos flotantes.

    Ejemplo: "$186,530.00" -> 186530.0.
    Elimina caracteres que no sean dígitos, puntos o signos negativos.
    Valores no válidos o vacíos se transforman en NaN.
    """
    if not isinstance(serie, pd.Series):
        serie = pd.Series(serie)
    limpio = serie.astype(str).str.replace(r"[^0-9.-]", "", regex=True)
    return pd.to_numeric(limpio, errors="coerce")


def cargar_datos(ruta: Path | str | None = None) -> pd.DataFrame:
    """Carga el dataset de Airbnb (listings.csv.gz) y agrega la columna numérica 'price_num'.

    Parámetros
    ----------
    ruta : Path o str, opcional
        Ruta al archivo comprimido. Por defecto utiliza data/raw/listings.csv.gz.
        Nota: El archivo de datos crudos se mantiene versionado en el repositorio
        por motivos académicos (para evaluación del TP), aunque en producción
        versionar datos pesados en Git se considera habitualmente una mala práctica.

    Retorna
    -------
    pd.DataFrame con los datos y la columna 'price_num'.
    """
    if ruta is None:
        ruta = RUTA_RAW
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de datos en: {ruta}.\n"
            "El archivo listings.csv.gz se mantiene incluido en el repositorio por razones académicas.\n"
            "Si fue eliminado, puedes descargarlo de Inside Airbnb Buenos Aires y colocarlo en data/raw/."
        )

    df = pd.read_csv(ruta, compression="gzip", low_memory=False)
    if "price" not in df.columns:
        raise ValueError("El archivo no contiene la columna obligatoria 'price'.")

    df["price_num"] = convertir_precio(df["price"])
    return df


def preparar(
    df: pd.DataFrame,
    predictores: list[str],
    q_low: float = 0.01,
    q_high: float = 0.99,
) -> pd.DataFrame:
    """Limpia y prepara el conjunto de datos para un conjunto de variables predictoras.

    Pasos aplicados:
      1. Selecciona solo las columnas predictoras y 'price_num'.
      2. Convierte los predictores a tipo numérico (coerción de errores a NaN).
      3. Elimina filas con valores ausentes en las variables seleccionadas.
      4. Filtra precios estrictamente positivos (price_num > 0).
      5. Aplica un filtro de percentiles [q_low, q_high] sobre 'price_num'
         para eliminar distorsiones por valores atípicos extremos.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame cargado con la columna 'price_num'.
    predictores : list of str
        Nombres de las columnas explicativas.
    q_low : float, default=0.01
        Cuantil inferior para el recorte.
    q_high : float, default=0.99
        Cuantil superior para el recorte.

    Retorna
    -------
    pd.DataFrame limpio y listo para el modelado.
    """
    columnas = list(predictores) + ["price_num"]
    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        raise ValueError(f"Columnas no presentes en el DataFrame: {faltantes}")

    datos = df[columnas].copy()

    for col in predictores:
        datos[col] = pd.to_numeric(datos[col], errors="coerce")

    # Eliminar valores nulos
    datos = datos.dropna()

    # Precios estrictamente positivos
    datos = datos[datos["price_num"] > 0]

    # Recorte de valores extremos por percentiles
    if q_low > 0 or q_high < 1:
        q_inf, q_sup = datos["price_num"].quantile([q_low, q_high])
        datos = datos[datos["price_num"].between(q_inf, q_sup)]

    return datos


def evaluar(
    y_real: pd.Series | np.ndarray,
    y_pred: pd.Series | np.ndarray,
    verbose: bool = True,
) -> tuple[float, float, float]:
    """Calcula y opcionalmente imprime las métricas de regresión (MAE, RMSE, R²).

    Parámetros
    ----------
    y_real : array-like
        Valores observados reales.
    y_pred : array-like
        Valores estimados por el modelo.
    verbose : bool, default=True
        Si es True, imprime las métricas formateadas.

    Retorna
    -------
    tuple(mae, rmse, r2)
    """
    mae = float(mean_absolute_error(y_real, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_real, y_pred)))
    r2 = float(r2_score(y_real, y_pred))

    if verbose:
        print(f"MAE:  {mae:,.2f}")
        print(f"RMSE: {rmse:,.2f}")
        print(f"R²:   {r2:.4f}")

    return mae, rmse, r2


def guardar_datos_procesados(df: pd.DataFrame, nombre_archivo: str) -> Path:
    """Guarda un DataFrame procesado en la carpeta data/processed/."""
    RUTA_PROCESSED.mkdir(parents=True, exist_ok=True)
    destino = RUTA_PROCESSED / nombre_archivo
    df.to_csv(destino, index=False)
    return destino


def guardar_figura(plt_or_fig, nombre_archivo: str, dpi: int = 150) -> Path:
    """Guarda una figura generada en reports/figures/ asegurando que la carpeta exista."""
    RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
    destino = RUTA_FIGURAS / nombre_archivo
    if hasattr(plt_or_fig, "savefig"):
        plt_or_fig.savefig(destino, dpi=dpi, bbox_inches="tight")
    else:
        # matplotlib.pyplot
        import matplotlib.pyplot as plt
        plt.savefig(destino, dpi=dpi, bbox_inches="tight")
    return destino
