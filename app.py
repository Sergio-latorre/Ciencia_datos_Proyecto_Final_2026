# app.py - tablero de mi proyecto final (Solara). Se publica el 19 de noviembre.
PREGUNTA = '¿Que autonomia puede esperar un comprador de un vehiculo electrico y como influye la capacidad de la bateria en la autonomia estimada?'  # la pregunta del proyecto, terminada en signo de interrogacion
A_QUIEN = 'Compradores y usuarios interesados en vehiculos electricos que desean comparar opciones segun su autonomia y capacidad de bateria.'  # quien usa el tablero y que decide con el
COLUMNA_FILTRO = 'battery_capacity_kWh' # columna numerica de datos_proyecto.csv para el deslizador
ETIQUETA_FILTRO = 'Capacidad de bateria (kWh)'  # nombre de esa columna con su unidad
ETIQUETA_OBJETIVO = 'Autonomia estimada (km)' # nombre del objetivo con su unidad
FUENTE = 'Electric Car Performance and Battery Dataset'  # enlace si es publico; origen y autorizacion si es privado
ETIQUETAS = {
    'top_speed_kmh': 'Velocidad maxima (km/h)',
    'battery_capacity_kWh': 'Capacidad de bateria (kWh)',
    'number_of_cells': 'Numero de celdas',
    'torque_nm': 'Torque (Nm)',
    'efficiency_wh_per_km': 'Consumo energetico (Wh/km)',
    'acceleration_0_100_s': 'Aceleracion 0-100 km/h (s)',
    'fast_charging_power_kw_dc': 'Potencia de carga rapida (kW)',
    'towing_capacity_kg': 'Capacidad de remolque (kg)',
    'seats': 'Numero de asientos',
    'length_mm': 'Longitud (mm)',
    'width_mm': 'Ancho (mm)',
    'height_mm': 'Altura (mm)',
    'brand': 'Marca',
    'battery_type': 'Tipo de bateria',
    'fast_charge_port': 'Puerto de carga rapida',
    'drivetrain': 'Traccion',
    'segment': 'Segmento',
    'car_body_type': 'Tipo de carroceria',
    'model': 'Modelo',
    'cargo_volume_l': 'Volumen de carga (L)'
}

from pathlib import Path  # rutas de archivos
import joblib  # lee el modelo guardado
import pandas as pd  # tablas de datos
import solara  # tablero web
from matplotlib.figure import Figure  # grafico que Solara sabe mostrar

CARPETA = Path(__file__).parent  # rutas relativas: el servidor no tiene su disco
datos = pd.read_csv(CARPETA / 'datos_proyecto.csv')  # los datos del Taller 14
resultado = pd.read_csv(CARPETA / 'resultado_proyecto.csv').iloc[0]  # la evaluacion en test
modelo = joblib.load(CARPETA / 'modelo_proyecto.joblib')  # el modelo entrenado
OBJETIVO = resultado['objetivo']  # lo que predice el modelo
ENTRADAS = [col for col in datos.columns if col != OBJETIVO]  # todo menos el objetivo

def filtrar(tabla, columna, desde, hasta):
    # Devuelve solo las filas con la columna entre desde y hasta (incluidos). (Taller 15)
    return tabla[tabla[columna].between(desde, hasta)]

def texto_resultado(res):
    # Frase honesta: el modelo comparado con la linea base, medido en datos no vistos. (Taller 15)
    if res['metrica'] == 'MAE':
        return (f"Adivinar siempre el promedio se equivoca en promedio **{res['valor_linea_base']}**; "
                f"el modelo, **{res['valor_modelo']}**. Medido en {res['filas_test']} filas que el modelo no vio.")
    return (f"Decir siempre la clase mas comun acierta **{res['valor_linea_base']:.0%}**; "
            f"el modelo, **{res['valor_modelo']:.0%}**. Medido en {res['filas_test']} filas que el modelo no vio.")

def grafico(tabla, columna_x, columna_y, titulo, etiqueta_x, etiqueta_y):
    # Dispersion de dos columnas, con titulo y ejes rotulados. (Taller 15)
    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.scatter(tabla[columna_x], tabla[columna_y], s=12, alpha=0.6)
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    return fig

