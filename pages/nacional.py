import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import utilidades as util

# Título e icono de la página
st.set_page_config(page_title="Trayecto nacional", page_icon="🗺️", layout="wide")
util.generarMenu()

df = pd.read_csv("BDVehiculosLHOK.csv")

st.title('Análisis de Datos de Vehículos con recorridos de Larga Distancia')
st.header("Recorridos de larga distancia")

st.write("El transporte de larga distancia (Long Haul) se refiere a operaciones logísticas donde los vehículos recorren trayectos extensos, generalmente superiores a 150 kilómetros, transportando grandes volúmenes de carga entre ciudades, regiones o incluso países. Este tipo de transporte es fundamental en cadenas de suministro globales, conectando centros de producción, distribución y consumo.")
st.image("https://www.scania.com/content/www/uk/en/home/products/attributes/fuel-efficiency/_jcr_content/image.img.90.360.jpeg", caption="Imagen desde URL:https://www.scania.com/content/www/uk/en/home/products/attributes/fuel-efficiency/_jcr_content/image.img.90.360.jpeg")

st.markdown("**A continuación, se presenta un análisis detallado de los datos relacionados con escenarios de transporte de larga distancia. Este análisis se centra en características clave como el consumo de combustible, las emisiones de CO₂, el rendimiento operacional y las condiciones de carga de los vehículos, proporcionando una visión integral del desempeño en diversas misiones y configuraciones.**")

# Definición de las columnas

st.header("Descripción de los campos")

columnas = {
    'OEM_Make': 'Marca del fabricante del vehículo.',
    'OEM_Model': 'Modelo del vehículo fabricado por el OEM (Original Equipment Manufacturer).',
    'MS_VehicleCategoryCode': 'Código de la categoría del vehículo según el fabricante.',
    'MS_FuelType': 'Tipo de combustible utilizado por el vehículo (por ejemplo, diésel, gasolina, gas, biodiésel).',
    'LHL_Mission': 'Tipo de misión de transporte en el escenario de larga distancia ligero (LHL).',
    'LHL_TotalVehicleMass_kg': 'Masa total del vehículo en kilogramos con carga incluido',
    'LHL_Payload_kg': 'Peso de la carga transportada en el vehículo en kilogramos.',
    'LHL_AverageSpeed_kmh': 'Velocidad promedio del vehículo en kilómetros por hora (km/h).',
    'LHL_MaxSpeed_kmh': 'Velocidad máxima alcanzada por el vehículo en kilómetros por hora (km/h).',
    'LHL_CO2_gkm': 'Emisiones de CO₂ por kilómetro recorrido en gramos (g/km).',
    'LHL_FuelConsumption_l100km': 'Consumo de combustible en litros por cada 100 kilómetros (L/100km).',
    'LHR_Mission': 'Tipo de misión de transporte en el escenario de larga distancia regular (LHR).',
    'LHR_TotalVehicleMass_kg': 'Masa total del vehículo en kilogramos en el escenario LHR con carga incluida.',
    'LHR_Payload_kg': 'Peso de la carga transportada en el vehículo en kilogramos en el escenario LHR.',
    'LHR_AverageSpeed_kmh': 'Velocidad promedio del vehículo en kilómetros por hora (km/h) en el escenario LHR.',
    'LHR_MaxSpeed_kmh': 'Velocidad máxima alcanzada por el vehículo en kilómetros por hora (km/h) en el escenario LHR.',
    'LHR_CO2_gkm': 'Emisiones de CO₂ por kilómetro recorrido en gramos (g/km) en el escenario LHR.',
    'LHR_FuelConsumption_l100km': 'Consumo de combustible en litros por cada 100 kilómetros (L/100km) en el escenario LHR.'
}

# Mostrar las columnas y sus definiciones
for col, defn in columnas.items():st.markdown(f"**{col}:** {defn}")

# Mostrar las estadísticas descriptivas del dataframe

st.write("A continuación se muestran los datos estadísticos del dataframe:")
estadisticas = df.describe().T
st.dataframe(estadisticas)  # Muestra el dataframe en Streamlit

# Título en Streamlit
st.header("Análisis gráfico vehículos con recorridos de larga distancia")
st.write("**Gráfico que muestra las emisiones de CO2 por tipo de vehículo y por marca**")

