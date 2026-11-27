Predicción de Autonomía de vehiculos eléctricos

## URL publica
_(pendiente: se publica el 19 de noviembre)_

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
conda activate ciencia_datos
solara run app.py

## Uso de IA
_El uso de la Inteligencia Artificial se dio para la comprensión de errores, para que generar casos de prueba sin sesgos caracterizados
por un humano y para diferentes puntos de opinión con respecto a la salida de información; ademas, me permitio corregir problemas de escritura de codigo y fue un apoyo 
para la creación del proyecto._

## Explicacion de mi codigo
_Fragmento 1: Función filtrar()

La función filtrar() permite seleccionar únicamente los vehículos cuya capacidad de batería se encuentra dentro del rango escogido por el usuario mediante 
el control deslizante. Esto hace posible explorar cómo cambia la distribución de los datos al analizar diferentes capacidades de batería.

Fragmento 2: Función grafico()

La función grafico() genera un gráfico de dispersión donde se visualiza la relación entre la capacidad de batería (kWh) y la autonomía estimada (km).
Este gráfico permite observar tendencias y comprobar visualmente que, en general, los vehículos con baterías de mayor capacidad suelen presentar una autonomía mayor.

Fragmento 3: Función texto_prediccion()

La función texto_prediccion() utiliza el modelo entrenado para estimar la autonomía de un vehículo a partir de las características seleccionadas por el usuario.
Además, emplea el error medio absoluto (MAE) para mostrar un intervalo razonable alrededor de la predicción, facilitando la interpretación del resultado.

Cambio propuesto

Como mejora futura, se propone incorporar una tabla comparativa de vehículos por marca y segmento, junto con indicadores estadísticos como autonomía promedio, autonomía máxima 
y eficiencia energética promedio. Esto permitiría que los compradores comparen alternativas de forma más completa además de obtener una predicción individual._
