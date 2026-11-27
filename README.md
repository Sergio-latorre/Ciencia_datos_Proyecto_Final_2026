Predicción de Autonomía de vehiculos eléctricos

## URL publica
_https://ciencia-datos-proyecto-final-2026-k38l.onrender.com_



## Pregunta y decision
_¿Qué autonomía puede esperar un comprador de un vehículo eléctrico y cómo influye la capacidad de la batería en la autonomía estimada?
La herramienta se dirige a compradores y usuarios interesados en vehiculos electricos, que desean comparar opciones según su 
autonomia y capacidad de batería ,el tablero permite explorar la relación entre la capacidad de la bateria y la autonomía, ademas de estimar la autonomía esperada para diferentes 
configuraciones de vehiculos._

## Datos
_Conjunto de datos **Electric Car Performance and Battery Dataset**
El dataset contiene información tecnica de vehiulos eléctricos, incluyendo capacidad de bateria,
velocidad maxima, torque, consumo energetico, aceleración, potencia de carga rápida,
dimensiones, capacidad de remolque, tipo de bateria, tipo de tracción, segmento y autonomia estimada;
el conjunto analizado contiene 478 registros de vehiculos eléctricos_

## Limpieza
_A los datos, se les hizo una limpieza, en donde a los datos faltantes en las variables númericas se le puso la mediana y a las variables categoricas se selecciono a categoria más usada._

## Modelo y evaluacion
_Se entrenó un modelo de aprendizaje automático para predecir la autonomía estimada
de vehiculos eléctricos; la evaluación se realizo sobre 120 registros que no fueron utilizados 
durante el entrenamiento; como linea base se utilizo la estrategia de predecir siempre el promedio de la
variable objetivo, obteniendo un error absoluto medio de 86.114km; pero, el modelo entrenado obtuvo un error medio 
mucho menor de 11.996km sobre esas mismas 120 observaciones de prueba, debido a que el error es muy menor que el de la 
linea base, en donde identificamos que el modelo captura patrones relevantes y predicciones más precisas_

## Limitaciones
_Las predicciones dependen de la calidad y representatividad del conjunto de datos utilizado. Además, existen factores que 
pueden afectar la autonomía real de un vehículo eléctrico y que no están incluidos en el modelo, como las condiciones climáticas,
el estilo de conducción, la topografía del recorrido, el tráfico y el estado de degradación de la batería._

## Como correrlo
_conda activate ciencia_datos
solara run app.py o por medio del enlace en Render_

## Uso de IA
_El uso de la Inteligencia Artificial se dio para la comprensión de errores, para que generar casos de prueba sin sesgos caracterizados
por un humano y para diferentes puntos de opinión con respecto a la salida de información; ademas, me permitio corregir problemas de escritura de codigo y fue un apoyo 
para la creación del proyecto._

## Explicacion de mi codigo
_Fragmento 1: Partición de los datos en entrenamiento y test
X_b = datos.drop(columns=OBJETIVO)  # entradas
y_b = datos[OBJETIVO]  # objetivo
X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X_b, y_b, test_size=0.25, random_state=SEMILLA)
print(X_train_b.shape, X_test_b.shape)
En esta parte del codigo, lo que se hizo fue borrar la variable objetivo que en mi caso era 'range_km' y crear un nuevo conjutno de datos con solo esa variable, la cual iba a ser la variable a predecir en el test; para eso dividimos los datos en un 75% con una semilla para la reproducibilidad y despues imprimimos la forma que quedaron los dataset. 

Fragmento 2: Linea Base y comparación con el modelo
base_b.fit(X_train_b, y_train_b)  # las dos cosas aprenden solo de train
modelo_b.fit(X_train_b, y_train_b)
if metrica == 'MAE':
    valor_base = mean_absolute_error(y_test_b, base_b.predict(X_test_b))  # las dos se miden en test
    valor_modelo = mean_absolute_error(y_test_b, modelo_b.predict(X_test_b))
Aquí primero se entrena una regla muy simple (`DummyRegressor`, que siempre responde el promedio de autonomía del entrenamiento) y luego el modelo de regresión lineal usando solo los datos de entrenamiento.
Después a los dos datos entrenados se les aplica el MAE (El error absoluto medio) para comparar cual de los dos (linea base o modelo) es mejor para la prediccíón

Fragmento 3: Filtro del tablero en `app.py` y rango sin datos
def filtrar(tabla, columna, desde, hasta):
    # Devuelve solo las filas con la columna entre desde y hasta (incluidos). (Taller 15)
    return tabla[tabla[columna].between(desde, hasta)]
La función `filtrar` toma la tabla de vehículos y se queda únicamente con los que tienen la capacidad de batería dentro del intervalo elegido en el control deslizante, incluyendo los bordes.

Como mejora futura, se propone incorporar una tabla comparativa de vehículos por marca y segmento, junto con indicadores estadísticos como autonomía promedio, autonomía máxima 
y eficiencia energética promedio. Esto permitiría que los compradores comparen alternativas de forma más completa además de obtener una predicción individual._