# Agrupar por tipo de vehículo y marca y calcular las emisiones promedio de CO2 LHL y LHR
Emisiones_marca_tVeh = df.groupby(['MS_VehicleCategoryCode', 'OEM_Make'])[['LHL_CO2_gkm', 'LHR_CO2_gkm']].mean().reset_index()
# Ordenar el DataFrame por tipo de vehículo y por las menores emisiones LHL y LHR
Emisiones_marca_tVeh = Emisiones_marca_tVeh.sort_values(by=['MS_VehicleCategoryCode', 'LHL_CO2_gkm', 'LHR_CO2_gkm'])

# Crear una fila con dos columnas para mostrar los gráficos y las conclusiones
col1, col2, col3 = st.columns(3)

# Primer gráfico: Emisiones de CO2 LHL
with col1:
    # Crear el gráfico de barras para LHL
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='MS_VehicleCategoryCode', y='LHL_CO2_gkm', hue='OEM_Make', data=Emisiones_marca_tVeh, ax=ax)
    ax.set_xlabel('Tipo de Vehículo')
    ax.set_ylabel('Emisiones de CO2 (g/km)')
    ax.set_title('Ranking de Emisiones de CO2 LHL por Marca para cada Tipo de Vehículo')
    ax.legend(title='Marca')

    #Ajustar Labels
    plt.tight_layout()

    st.pyplot(fig)
    
    # Texto debajo del gráfico LHL
    st.markdown("**Gráfico LHL (Long Haul)**: Emisiones de CO2 por tipo de vehículo y marca para LHL.")

# Segundo gráfico: Emisiones de CO2 LHR
with col2:
    # Crear el gráfico de barras para LHR
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='MS_VehicleCategoryCode', y='LHR_CO2_gkm', hue='OEM_Make', data=Emisiones_marca_tVeh, ax=ax)
    ax.set_xlabel('Tipo de Vehículo')
    ax.set_ylabel('Emisiones de CO2 (g/km)')
    ax.set_title('Ranking de Emisiones de CO2 LHR por Marca para cada Tipo de Vehículo')
    ax.legend(title='Marca')

    #Ajustar Labels
    plt.tight_layout()

    st.pyplot(fig)
    
    # Texto debajo del gráfico LHR
    st.markdown("**Gráfico LHR (Long Haul Return)**: Emisiones de CO2 por tipo de vehículo y marca para LHR.")

# Conclusión
with col3:
    st.write("""
        "Inicialmente, se observa que no existe una variación pronunciada en las emisiones de CO2 entre los distintos escenarios,
        tanto para LHL como para LHR. Sin embargo, se puede apreciar que los camiones Scania presentan las menores emisiones de 
        CO2 en ambos escenarios (LHL y LHR) para los vehículos de tipo N3 (vehículos con un peso bruto superior a 12 toneladas). 
        Por otro lado, Renault destaca por sus bajas emisiones en las categorías M1 y M3, que corresponden al transporte de pasajeros."

    """)

# Título en Streamlit
st.write("**Gráfico que muestra el consumo de combustible (lts/100km) por tipo de vehículo y por marca**")

# Agrupar por tipo de vehículo y marca y calcular el consumo promedio de combustible LHL y LHR
Consumo_marca_tVeh = df.groupby(['MS_VehicleCategoryCode', 'OEM_Make'])[['LHL_FuelConsumption_l100km', 'LHR_FuelConsumption_l100km']].mean().reset_index()

# Ordenar el DataFrame por tipo de vehículo y por el menor consumo LHL y LHR
Consumo_marca_tVeh = Consumo_marca_tVeh.sort_values(by=['MS_VehicleCategoryCode', 'LHL_FuelConsumption_l100km', 'LHR_FuelConsumption_l100km'])

# Crear una fila con tres columnas para mostrar los gráficos y las conclusiones
col1, col2, col3 = st.columns(3)

# Primer gráfico: Consumo de combustible LHL
with col1:
    # Crear el gráfico de barras para LHL
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='MS_VehicleCategoryCode', y='LHL_FuelConsumption_l100km', hue='OEM_Make', data=Consumo_marca_tVeh, ax=ax)
    ax.set_xlabel('Tipo de Vehículo')
    ax.set_ylabel('Consumo de Combustible (L/100 km)')
    ax.set_title('Ranking de Consumo de Combustible LHL por Marca para cada Tipo de Vehículo')
    ax.legend(title='Marca')

    #Ajustar Labels
    plt.tight_layout()

    st.pyplot(fig)
    
    # Texto debajo del gráfico LHL
    st.markdown("**Gráfico LHL (Long Haul)**: Consumo de combustible por tipo de vehículo y marca para LHL.")

