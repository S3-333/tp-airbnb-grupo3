# Conclusiones del Proyecto

Los datos muestran que existe una relación real, pero moderada, entre las características del alojamiento (`accommodates`, `bedrooms`, `beds`, `minimum_nights` y `number_of_reviews`) y su precio nocturno.

- **Rendimiento del modelo:** El $k$-NN con $k = 15$ logra un $R^2 \approx 0,19$ y un error medio (MAE) de unos **$50.000 ARS**, lo que equivale a casi el 40 % del precio promedio (~$130.000 ARS).
- **Interpretación predictiva:** Las predicciones quedan cerca del orden de magnitud del precio real y mejoran claramente a predecir siempre el promedio ($R^2 \approx 0$), pero todavía se alejan bastante del valor exacto, como en el caso puntual estimado (**$157.077 ARS** frente a un real de **$238.143 ARS**).
- **Conclusión técnica:** Estas variables ayudan a estimar el precio de forma aproximada, pero no lo determinan por sí solas. Además, el modelo se limita a encontrar anuncios parecidos y promediar sus precios: muestra que esas características acompañan al precio, pero no demuestra que sean la causa de que un alojamiento cueste más o menos. Por eso sirve para estimar, no para explicar qué hace que un precio sea alto o bajo.
