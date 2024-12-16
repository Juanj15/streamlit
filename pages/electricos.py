import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import utilidades as util

# Título e icono de la página
st.set_page_config(page_title="Vehículos eléctricos", page_icon="🔋", layout="wide")
util.generarMenu()

autos_eh = pd.read_csv("autos_eh.csv")

    # Encabezado y descripción
st.header("Análisis de autos eléctricos e híbridos")
st.write("Este análisis evalúa los datos de autos eléctricos e híbridos, analizando las motorizaciones, categorías y consumo para identificar patrones relevantes y comparaciones clave entre los tipos de vehículos.")
st.write("   ")

    # Análisis descriptivo
col1, col2 = st.columns([3, 1])

    
st.subheader("Vista general de los datos")
st.table(autos_eh.head())


st.subheader("Resumen estadístico")
st.table(autos_eh.describe())

st.write("---")
st.write("   ")

# Distribución por tipo de vehículo
st.header("Distribución por tipo de vehículo")

col3, col4 = st.columns([3, 1])

with col3:
        motorizaciones = autos_eh["Motorizacion"].value_counts().index
        frecuencias = autos_eh["Motorizacion"].value_counts().values
        colores = ["gold"] * len(motorizaciones)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(motorizaciones, frecuencias, color=colores)
        ax.set_title("Distribución por tipo de vehículo")
        ax.set_xlabel("Tipo")
        ax.set_ylabel("Frecuencia")
        ax.set_xticks(range(len(motorizaciones)))
        ax.set_xticklabels(motorizaciones, rotation=90)
        for i in range(len(motorizaciones)):
            ax.text(i, frecuencias[i] + 0.1, str(frecuencias[i]), ha='center', va='bottom', fontsize=8, rotation=90)

        st.pyplot(fig)

with col4:
        st.subheader("Tabla de Frecuencias")
        st.table(autos_eh["Motorizacion"].value_counts().rename_axis("Motorización").reset_index(name="Frecuencia"))

st.write("---")
st.write("   ")

# Análisis de vehículos eléctricos
st.header("Análisis de vehículos eléctricos")
Electricos = autos_eh[autos_eh["Motorizacion"] == "Eléctricos puros"]

col5, col6 = st.columns([2, 1])

with col5:
        categorias = Electricos["Categoria"].value_counts().index
        frecuencias = Electricos["Categoria"].value_counts().values
        colores = ["yellowgreen"] * len(categorias)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(categorias, frecuencias, color=colores)
        ax.set_title("Distribución por categoría de autos eléctricos")
        ax.set_xlabel("Categoría")
        ax.set_ylabel("Frecuencia")
        ax.set_xticks(range(len(categorias)))
        ax.set_xticklabels(categorias, rotation=90)
        for i in range(len(categorias)):
            ax.text(i, frecuencias[i] + 1, str(frecuencias[i]), ha='center', va='bottom', fontsize=8, rotation=90)

        st.pyplot(fig)

with col6:
        st.subheader("Tabla de Categorías")
        st.table(Electricos["Categoria"].value_counts().rename_axis("Categoría").reset_index(name="Frecuencia"))

st.write("---")
st.write("   ")

# Consumo eléctrico por categoría
st.subheader("Vehículos eléctricos con mayor y menor consumo en kWh/km por categoría")
Electricos.rename(columns={'Consumo_electrico_kWh/10km': 'Consumo_electrico_kWh/100km'}, inplace=True)
Electricos["Consumo_electrico_kWh/km"] = Electricos['Consumo_electrico_kWh/100km'] / 100

