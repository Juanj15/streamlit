import streamlit as st
import pandas as pd
import utilidades as util
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Título e icono de la página
st.set_page_config(page_title="Trayecto regional", page_icon="🏔️", layout="wide")
util.generarMenu()

# Función para cargar y procesar datos
@st.cache_data
def cargar_y_procesar_datos(ruta_archivo):
    try:
        # Cargar archivo CSV
        emisiones_df = pd.read_csv(ruta_archivo, encoding="latin1", sep=",")

        # Agrupar por 'OEM_Make' y 'Mission'
        emisiones_por_vehiculo_mision = emisiones_df.groupby(['OEM_Make', 'Mission'])['Emision_CO2_avg'].mean().reset_index()

        # Emisión promedio por fabricante
        emisiones_promedio_por_fabricante = emisiones_por_vehiculo_mision.groupby('OEM_Make')['Emision_CO2_avg'].mean().reset_index()
        emisiones_promedio_por_fabricante = emisiones_promedio_por_fabricante.sort_values('Emision_CO2_avg')

        return emisiones_df, emisiones_por_vehiculo_mision, emisiones_promedio_por_fabricante

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        return None, None, None

# Cargar los datos
ruta_archivo = "datos_vehiculo_regional.csv"
with st.spinner("Cargando y procesando datos..."):
    emisiones_df, emisiones_por_vehiculo_mision, emisiones_promedio_por_fabricante = cargar_y_procesar_datos(ruta_archivo)

# Verificar si se cargaron los datos correctamente
if emisiones_df is not None:
    st.header("Análisis de emisiones")
    st.write("""
    Este análisis evalúa las emisiones promedio de CO2 al agrupar los datos por tipo de misión (Mission) 
    y fabricante del vehículo (OEM_Make). La comparación permite identificar qué misiones y fabricantes 
    presentan mayores niveles de emisiones.
    """)

    # Filtro dinámico con opción de desmarcar
    st.write("## Comparación de emisiones de CO2 por fabricante y misión")
    opcion_emisiones = st.selectbox(
        "Filtrar por tipo de vehículo:",
        ["-- Sin filtro --", "Sin carga (L_CO2_gkm)", "Con carga (R_CO2_gkm)"]
    )

    # Determinar la columna de emisiones según la opción seleccionada
    if opcion_emisiones == "Sin carga (L_CO2_gkm)":
        columna_emisiones = "L_CO2_gkm"
    elif opcion_emisiones == "Con carga (R_CO2_gkm)":
        columna_emisiones = "R_CO2_gkm"
    else:
        columna_emisiones = "Emision_CO2_avg"  # Información inicial por defecto

    # Agrupar los datos dinámicamente según la columna seleccionada
    emisiones_por_vehiculo_mision_seleccion = (
        emisiones_df.groupby(['OEM_Make', 'Mission'])[columna_emisiones]
        .mean()
        .reset_index()
        .rename(columns={columna_emisiones: "Emision_CO2_avg"})
    )

    # Calcular la emisión promedio por fabricante
    emisiones_promedio_por_fabricante = (
        emisiones_por_vehiculo_mision_seleccion.groupby('OEM_Make')['Emision_CO2_avg']
        .mean()
        .reset_index()
        .sort_values(by="Emision_CO2_avg")
    )

    # Layout con dos columnas
    col1, col2 = st.columns([3, 1])

    # Gráfica dinámica
    with col1:
        fig = px.bar(
            emisiones_por_vehiculo_mision_seleccion,
            x="OEM_Make",
            y="Emision_CO2_avg",
            color="Mission",
            title="Emisiones de CO2 por fabricante y misión",
            labels={
                "OEM_Make": "Fabricante",
                "Emision_CO2_avg": "Emisiones de CO2 (g/km)",
                "Mission": "Tipo de misión"
            }
        )
        fig.update_layout(
            legend_title="Tipo de Misión",
            legend=dict(orientation="h", y=1.02, x=1),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig)

    # Métrica dinámica
    with col2:
        st.subheader("Hallazgos")
        st.write("Este indicador muestra la marca con menor promedio de emisiones de CO2, comparándola con el promedio general.")

        # Calcular los valores dinámicos
        marca_menor_emision = emisiones_promedio_por_fabricante.iloc[0]["OEM_Make"]
        emision_menor = emisiones_promedio_por_fabricante.iloc[0]["Emision_CO2_avg"]
        emision_promedio_total = emisiones_promedio_por_fabricante["Emision_CO2_avg"].mean()
        delta_emision = emision_menor - emision_promedio_total

        # Mostrar la métrica
        st.metric(
            label="Marca con menor emisión",
            value=f"{marca_menor_emision}",
            delta=f"{delta_emision:.2f} g/km respecto al promedio",
        )