def valor_tipico(serie):
    # Mediana si la columna es numerica; el valor mas comun si no lo es. (Parte 1)
    if pd.api.types.is_integer_dtype(serie):
        return int(round(serie.median()))
    if pd.api.types.is_numeric_dtype(serie):
        return float(serie.median())
    return serie.mode()[0]

def le_gana(res):
    # True si el modelo supera a la linea base en test. (Parte 3)
    if res['metrica'] == 'MAE':
        return res['valor_modelo'] < res['valor_linea_base']
    return res['valor_modelo'] > res['valor_linea_base']

def texto_prediccion(valor, res):
    # La prediccion de un caso con el error medido en test, en palabras del usuario. (Parte 3)
    if res['metrica'] == 'MAE':
        error = res['valor_modelo']
        return (f"El modelo estima **{valor:.1f}**. En {res['filas_test']} filas que no vio se equivoco en promedio "
                f"{error}: espere un valor entre **{valor - error:.1f}** y **{valor + error:.1f}**.")
    return (f"El modelo dice **{valor}**. En {res['filas_test']} filas que no vio acerto el {res['valor_modelo']:.0%}; "
            f"decir siempre la clase mas comun acierta el {res['valor_linea_base']:.0%}.")

def grafico_distribucion(tabla, columna, marca, titulo, etiqueta):
    # Como se reparten los valores de una columna, con el caso del usuario marcado en rojo. (Parte 4)
    fig = Figure(figsize=(6, 3))
    ax = fig.subplots()
    if pd.api.types.is_numeric_dtype(tabla[columna]):
        ax.hist(tabla[columna].dropna(), bins=20, color='lightgray')
        ax.axvline(marca, color='crimson', linewidth=2)
    else:
        conteo = tabla[columna].value_counts()
        ax.bar(conteo.index.astype(str), conteo.values, color=['crimson' if str(v) == str(marca) else 'lightgray' for v in conteo.index])
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta)
    ax.set_ylabel('Numero de filas')
    return fig

minimo = float(datos[COLUMNA_FILTRO].min())
maximo = float(datos[COLUMNA_FILTRO].max())
rango = solara.reactive((minimo, maximo))  # estado del filtro: empieza con todo el rango
caso = {col: solara.reactive(valor_tipico(datos[col])) for col in ENTRADAS}  # estado del caso: el tipico

def control(col):
    # Entrada de una columna que solo deja elegir valores que el modelo vio: no se rompe ni extrapola.
    serie, etiqueta = datos[col], ETIQUETAS.get(col, col)
    if pd.api.types.is_integer_dtype(serie):
        solara.SliderInt(etiqueta, value=caso[col], min=int(serie.min()), max=int(serie.max()))
    elif pd.api.types.is_numeric_dtype(serie):
        solara.SliderFloat(etiqueta, value=caso[col], min=float(serie.min()), max=float(serie.max()))
    else:
        solara.Select(etiqueta, value=caso[col], values=sorted(serie.dropna().unique().tolist()))

@solara.component
def Exploracion():
    desde, hasta = rango.value  # el rango que eligio el usuario
    filtradas = filtrar(datos, COLUMNA_FILTRO, desde, hasta)
    solara.SliderRangeFloat(ETIQUETA_FILTRO, value=rango, min=minimo, max=maximo)
    solara.Markdown(f'Filas en el rango: **{len(filtradas)}** de {len(datos)}')
    if len(filtradas) == 0:
        solara.Markdown('**Ninguna fila cumple el filtro. Amplie el rango.**')
    else:
        solara.FigureMatplotlib(grafico(filtradas, COLUMNA_FILTRO, OBJETIVO, PREGUNTA, ETIQUETA_FILTRO, ETIQUETA_OBJETIVO))
    with solara.Card('Que tan bueno es el modelo'):
        solara.Markdown(texto_resultado(resultado))