for i in Electricos["Categoria"].unique():
        E = Electricos[Electricos["Categoria"] == i]
        max_consumo = E["Consumo_electrico_kWh/km"].max()
        min_consumo = E["Consumo_electrico_kWh/km"].min()

        max_vehiculos = E[E["Consumo_electrico_kWh/km"] == max_consumo]["Modelo"].tolist()
        min_vehiculos = E[E["Consumo_electrico_kWh/km"] == min_consumo]["Modelo"].tolist()

        st.write(f"Categoría: *{i}*")
        st.write(f"- Mayor consumo: {', '.join(max_vehiculos)} ({max_consumo:.2f} kWh/km)")
        st.write(f"- Menor consumo: {', '.join(min_vehiculos)} ({min_consumo:.2f} kWh/km)")

st.write("---")
st.write("   ")

# Distribución del consumo eléctrico
st.header("Distribución del Consumo Eléctrico por Categoría")

col7, col8 = st.columns([1, 1])
with col7:
        fig = plt.figure(figsize=(4.5, 4.5))
        sns.boxplot(x="Categoria", y="Consumo_electrico_kWh/km", data=Electricos)
        plt.title("Distribución del Consumo Eléctrico por Categoría")
        plt.xlabel("Categoría")
        plt.ylabel("Consumo Eléctrico (kWh/km)")
        st.pyplot(fig)

with col8:
        fig = plt.figure(figsize=(6, 4))
        sns.violinplot(x="Categoria", y="Consumo_electrico_kWh/km", data=Electricos, inner="quartile", palette="muted")
        plt.title("Distribución del Consumo Eléctrico por Categoría")
        plt.xlabel("Categoría")
        plt.ylabel("Consumo Eléctrico (kWh/km)")
        st.pyplot(fig)

st.write("---")
st.write("   ")
    
col115,col116=st.columns(2)
with col115:
        st.header("Analisis carga")
        # Gráfico 1: Dispersión MTMA_Kg vs Consumo Eléctrico
        st.subheader("Relación entre MTMA (Kg) y Consumo Eléctrico (kWh/km)")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=Electricos, x="MTMA_Kg", y="Consumo_electrico_kWh/km", ax=ax)
        ax.set_title("MTMA vs Consumo Eléctrico")
        ax.set_xlabel("MTMA (Kg)")
        ax.set_ylabel("Consumo Eléctrico (kWh/km)")
        st.pyplot(fig)
        
        st.write("""
        ### Tendencia general:
        - Se observa que el consumo eléctrico (\(kWh/km\)) tiene una relación no lineal con el peso total del vehículo (\(MTMA\)).
        - Para vehículos de menor peso (\(< 5,000 \, Kg\)), existe una mayor variabilidad en el consumo eléctrico, con valores que pueden superar los \(2.5 \, kWh/km\).
        - A medida que el \(MTMA\) aumenta (\(> 10,000 \, Kg\)), los valores de consumo eléctrico tienden a estabilizarse en un rango más bajo (\(< 1.0 \, kWh/km\)).

        ### Interpretación:
        - Los vehículos ligeros suelen estar diseñados para aplicaciones urbanas o de corta distancia, lo que podría explicar su mayor consumo relativo debido a las constantes aceleraciones y frenados.
        - Los vehículos más pesados, aunque requieren más energía en términos absolutos, tienden a ser más eficientes por kilómetro recorrido en escenarios de larga distancia o velocidades constantes.
        """)

with col116:
        # Gráfico 2: Dispersión MTMA_Kg vs Autonomía
        st.subheader("Relación entre MTMA (Kg) y Autonomía (Km)")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=Electricos, x="MTMA_Kg", y="Autonomia_electrica_km", ax=ax, color="orange")
        ax.set_title("MTMA vs Autonomía")
        ax.set_xlabel("MTMA (Kg)")
        ax.set_ylabel("Autonomía Eléctrica (Km)")
        st.pyplot(fig)

    # Agregar texto explicativo
        st.write("""
            ### Tendencia general:
            - Para pesos más bajos (\(< 5,000 \, Kg\)), la autonomía varía significativamente, desde menos de \(100 \, Km\) hasta más de \(700 \, Km\).
            - A medida que el \(MTMA\) aumenta, la autonomía se concentra en un rango más estrecho (\(200 \, Km\) a \(400 \, Km\)).

            ### Interpretación:
            - Los vehículos ligeros probablemente están diseñados para tener mayor flexibilidad en autonomía, dependiendo de su tamaño de batería y su eficiencia.
            - Los vehículos más pesados parecen optimizados para aplicaciones específicas, donde la autonomía se ajusta a sus propósitos, como transporte de mercancías o pasajeros en rutas predefinidas.
            """)