# Segundo gráfico: Consumo de combustible LHR
with col2:
    # Crear el gráfico de barras para LHR
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='MS_VehicleCategoryCode', y='LHR_FuelConsumption_l100km', hue='OEM_Make', data=Consumo_marca_tVeh, ax=ax)
    ax.set_xlabel('Tipo de Vehículo')
    ax.set_ylabel('Consumo de Combustible (L/100 km)')
    ax.set_title('Ranking de Consumo de Combustible LHR por Marca para cada Tipo de Vehículo')
    ax.legend(title='Marca')

    #Ajustar Labels
    plt.tight_layout()

    
    st.pyplot(fig)
    
    # Texto debajo del gráfico LHR
    st.markdown("**Gráfico LHR (Long Haul Return)**: Consumo de combustible por tipo de vehículo y marca para LHR.")

# Conclusión
with col3:
    st.write("""
        "Este análisis presenta el consumo de combustible de los vehículos en dos escenarios. Las gráficas muestran un patrón similar
         al de las emisiones de CO2, evidenciando que los vehículos con menor consumo de combustible también registran las menores 
         emisiones de CO2. Esto sugiere una relación directa entre la eficiencia en el consumo de combustible y las emisiones
    """)

# Calcular el coeficiente de correlación de Pearson para LHL
correlation_lhl = df['LHL_FuelConsumption_l100km'].corr(df['LHL_CO2_gkm'])

# Calcular el coeficiente de correlación de Pearson para LHR
correlation_lhr = df['LHR_FuelConsumption_l100km'].corr(df['LHR_CO2_gkm'])

# Título del análisis en Streamlit
st.header("Análisis de Correlación entre Consumo de Combustible y Emisiones de CO2")

# Mostrar los resultados en Streamlit
st.write(f"**Correlación entre Consumo de Combustible y Emisiones de CO2 (LHL):** {correlation_lhl:.2f}")
st.write(f"**Correlación entre Consumo de Combustible y Emisiones de CO2 (LHR):** {correlation_lhr:.2f}")

# Interpretación de los resultados
st.write("""
    Se ha identificado una correlación directa entre el consumo de combustible y las emisiones de CO2,
    lo que sugiere que a mayor consumo de combustible, mayores son las emisiones de CO2. Este patrón resalta
    la importancia de optimizar el consumo de combustible como una estrategia para reducir las emisiones contaminantes.
""")

# Calcular métricas promedio por marca para LHL
eficiencia_marcas_lhl = df.groupby('OEM_Make').agg(
    Consumo_FuelPromedio_LHL=('LHL_FuelConsumption_l100km', 'mean'),
    Emisiones_Promedio_LHL=('LHL_CO2_gkm', 'mean')
).reset_index()

# Calcular métricas promedio por marca para LHR
eficiencia_marcas_lhr = df.groupby('OEM_Make').agg(
    Consumo_FuelPromedio_LHR=('LHR_FuelConsumption_l100km', 'mean'),
    Emisiones_Promedio_LHR=('LHR_CO2_gkm', 'mean')
).reset_index()

# Ordenar las marcas por menor consumo de combustible para LHL
eficiencia_marcas_lhl = eficiencia_marcas_lhl.sort_values('Consumo_FuelPromedio_LHL')

# Ordenar las marcas por menor consumo de combustible para LHR
eficiencia_marcas_lhr = eficiencia_marcas_lhr.sort_values('Consumo_FuelPromedio_LHR')

# Crear una fila con tres columnas para los gráficos y las conclusiones
col1, col2 = st.columns(2)

# Primer gráfico: Consumo y emisiones para LHL
with col1:
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Barras para consumo promedio de combustible LHL
    sns.barplot(data=eficiencia_marcas_lhl, x='OEM_Make', y='Consumo_FuelPromedio_LHL', color='blue', alpha=0.7, label='Consumo Promedio LHL (l/100km)', ax=ax1)
    ax1.set_ylabel('Consumo Promedio LHL (l/100km)', color='blue')
    ax1.set_xlabel('Marca')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xticklabels(eficiencia_marcas_lhl['OEM_Make'], rotation=45, ha='right')

    # Eje secundario para emisiones promedio LHL
    ax2 = ax1.twinx()
    sns.lineplot(data=eficiencia_marcas_lhl, x='OEM_Make', y='Emisiones_Promedio_LHL', color='red', label='Emisiones Promedio LHL (CO₂ g/km)', marker='o', ax=ax2)
    ax2.set_ylabel('Emisiones Promedio LHL (CO₂ g/km)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Añadir leyendas y título
    fig.suptitle('Marcas Más Eficientes en Consumo de Combustible LHL vs. Emisiones de CO₂ LHL', fontsize=16)
    ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))
    ax2.legend(loc='upper right', bbox_to_anchor=(1, 1))

    #Ajustar Labels
    plt.tight_layout()

    st.pyplot(fig)