@solara.component
def VistaPrediccion():
    solara.Markdown('## Pruebe un caso')
    for columna in ENTRADAS:
        if columna not in ['source_url', 'model']:
            control(columna)
    tabla_caso = pd.DataFrame([{col: caso[col].value for col in ENTRADAS}])  # el caso, en una fila
    valor = modelo.predict(tabla_caso)[0]
    solara.Markdown(texto_prediccion(valor, resultado))
    if not le_gana(resultado):
        solara.Markdown('**Ojo: este modelo no le gana a la linea base. Tome la estimacion con cautela.**')
    solara.FigureMatplotlib(grafico_distribucion(datos, OBJETIVO, valor, 'Donde cae su caso frente a los datos?', ETIQUETA_OBJETIVO))

@solara.component
def Page():
    solara.Title('Tablero del proyecto')
    solara.Markdown('## ' + PREGUNTA)
    solara.Markdown('**Para quien:** ' + A_QUIEN)
    Exploracion()
    VistaPrediccion()
    solara.Markdown('**Fuente de los datos:** ' + FUENTE)
#tercer-grafico

def grafico_carroceria(tabla, columna_cat, columna_y, titulo, etiqueta_x, etiqueta_y):
    # Autonomia promedio por tipo de carroceria, con titulo y ejes con unidad.
    resumen = (
        tabla.groupby(columna_cat, dropna=True)[columna_y]
        .mean()
        .sort_values(ascending=True)
    )
    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    ax.barh(resumen.index.astype(str), resumen.values, color='#2b6cb0', alpha=0.85)
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    fig.tight_layout()
    return fig

@solara.component
def Exploracion():
    desde, hasta = rango.value  # el rango que eligio el usuario
    filtradas = filtrar(datos, COLUMNA_FILTRO, desde, hasta)
    solara.SliderRangeFloat(ETIQUETA_FILTRO, value=rango, min=minimo, max=maximo)
    solara.Markdown(f'Filas en el rango: **{len(filtradas)}** de {len(datos)}')
    if len(filtradas) == 0:
        solara.Markdown('**Ninguna fila cumple el filtro. Amplie el rango.**')
    else:
        solara.FigureMatplotlib(
            grafico(
                filtradas,
                COLUMNA_FILTRO,
                OBJETIVO,
                '¿Cómo influye la capacidad de batería en la autonomía?',
                ETIQUETA_FILTRO,
                ETIQUETA_OBJETIVO,
            )
        )
        solara.FigureMatplotlib(
            grafico_carroceria(
                filtradas,
                'car_body_type',
                OBJETIVO,
                '¿Qué tipo de carrocería ofrece mayor autonomía promedio?',
                ETIQUETA_OBJETIVO,
                ETIQUETAS['car_body_type'],
            )
        )
    with solara.Card('Que tan bueno es el modelo'):
        solara.Markdown(texto_resultado(resultado))

def grafico_consumo(tabla, columna_x, columna_y, columna_color, titulo, etiqueta_x, etiqueta_y, etiqueta_color):
    # Relacion entre consumo energetico y autonomia, coloreado por capacidad de bateria.
    fig = Figure(figsize=(6, 4))
    ax = fig.subplots()
    dispersion = ax.scatter(
        tabla[columna_x],
        tabla[columna_y],
        c=tabla[columna_color],
        cmap='viridis',
        s=14,
        alpha=0.75,
    )
    barra = fig.colorbar(dispersion, ax=ax)
    barra.set_label(etiqueta_color)
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel(etiqueta_y)
    fig.tight_layout()
    return fig