else:
    st.error("No se pudieron cargar los datos. Verifique el archivo.")

st.write("---")
st.write("   ")

col5, col6 = st.columns([1, 3])

with col5:
    st.subheader("Tendencias")
    st.write("""Las recorridos (misiones) como **Regional delivery** tienen niveles elevados de emisiones, reflejando el uso intensivo de vehículos Diesel para transporte de cargas en distancias medianas.
                
                \nOtras misiones presentan variabilidad, pero la predominancia del Diesel es clara en los niveles de CO2.""")

with col6:

        fig = px.box(emisiones_df, x='MS_FuelType', y='Emision_CO2_avg',
                    title='Distribución de emisiones de CO2 por tipo de combustible',
                    labels={'MS_FuelType': 'Tipo de combustible', 'Emision_CO2_avg': 'Emisiones de CO2 (g/km)'},
                    color='MS_FuelType') #Añadimos color por cada tipo de combustible.

        fig.update_layout(yaxis_title='Emisiones de CO2 (g/km)',
                        xaxis_title='Tipo de combustible')
        st.plotly_chart(fig)


st.write("---")
st.write("   ")

col7, col8 = st.columns([3, 2])
with col7:
        if emisiones_df is not None:
            # 1. Calcular las emisiones totales por categoría
            emisiones_por_categoria = (
                emisiones_df.groupby("MS_VehicleCategoryCode")["Emision_CO2_avg"]
                .sum()
                .reset_index()
            )
            emisiones_por_categoria = emisiones_por_categoria.sort_values(
                by="Emision_CO2_avg", ascending=False
            )

            # 2. Crear el gráfico de barras con Plotly Express
            fig = px.bar(
                emisiones_por_categoria,
                x="MS_VehicleCategoryCode",
                y="Emision_CO2_avg",
                title="Emisiones Totales de CO2 por Categoría de Vehículo",
                labels={
                    "MS_VehicleCategoryCode": "Categoría de Vehículo",
                    "Emision_CO2_avg": "Emisiones de CO2 (g/km)",
                },
            )

            # 3. Mejorar la presentación del gráfico
            fig.update_layout(
                xaxis_tickangle=-45,  # Rotar las etiquetas del eje x
                bargap=0.2,  # Espacio entre barras
            )
            fig.update_traces(marker_color="skyblue")  # Color de las barras

            # 4. Mostrar el gráfico en Streamlit
            st.plotly_chart(fig)

        else:
            st.warning("No hay datos disponibles para mostrar.")
            st.stop()


    # Análisis textual en la columna col8