# Segundo gráfico: Consumo y emisiones para LHR
with col2:
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Barras para consumo promedio de combustible LHR
    sns.barplot(data=eficiencia_marcas_lhr, x='OEM_Make', y='Consumo_FuelPromedio_LHR', color='green', alpha=0.7, label='Consumo Promedio LHR (l/100km)', ax=ax1)
    ax1.set_ylabel('Consumo Promedio LHR (l/100km)', color='green')
    ax1.set_xlabel('Marca')
    ax1.tick_params(axis='y', labelcolor='green')
    ax1.set_xticklabels(eficiencia_marcas_lhr['OEM_Make'], rotation=45, ha='right')

    # Eje secundario para emisiones promedio LHR
    ax2 = ax1.twinx()
    sns.lineplot(data=eficiencia_marcas_lhr, x='OEM_Make', y='Emisiones_Promedio_LHR', color='orange', label='Emisiones Promedio LHR (CO₂ g/km)', marker='o', ax=ax2)
    ax2.set_ylabel('Emisiones Promedio LHR (CO₂ g/km)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    # Añadir leyendas y título
    fig.suptitle('Marcas Más Eficientes en Consumo de Combustible LHR vs. Emisiones de CO₂ LHR', fontsize=16)
    ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))
    ax2.legend(loc='upper right', bbox_to_anchor=(1, 1))

    #Ajustar Labels
    plt.tight_layout()

    st.pyplot(fig)

# Tercera columna: Conclusión
st.write("""
    **Conclusión:**
    Las gráficas revelan la relación entre las marcas y su rendimiento en términos de consumo de combustible
    y emisiones de CO₂. Se observa que Scania lidera en eficiencia, destacándose por su excelente autonomía y
    bajas emisiones de CO₂. Le siguen DAF, Volvo y MAN en cuanto a rendimiento, mientras que IVECO ocupa el último 
    lugar, con la menor autonomía y las mayores emisiones de CO₂.
    """)

# Título del análisis en Streamlit
st.header("Análisis de costo por kilometro recorrido para cada tipo de vehiculo y marca")

# Definir el costo del diésel por galón en COP
costo_diesel_por_galon = 10561  # COP

# Filtrar los vehículos diésel
df_diesel = df[df['MS_FuelType'] == 'Diesel'].copy()

# Convertir el consumo de l/100 km a galones/100 km para LHL
df_diesel['Consumo_por_galon_LHL'] = df_diesel['LHL_FuelConsumption_l100km'] / 3.78541
df_diesel['Costo_por_km_LHL'] = (df_diesel['Consumo_por_galon_LHL'] / 100) * costo_diesel_por_galon

# Convertir el consumo de l/100 km a galones/100 km para LHR
df_diesel['Consumo_por_galon_LHR'] = df_diesel['LHR_FuelConsumption_l100km'] / 3.78541
df_diesel['Costo_por_km_LHR'] = (df_diesel['Consumo_por_galon_LHR'] / 100) * costo_diesel_por_galon

# Agrupar por marca y tipo de vehículo y calcular el costo promedio por kilómetro para LHL y LHR
costo_por_km_por_marca_y_tipo = df_diesel.groupby(['OEM_Make', 'MS_VehicleCategoryCode'])[['Costo_por_km_LHL', 'Costo_por_km_LHR']].mean().reset_index()

# Renombrar columnas en español
costo_por_km_por_marca_y_tipo.columns = ['Marca', 'Tipo_de_Vehículo', 'Costo_promedio_por_km_LHL (COP)', 'Costo_promedio_por_km_LHR (COP)']

# Graficar los resultados usando Streamlit y seaborn

# Crear dos columnas en Streamlit
col1, col2 = st.columns(2)

# Gráfico para LHL
with col1:
    fig, ax1 = plt.subplots(figsize=(8, 6))
    
    # Graficar LHL por tipo de vehículo y marca
    sns.barplot(data=costo_por_km_por_marca_y_tipo, x='Tipo_de_Vehículo', y='Costo_promedio_por_km_LHL (COP)', hue='Marca', ax=ax1)
    
    # Títulos y etiquetas
    ax1.set_title('Costo Promedio por Kilómetro LHL (COP) por Tipo de Vehículo')
    ax1.set_xlabel('Tipo de Vehículo')
    ax1.set_ylabel('Costo Promedio por Km (COP)')
    ax1.set_xticklabels(costo_por_km_por_marca_y_tipo['Tipo_de_Vehículo'].unique(), rotation=45, ha='right')

    #Ajustar Labels
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