col117,col118=st.columns(2)
with col117:
        # Gráfico 3: Comparación entre Autonomía y Consumo por MTMA
        st.subheader("Comparación de Autonomía y Consumo por MTMA")
        fig, ax1 = plt.subplots(figsize=(8, 6))
        sns.lineplot(data=Electricos, x="MTMA_Kg", y="Consumo_electrico_kWh/km", label="Consumo Eléctrico", ax=ax1)
        sns.lineplot(data=Electricos, x="MTMA_Kg", y="Autonomia_electrica_km", label="Autonomía Eléctrica", ax=ax1)
        ax1.set_title("MTMA vs Autonomía y Consumo")
        ax1.set_xlabel("MTMA (Kg)")
        ax1.set_ylabel("Valores")
        ax1.legend()
        st.pyplot(fig)

with col118:

        # Gráfico 4: Matriz de correlación
        st.subheader("Matriz de correlación entre variables numéricas")
        fig, ax = plt.subplots(figsize=(8, 6))
        correlation_matrix = Electricos[["MTMA_Kg", "Consumo_electrico_kWh/km", "Autonomia_electrica_km"]].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Matriz de Correlación")
        st.pyplot(fig)

    
from scipy.stats import zscore

  
Electricos['z_score'] = zscore(Electricos['Consumo_electrico_kWh/km'])

# Filtrar datos sin valores atípicos (por ejemplo, z-score entre -3 y 3)
Electricos = Electricos[(Electricos['z_score'] >= -3) & (Electricos['z_score'] <= 3)]
    
st.header("Precio de KWh en algunos vehiculos electricos")
    
# Datos de los camiones
camiones = [
        {
            "nombre": "Mercedes Benz eActross",
            "capacidad_carga_kg": 40000,
            "capacidad_bateria_kWh": 600,
            "autonomia_km": 500,
            "consumo_kWh_por_km": 1.19,
            "tiempo_carga_horas": 0.833333333,
            "costo_por_kWh_COP": 1051,
        },
        {
            "nombre": "Tesla Semi",
            "capacidad_carga_kg": 22000,
            "capacidad_bateria_kWh": 900,
            "autonomia_km": 800,
            "consumo_kWh_por_km": 1.1,
            "tiempo_carga_horas": 0.714285714,
            "costo_por_kWh_COP": 1051,
        },
    ]

    # Cálculo del costo por kilómetro
def calcular_costo_por_km(camion):
        consumo_por_km = camion["consumo_kWh_por_km"]
        costo_por_kWh = camion["costo_por_kWh_COP"]
        return consumo_por_km * costo_por_kWh

# Crear un DataFrame con los datos y resultados
data = []
for camion in camiones:
        costo_por_km = calcular_costo_por_km(camion)
        data.append({
            "Camión": camion["nombre"],
            "Capacidad de carga (kg)": camion["capacidad_carga_kg"],
            "Capacidad de batería (kWh)": camion["capacidad_bateria_kWh"],
            "Autonomía (km)": camion["autonomia_km"],
            "Consumo (kWh/km)": camion["consumo_kWh_por_km"],
            "Tiempo de carga (hrs)": camion["tiempo_carga_horas"],
            "Costo por kWh (COP)": camion["costo_por_kWh_COP"],
            "Costo por km (COP)": round(costo_por_km, 2),
        })

df = pd.DataFrame(data)

st.subheader("Tabla de datos y resultados")
st.table(df)

# Análisis de vehículos híbridos
st.header("Análisis de vehículos híbridos")
    