@solara.component
def Exploracion():
    desde, hasta = rango.value  # el rango que eligio el usuario
    filtradas = filtrar(datos, COLUMNA_FILTRO, desde, hasta)
    solara.SliderRangeFloat(ETIQUETA_FILTRO, value=rango, min=minimo, max=maximo)
    solara.Markdown(f'Filas en el rango: **{len(filtradas)}** de {len(datos)}')
    if len(filtradas) == 0:
        solara.Markdown('**Ninguna fila cumple el filtro. Amplie el rango.**')
    else:
        solara.FigureMatplotlib(
            grafico(
                filtradas,
                COLUMNA_FILTRO,
                OBJETIVO,
                '¿Cómo influye la capacidad de batería en la autonomía?',
                ETIQUETA_FILTRO,
                ETIQUETA_OBJETIVO,
            )
        )
        solara.FigureMatplotlib(
            grafico_consumo(
                filtradas,
                'efficiency_wh_per_km',
                OBJETIVO,
                COLUMNA_FILTRO,
                '¿Cómo influye el consumo energético en la autonomía?',
                ETIQUETAS['efficiency_wh_per_km'],
                ETIQUETA_OBJETIVO,
                ETIQUETA_FILTRO,
            )
        )
        solara.FigureMatplotlib(
            grafico_carroceria(
                filtradas,
                'car_body_type',
                OBJETIVO,
                '¿Qué tipo de carrocería ofrece mayor autonomía promedio?',
                ETIQUETA_OBJETIVO,
                ETIQUETAS['car_body_type'],
            )
        )
    with solara.Card('Que tan bueno es el modelo'):
        solara.Markdown(texto_resultado(resultado))

def texto_prediccion(valor, res):
    # La prediccion de un caso con el error medido en test, en palabras del usuario. (Parte 3)
    if res['metrica'] == 'MAE':
        error = res['valor_modelo']
        return (f"El modelo estima **{valor:.1f} km**. En {res['filas_test']} filas que no vio se equivoco en promedio "
                f"{error} km: espere un valor entre **{valor - error:.1f} km** y **{valor + error:.1f} km**.")
    return (f"El modelo dice **{valor}**. En {res['filas_test']} filas que no vio acerto el {res['valor_modelo']:.0%}; "
            f"decir siempre la clase mas comun acierta el {res['valor_linea_base']:.0%}.")

def filtrar(tabla, columna, desde, hasta):
    # Devuelve solo las filas con la columna entre desde y hasta (incluidos). (Taller 15)
    return tabla[tabla[columna].between(desde, hasta)]

def texto_resultado(res):
    # Frase honesta: el modelo comparado con la linea base, medido en datos no vistos.
    if res['metrica'] == 'MAE':
        return (f"Adivinar siempre el promedio se equivoca en promedio **{res['valor_linea_base']} km**; "
                f"el modelo, **{res['valor_modelo']} km**. Medido en {res['filas_test']} filas que el modelo no vio.")
    return (f"Decir siempre la clase mas comun acierta **{res['valor_linea_base']:.0%}**; "
            f"el modelo, **{res['valor_modelo']:.0%}**. Medido en {res['filas_test']} filas que el modelo no vio.")

def filtrar(tabla, columna, desde, hasta):
    # Devuelve solo las filas con la columna entre desde y hasta (incluidos). (Taller 15)
    return tabla[tabla[columna].between(desde, hasta)]

def texto_resultado(res):
    # Frase honesta: el modelo comparado con la linea base, medido en datos no vistos.
    if res['metrica'] == 'MAE':
        return (f"La linea base en el error absoluto medio se equivoco **{round(res['valor_linea_base']),1} km**; "
                f"el modelo, **{round(res['valor_modelo']),1} km**. Medido en {res['filas_test']} filas que el modelo no vio.")
    return (f"Decir siempre la clase mas comun acierta **{res['valor_linea_base']:.0%}**; "
            f"el modelo, **{res['valor_modelo']:.0%}**. Medido en {res['filas_test']} filas que el modelo no vio.")

def filtrar(tabla, columna, desde, hasta):
    # Devuelve solo las filas con la columna entre desde y hasta (incluidos). (Taller 15)
    return tabla[tabla[columna].between(desde, hasta)]

def texto_resultado(res):
    # Frase honesta: el modelo comparado con la linea base, medido en datos no vistos.
    if res['metrica'] == 'MAE':
        return (f"La linea base en el error absoluto medio se equivoco **{round(res['valor_linea_base']),1} km**; "
                f"el modelo se equivoco un:  **{round(res['valor_modelo']),1} km**. Medido en {res['filas_test']} filas que el modelo no vio.")
    return (f"Decir siempre la clase mas comun acierta **{res['valor_linea_base']:.0%}**; "
            f"el modelo, **{res['valor_modelo']:.0%}**. Medido en {res['filas_test']} filas que el modelo no vio.")