# Gráfico para LHR
with col2:
    fig, ax2 = plt.subplots(figsize=(8, 6))
    
    # Graficar LHR por tipo de vehículo y marca
    sns.barplot(data=costo_por_km_por_marca_y_tipo, x='Tipo_de_Vehículo', y='Costo_promedio_por_km_LHR (COP)', hue='Marca', ax=ax2)
    
    # Títulos y etiquetas
    ax2.set_title('Costo Promedio por Kilómetro LHR (COP) por Tipo de Vehículo')
    ax2.set_xlabel('Tipo de Vehículo')
    ax2.set_ylabel('Costo Promedio por Km (COP)')
    ax2.set_xticklabels(costo_por_km_por_marca_y_tipo['Tipo_de_Vehículo'].unique(), rotation=45, ha='right')
    
    #Ajustar Labels
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Definir el costo del diésel por galón en COP 
costo_diesel_por_galon = 10561  # COP

# Filtrar los vehículos diésel
df_diesel = df[df['MS_FuelType'] == 'Diesel'].copy()

# Convertir el consumo de l/100 km a galones/100 km para LHL
df_diesel['Consumo_por_galon_LHL'] = df_diesel['LHL_FuelConsumption_l100km'] / 3.78541
df_diesel['Costo_por_km_LHL'] = (df_diesel['Consumo_por_galon_LHL'] / 100) * costo_diesel_por_galon

# Convertir el consumo de l/100 km a galones/100 km para LHR
df_diesel['Consumo_por_galon_LHR'] = df_diesel['LHR_FuelConsumption_l100km'] / 3.78541
df_diesel['Costo_por_km_LHR'] = (df_diesel['Consumo_por_galon_LHR'] / 100) * costo_diesel_por_galon

# Agrupar por marca y tipo de vehículo y calcular el costo promedio por kilómetro
costo_por_km_por_marca_y_tipo = df_diesel.groupby(['OEM_Make', 'MS_VehicleCategoryCode'])[['Costo_por_km_LHL', 'Costo_por_km_LHR']].mean().reset_index()

# Ordenar de menor a mayor por costo por kilómetro para LHL y LHR
costo_por_km_por_marca_y_tipo_sorted_LHL = costo_por_km_por_marca_y_tipo.sort_values(by=['MS_VehicleCategoryCode', 'Costo_por_km_LHL'])
costo_por_km_por_marca_y_tipo_sorted_LHR = costo_por_km_por_marca_y_tipo.sort_values(by=['MS_VehicleCategoryCode', 'Costo_por_km_LHR'])

# Seleccionar la mejor marca (menor costo por km) por tipo de vehículo
mejores_marcas_LHL = costo_por_km_por_marca_y_tipo_sorted_LHL.groupby('MS_VehicleCategoryCode').first().reset_index()
mejores_marcas_LHR = costo_por_km_por_marca_y_tipo_sorted_LHR.groupby('MS_VehicleCategoryCode').first().reset_index()

# Unir los resultados de LHL y LHR
mejores_marcas = pd.merge(mejores_marcas_LHL[['MS_VehicleCategoryCode', 'OEM_Make', 'Costo_por_km_LHL']], 
                          mejores_marcas_LHR[['MS_VehicleCategoryCode', 'OEM_Make', 'Costo_por_km_LHR']], 
                          on='MS_VehicleCategoryCode')

# Renombrar columnas para mayor claridad
mejores_marcas.columns = ['Tipo_de_Vehículo', 'Marca_LHL', 'Costo_por_km_LHL (COP)', 'Marca_LHR', 'Costo_por_km_LHR (COP)']

# Mostrar la tabla de las mejores marcas por categoría y costo por km
st.write("### Mejores Marcas por Categoría (Menor Costo por Kilómetro)")
st.dataframe(mejores_marcas)

st.write("---")
st.write("   ")

col1, col2, col3 = st.columns([2,1,5])

with col1:
    btnElectricos = st.button('Vehículos eléctricos')
with col2:
    btnInicio = st.button('Inicio')

if btnElectricos:
    st.switch_page('pages/electricos.py')

if btnInicio:
    st.switch_page('main.py')