Hibridos = autos_eh[autos_eh['Motorizacion'].str.contains('híbridos', case=False, na=False)]
Hibridos.rename(columns={'Consumo_electrico_kWh/10km': 'Consumo_combustible_l/100km'}, inplace=True)

col9, col10 = st.columns([2, 1])

with col9:
        categorias = Hibridos["Categoria"].value_counts().index
        frecuencias = Hibridos["Categoria"].value_counts().values
        colores = ["skyblue"] * len(categorias)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(categorias, frecuencias, color=colores)
        ax.set_title("Distribución por categoría de autos híbridos")
        ax.set_xlabel("Categoría")
        ax.set_ylabel("Frecuencia")
        ax.set_xticks(range(len(categorias)))
        ax.set_xticklabels(categorias, rotation=90)
        for i in range(len(categorias)):
            ax.text(i, frecuencias[i] + 1, str(frecuencias[i]), ha='center', va='bottom', fontsize=8, rotation=90)

        st.pyplot(fig)

with col10:
        st.subheader("Tabla de Categorías")
        st.table(Hibridos["Categoria"].value_counts().rename_axis("Categoría").reset_index(name="Frecuencia"))

st.write("---")

# Vehículos híbridos: Consumo
st.subheader("Vehículos híbridos con mayor y menor consumo en L/100km por categoría")

for i in Hibridos["Categoria"].unique():
        E = Hibridos[Hibridos["Categoria"] == i]
        max_consumo = E["Consumo_combustible_l/100km"].max()
        min_consumo = E["Consumo_combustible_l/100km"].min()

        max_vehiculos = E[E["Consumo_combustible_l/100km"] == max_consumo]["Modelo"].tolist()
        min_vehiculos = E[E["Consumo_combustible_l/100km"] == min_consumo]["Modelo"].tolist()

        st.write(f"Categoría: *{i}*")
        st.write(f"- Mayor consumo: {', '.join(max_vehiculos)} ({max_consumo:.2f} L/100km)")
        st.write(f"- Menor consumo: {', '.join(min_vehiculos)} ({min_consumo:.2f} L/100km)")

st.write("---")
st.write("   ")

# Distribución del consumo híbrido
st.header("Distribución del Consumo de Combustible por Categoría")

col11, col12 = st.columns([1, 1])

with col11:
        fig = plt.figure(figsize=(4.5, 4.5))
        sns.boxplot(x="Categoria", y="Consumo_combustible_l/100km", data=Hibridos)
        plt.title("Distribución del Consumo de Combustible por Categoría")
        plt.xlabel("Categoría")
        plt.ylabel("Consumo (L/100km)")
        st.pyplot(fig)

with col12:
        fig = plt.figure(figsize=(6, 4))
        sns.violinplot(x="Categoria", y="Consumo_combustible_l/100km", data=Hibridos, inner="quartile", palette="muted")
        plt.title("Distribución del Consumo de Combustible por Categoría")
        plt.xlabel("Categoría")
        plt.ylabel("Consumo (L/100km)")
        st.pyplot(fig)

st.write("---")

# Mostrar tabla
st.table(df)
Hibridos['z_score'] = zscore(Hibridos['Consumo_combustible_l/100km'])

# Filtrar datos sin valores atípicos (por ejemplo, z-score entre -3 y 3)
Hibridos = Hibridos[(Hibridos['z_score'] >= -3) & (Hibridos['z_score'] <= 3)]

# Análisis adicional: autonomía
st.subheader("Análisis de autonomía por categoría")

for i in Hibridos["Categoria"].unique():
        E = Hibridos[Hibridos["Categoria"] == i]
        max_autonomia = E["Autonomia_electrica_km"].max()
        min_autonomia = E["Autonomia_electrica_km"].min()

        max_vehiculos = E[E["Autonomia_electrica_km"] == max_autonomia]["Modelo"].tolist()
        min_vehiculos = E[E["Autonomia_electrica_km"] == min_autonomia]["Modelo"].tolist()

        st.write(f"Categoría: *{i}*")
        st.write(f"- Mayor autonomía: {', '.join(max_vehiculos)} ({max_autonomia:.2f} km)")
        st.write(f"- Menor autonomía: {', '.join(min_vehiculos)} ({min_autonomia:.2f} km)")