with col8:
        st.write("### Análisis:")
        if not emisiones_por_categoria.empty:
            # Obtener la categoría con mayores emisiones
            categoria_max = emisiones_por_categoria.iloc[0]["MS_VehicleCategoryCode"]
            max_emisiones = emisiones_por_categoria.iloc[0]["Emision_CO2_avg"]
            total_emisiones = emisiones_por_categoria["Emision_CO2_avg"].sum()
            porcentaje_max = (max_emisiones / total_emisiones) * 100

            # Mostrar el análisis con valores calculados
            st.write(
                f"Este gráfico muestra las **emisiones totales de CO2** por cada categoría de vehículo. "
                f"Se puede observar que la categoría **{categoria_max}** presenta las mayores emisiones, "
                f"representando el **{porcentaje_max:.2f}%** de las emisiones totales."
            )
        else:
            st.write("No hay datos suficientes para realizar el análisis.")

        # Mostrar la tabla con los datos calculados
        st.dataframe(emisiones_por_categoria)

st.write("---")
st.write("   ")
st.write("   ")

st.header("Análisis integral del consumo de combustible")

    # Dividir la página en tres columnas
col9, col10, col11 = st.columns(3)

    # Gráfica 1: Relación entre consumo y carga transportada
with col9:
        st.subheader("Consumo vs Carga")
        fig1 = px.scatter(
            emisiones_df,
            x="L_Payload_kg",
            y="Consumo_avg",
            size="Emision_CO2_avg",
            color="MS_FuelType",
            hover_data=["OEM_Model", "Mission"],
            title="Carga vs Consumo",
            labels={"L_Payload_kg": "Carga (kg)", "Consumo_avg": "Consumo Promedio (L/100km)"}
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfica 2: Comparación por tipo de combustible
with col10:
        st.subheader("Consumo y emisiones por combustible")
        consumo_emisiones_combustible = emisiones_df.groupby("MS_FuelType")[["Consumo_avg", "Emision_CO2_avg"]].mean().reset_index()
        fig2 = px.bar(
            consumo_emisiones_combustible,
            x="MS_FuelType",
            y=["Consumo_avg", "Emision_CO2_avg"],
            barmode="group",
            title="Consumo y CO2 por combustible",
            labels={"value": "Promedio", "variable": "Métrica", "MS_FuelType": "Tipo de Combustible"}
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Gráfica 3: Distribución del consumo promedio
with col11:
        st.subheader("Distribución del consumo")
        fig3 = px.histogram(
            emisiones_df,
            x="Consumo_avg",
            nbins=20,
            title="Distribución del consumo",
            labels={"Consumo_avg": "Consumo Promedio (L/100km)"},
            color_discrete_sequence=["green"]
        )
        st.plotly_chart(fig3, use_container_width=True)
        
st.subheader("Análisis de la relación entre consumo, carga y emisiones")
st.write("""
    1. **Consumo vs Carga**: Los vehículos con cargas más pesadas tienden a consumir más combustible, pero algunos presentan mayor eficiencia al transportar más carga con menor consumo.
    2. **Tipo de combustible**: El Diesel, aunque predominante, muestra un consumo y emisiones más elevados en promedio. Esto resalta la necesidad de explorar alternativas más limpias.
    3. **Distribución del consumo**: La mayoría de los vehículos tienen consumos concentrados en un rango específico, pero existen valores extremos que requieren mayor atención.
    """)

## Añadido recientemente

# Sección para calcular el nivel de emisión basado en una cantidad de vehículos
st.header("Cálculo de emisiones para una cantidad específica de vehículos")

# Obtener las 5 marcas con más referencias
top5_marcas = emisiones_df['OEM_Make'].value_counts().head(5).index.tolist()
st.write("Las **5 marcas con más referencias** en la base de datos son:", ", ".join(top5_marcas))

# Crear una selección de marca y textbox para la cantidad de vehículos
col15, col16 = st.columns(2)
with col15:
    marca_seleccionada = st.selectbox("Selecciona una marca de las 5 principales:", [""] + top5_marcas)

with col16:
    cantidad_vehiculos = st.number_input("Cantidad de vehículos a analizar:", min_value=1, value=10, step=1)

# Calcular las emisiones si la marca está seleccionada
if marca_seleccionada:
    # Filtrar por la marca seleccionada y calcular las emisiones promedio
    emisiones_marca = emisiones_df[emisiones_df['OEM_Make'] == marca_seleccionada]

    # Seleccionar las 5 referencias con menor emisión promedio
    top5_referencias = (
        emisiones_marca.groupby('OEM_Model')['Emision_CO2_avg']
        .mean()
        .nsmallest(5)
        .reset_index()
    )

    # Calcular emisiones totales para la cantidad seleccionada de vehículos
    top5_referencias['Emisiones Totales'] = top5_referencias['Emision_CO2_avg'] * cantidad_vehiculos

    # Mostrar resultados
    st.write(f"**Marca seleccionada:** {marca_seleccionada}")
    st.write(f"**Emisiones totales calculadas para las referencias de la marca:**")

    # Mostrar tabla con resultados
    st.table(top5_referencias.rename(columns={
        'OEM_Model': 'Modelo de Vehículo',
        'Emision_CO2_avg': 'Emisión Promedio (g/km)',
        'Emisiones Totales': 'Emisiones Totales (g/km)'
    }))

    # Gráfica interactiva con Plotly
    st.subheader("Top 5 referencias con menor emisión promedio de CO₂")
    import plotly.express as px

    fig = px.bar(
        top5_referencias,
        x='OEM_Model',
        y='Emisiones Totales',
        text='Emisiones Totales',
        title=f"Top 5 referencias con menor emisión en {marca_seleccionada}",
        labels={
            'OEM_Model': 'Modelo de Vehículo',
            'Emisiones Totales': 'Emisiones Totales (g/km)'
        },
        color='Emisiones Totales',  # Añadir un degradado de color
        color_continuous_scale='Blues'
    )

    # Ajustes adicionales para la gráfica
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        xaxis_title="Modelo de Vehículo",
        yaxis_title="Emisiones Totales (g/km)",
        xaxis_tickangle=-45
    )

    # Mostrar gráfica en Streamlit
    st.plotly_chart(fig)

else:
    st.info("Por favor selecciona una marca y la cantidad de vehículos para realizar el cálculo.")


## Métrica
# Calcular la referencia con menos y más emisiones
referencia_menor_emision = top5_referencias.iloc[0]
referencia_mayor_emision = top5_referencias.iloc[-1]

# Métricas
# Calcular la referencia con menos y más emisiones
referencia_menor_emision = top5_referencias.iloc[0]
referencia_mayor_emision = top5_referencias.iloc[-1]

# Métricas
st.subheader("Resumen de Emisiones")

col17, col18 = st.columns(2)

with col17:
    st.metric(
        label="Referencia con menores emisiones",
        value=f"{referencia_menor_emision['OEM_Model']} ({referencia_menor_emision['Emision_CO2_avg']:.2f} g/km)"
    )

with col18:
    delta_emision = referencia_mayor_emision['Emision_CO2_avg'] - referencia_menor_emision['Emision_CO2_avg']
    promedio_emisiones = top5_referencias['Emision_CO2_avg'].mean()
    
    st.metric(
        label="Comparación promedio vs mayor emisión",
        value=f"{promedio_emisiones:.2f} g/km",
        delta=f"{-delta_emision:.2f} g/km respecto a {referencia_mayor_emision['OEM_Model']}"
    )

st.subheader("Análisis de emisiones de CO₂ por referencia de vehículos")
st.write("""El análisis presentado se centra en la comparación de las 5 referencias de vehículos con menor emisión de CO₂ dentro de la marca seleccionada. Se calcularon las emisiones totales para una cantidad específica de vehículos, facilitando así la evaluación del impacto ambiental a escala.

Referencia con menores emisiones:
La referencia {modelo_menor_emision} destaca por registrar la menor emisión promedio, con {emision_menor:.2f} g/km, lo que representa una reducción de {abs(delta):.2f} g/km en comparación con la referencia que más emite, {modelo_mayor_emision}.

Tendencia general:
Las referencias analizadas muestran una significativa variabilidad en sus niveles de emisiones. La diferencia entre la referencia más eficiente y la de mayor emisión resalta oportunidades de optimización en el desempeño ambiental de la flota vehicular.

Impacto acumulado:
Al considerar una cantidad determinada de vehículos, se evidenció el impacto acumulativo de las emisiones totales. Esta métrica permite a los responsables de flotas y tomadores de decisiones identificar modelos más sostenibles y promover su adopción a gran escala.
         """)

## Emisiones Medellín
# Sección para comparar las emisiones con el nivel de emisiones de Medellín
st.header("Comparación de emisiones con el nivel de emisiones de Medellín")

# Input: Nivel de emisiones de Medellín (en toneladas)
emisiones_medellin = st.number_input(
    "Ingresa el nivel de emisiones de Medellín (en toneladas de CO₂):", 
    min_value=0.0, 
    value=10000.0,  # Ejemplo: 10,000 toneladas
    step=100.0
)

# Input: Recorrido diario promedio en kilómetros
recorrido_diario = st.number_input(
    "Ingresa el recorrido promedio diario de los vehículos (en km):", 
    min_value=1, 
    value=100, 
    step=10
)

if marca_seleccionada and cantidad_vehiculos:
    # Calcular emisiones totales diarias de la cantidad de vehículos seleccionados
    emision_total_diaria = top5_referencias['Emision_CO2_avg'].mean() * cantidad_vehiculos * recorrido_diario
    emision_total_toneladas = emision_total_diaria / 1_000_000  # Convertir a toneladas

    # Relación entre las emisiones de los vehículos seleccionados y las de Medellín
    porcentaje_emisiones = (emision_total_toneladas / emisiones_medellin) * 100

    # Mostrar resultados
    st.write("### Resultados del análisis:")
    st.metric(
        label="Emisiones totales diarias de los vehículos seleccionados",
        value=f"{emision_total_toneladas:.2f} toneladas de CO₂",
        delta=f"{porcentaje_emisiones:.2f}% del total de Medellín"
    )

    # Gráfica comparativa con Plotly
    st.subheader("Comparación gráfica de emisiones")
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Emisiones de los vehículos seleccionados", "Nivel de emisiones de Medellín"],
        y=[emision_total_toneladas, emisiones_medellin],
        text=[f"{emision_total_toneladas:.2f} toneladas", f"{emisiones_medellin:.2f} toneladas"],
        textposition='auto',
        marker_color=['skyblue', 'lightgreen']
    ))

    fig.update_layout(
        title="Comparación de emisiones entre vehículos seleccionados y Medellín",
        xaxis_title="Fuente de emisiones",
        yaxis_title="Toneladas de CO₂",
        showlegend=False
    )

    st.plotly_chart(fig)

    # Interpretación
    st.write("### Interpretación del análisis")
    st.write(f"""
        - Las emisiones totales de los **{cantidad_vehiculos} vehículos seleccionados**, 
          recorriendo un promedio de **{recorrido_diario} km/día**, equivalen a **{emision_total_toneladas:.2f} toneladas de CO₂ por día**.
        - Esto representa aproximadamente un **{porcentaje_emisiones:.2f}%** del nivel total de emisiones registrado en Medellín, 
          que se estima en **{emisiones_medellin} toneladas**.
    """)
else:
    st.info("Por favor, selecciona una marca, la cantidad de vehículos y proporciona los datos para realizar la comparación.")

    
## Botones
st.write("---")
st.write("   ")

col12, col13, col14 = st.columns([1,1,5])

with col12:
    btnNacional = st.button('Datos nacionales')
with col13:
    btnInicio = st.button('Inicio')

if btnNacional:
    st.switch_page('pages/nacional.py')

if btnInicio:
    st.switch_page('main.py')