st.write("---")
    
st.header("Analisis consumo combustible, emisiones")
Hibridos["Consumo promedio"]=(Hibridos['Consumo Máximo']+Hibridos['Consumo Mínimo'])/2
Hibridos["Emisiones promedio"]=(Hibridos['Emisiones Mínimo']+Hibridos['Emisiones Máximo'])/2

col111, col112 = st.columns([1, 1])
    
with col111:
        # Gráfico de dispersión entre Emisiones y Consumo
        fig,ax=plt.subplots()
        plt.scatter(Hibridos['Consumo promedio'], Hibridos['Emisiones promedio'], alpha=0.6)
        plt.title('Relación entre Emisiones y Consumo en Vehículos Híbridos')
        plt.xlabel('Consumo Promedio (L/100 km )')
        plt.ylabel('Emisiones Promedio (g CO2/km)')
        plt.grid(True)
        st.pyplot(fig)
with col112:
        st.header("Análisis")
        st.text("Hay una correlación positiva entre el consumo promedio de combustible (L/100 km) y las emisiones promedio (g CO₂/km). Esto significa que a medida que aumenta el consumo promedio de combustible, las emisiones de CO₂ también aumentan.")
    
key_variables = ['Consumo promedio', 'Autonomia_electrica_km', 'Emisiones promedio']

col113, col114 = st.columns(2)

# Definir las variables clave para el análisis
key_variables = ['Consumo promedio', 'Autonomia_electrica_km', 'Emisiones promedio']

# Verificar que las variables clave estén presentes en el DataFrame
missing_vars = [var for var in key_variables if var not in Hibridos.columns]
if missing_vars:
        st.write(f"Las siguientes variables clave faltan en el DataFrame: {', '.join(missing_vars)}")
else:
        
# Pairplot en la primera columna
        with col113:
            st.subheader("Pairplot de Variables Clave")
            pairplot_fig = sns.pairplot(
                Hibridos[key_variables].dropna(),
                diag_kind='kde',
                plot_kws={'alpha': 0.7}
            )
            pairplot_fig.fig.suptitle('Pairplot de Variables Clave', y=1.02)  # Ajustar el título
            st.pyplot(pairplot_fig)

        # Matriz de correlación en la segunda columna
        with col114:
            st.subheader("Matriz de Correlación")
            correlation_matrix = Hibridos[key_variables].corr()

            fig, ax = plt.subplots(figsize=(8, 6))  # Tamaño ajustado para mejor visibilidad
            sns.heatmap(
                correlation_matrix,
                annot=True,
                cmap='coolwarm',
                fmt='.2f',
                linewidths=0.5,
                cbar_kws={'label': 'Correlación'}
            )
            ax.set_title('Matriz de Correlación (Consumo, Emisiones, Autonomía)', fontsize=14)
            st.pyplot(fig)
        
        st.text("""Consumo promedio: Su distribución está concentrada cerca de valores bajos (cercanos a 0), indicando que la mayoría de los vehículos tienen un consumo promedio eficiente.
                Autonomía eléctrica (km): La distribución está altamente concentrada en un rango bajo, con unos pocos valores que alcanzan los 400 km, sugiriendo que la mayoría de los vehículos tienen una autonomía limitada.
                Emisiones promedio: Similar al Consumo promedio, la mayoría de los vehículos tienen bajas emisiones, aunque hay valores atípicos en el rango de 100-200 g CO₂/km""")

st.write("---")
st.write("   ")

col115, col116 = st.columns([1,5])

with col115:
    btnInicio = st.button('Inicio')

if btnInicio:
    st.switch_page('main.py')