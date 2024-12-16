import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import utilidades as util

# Título e icono de la página
st.set_page_config(page_title="Trayecto urbano", page_icon="🏙️", layout="wide")
util.generarMenu()

 # Cargar los datos
dfu = pd.read_csv('datos_vehiculo_urbano.csv')
# Crear DataFrame
dfu = pd.DataFrame(dfu)

st.header("TABLA CON LOS DATOS DE LAS MARCAS DE VEHICULOS")
# Calcular la carga promedio
dfu['Carga_Promedio'] = (dfu['R_Payload_kg'])

# Calcular la emisión promedio de CO2
dfu['Emision_CO2'] = (dfu['R_CO2_gkm'] )

# Calcular el consumo específico promedio
dfu['Consumo_Especifico'] = (dfu['Cs_R_Gal_km_Ton'] )

# Agrupar los datos por categoría de vehículo y marca
dfu_agrupado = dfu.groupby(['OEM_Make']).agg({
        'Carga_Promedio': 'max',
        'Emision_CO2': 'max',
        'Consumo_Especifico': 'max',
        'precio_total_COP_Gal_km': 'max'
    }).reset_index()

    # Renombrar las columnas para mayor claridad
dfu_agrupado.columns = [
        'Marca',
        'Carga_vehiculo',
        'Emision_CO2',
        'Consumo_Especifico',
        'Costo_Consumo_Combustible'
    ]

# Mostrar las primeras filas de los datos
st.table(dfu_agrupado)

# Crear columnas para mostrar gráficos
col11, col12 = st.columns(2) 
col13, col14 = st.columns(2)              
col15,col16=st.columns(2)
col17,col18=st.columns(2)
    
with col11:
        st.header("GRAFICO DEL CONSUMO DE CO2")
        # Sort the DataFrame by price in ascending order
        dfu_sorted = dfu.sort_values('precio_total_COP_Gal_km')

        # Create the bar plot
        fig,ax= plt.subplots(figsize=(5, 3))
        dfu_sorted.groupby('OEM_Make')['precio_total_COP_Gal_km'].mean().plot(kind='bar')
        plt.xlabel('Marca de Vehículo')
        plt.ylabel('Costo COP (Gal/km)')
        plt.title('Costo Promedio de Combustible por Marca')
        plt.xticks(rotation=90)  # Rotate x-axis labels
        st.pyplot(fig)
with col12: 
    # mostrar datos en tabla de precios de combustible por km de marcas de vehiculos menos costosas
        
    # Seleccionar las columnas relacionadas con el costo del combustible
        st.header("TABLAS DEL CONSUMO DE CO2")
        st.subheader("Hallazgos")
        st.write(" Los vehículos de marca Mitsubishi e Isuzu tienen 25% aproximadamente menor que el costo promedio del combustible ")
        # Crear DataFrame
        dfu = pd.DataFrame(dfu)

        # Agrupar los datos por marca de vehículo y calcular el costo promedio del combustible
        dfu_agrupado = dfu.groupby('OEM_Make')['precio_total_COP_Gal_km'].mean().reset_index()

      
        st.table(dfu_agrupado)
        

         
with col13:
        st.header("GRAFICO DEL CONSUMO ESPECIFICO")
        # Agrupar por OEM_Make y calcular la media de Cs_L_Gal_km_Ton y Cs_R_Gal_km_Ton para cada grupo
        dfu_grouped = dfu.groupby('OEM_Make')[['Cs_L_Gal_km_Ton', 'Cs_R_Gal_km_Ton']].mean().reset_index()
        # Plotting the results
        fig, ax= plt.subplots(figsize=(5,3))
        dfu_grouped_sorted = dfu_grouped.sort_values(by='Cs_R_Gal_km_Ton')
        plt.bar(dfu_grouped_sorted['OEM_Make'], dfu_grouped_sorted['Cs_R_Gal_km_Ton'] * 100) # Convert to percentage
        plt.xlabel('Marca vehículo')
        plt.ylabel('Consumo específico Gal/km * Ton (%)')
        plt.title('Consumo específico de los vehículos por marca')
        plt.xticks(rotation=90)
        st.pyplot(fig)
  

with col14:       
         # Seleccionar las columnas relacionadas con el consumo especifico
       # Crear DataFrame

        st.header("TABLA DEL CONSUMO ESPECIFICO")
        st.subheader("Hallazgos")
        st.write(" El consumo específico (Consumo de combustible el galones / peso carga) resultan en promedio 5  veces mas alto que los demás marcas de vehículos, esto es, que se debe considerar para este caso tanto el consumo especifico como el costo del combustible para la carga máxima que el vehículo llevara ")
        dfu = pd.DataFrame(dfu)

        # Agrupar los datos por marca de vehículo y calcular el costo promedio del combustible
        dfu_agrupado = dfu.groupby('OEM_Make')['Cs_R_Gal_km_Ton'].mean().reset_index()

      
        st.table(dfu_agrupado)

with col15:   
      
        st.header("GRAFICO DEL CO2 Y GAL/KM CUANDO EL VEHICULO ESTA CARGADO")
        st.subheader("Hallazgos")
        st.write(" los vehículos mas optimos en cuanto a consumo y a costo son de las marcas Mercedes Benz, Renualt , Daf y Volvo ")
        dfu = pd.DataFrame(dfu)


        eficiencia_marcas = dfu.groupby('OEM_Make').agg(
            Consumo_FuelPromedio=('R_FuelConsumption_Gal_km', 'mean'),
            Emisiones_Promedio=('R_CO2_gkm', 'mean')
        ).reset_index()

        # Ordenar las marcas por menor consumo de combustible y emisiones
        eficiencia_marcas = eficiencia_marcas.sort_values('Consumo_FuelPromedio')

        # Crear el gráfico combinado
        fig, ax1 = plt.subplots(figsize=(6, 4))

        # Barras para consumo promedio de combustible
        sns.barplot(data=eficiencia_marcas, x='OEM_Make', y='Consumo_FuelPromedio', color='blue', alpha=0.7, label='Consumo (Gal/km)', ax=ax1)
        ax1.set_ylabel('Consumo (Gal/km)')
        ax1.set_xlabel('Marca')
        ax1.tick_params(axis='y')
        ax1.set_xticklabels(eficiencia_marcas['OEM_Make'], rotation=45, ha='right')

        # Eje secundario para emisiones promedio
        ax2 = ax1.twinx()
        sns.lineplot(data=eficiencia_marcas, x='OEM_Make', y='Emisiones_Promedio', color='red', label='Emisiones CO₂ (g/km)', marker='o', ax=ax2)
        ax2.set_ylabel('Emisiones CO₂ (g/km)')
        ax2.tick_params(axis='y')

        # Añadir leyendas y título
        fig.suptitle('Marcas Más Eficientes en Consumo de Combustible vs. Emisiones de CO₂ cuando esta cargado', fontsize=16)
        ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))
        ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.9))
        st.pyplot(fig)


with col16:
        st.header("GRAFICO DEL CO2 Y GAL/KM CUANDO EL VEHICULO ESTA  SIN CARGA")

        st.subheader("Hallazgos")
        st.write(" los vehículos mas optimos en cuanto a consumo y a costo son de las marcas Mercedes Benz, Renualt , Daf y Volvo ")
        dfu = pd.DataFrame(dfu)
        eficiencia_marcas = dfu.groupby('OEM_Make').agg(
            Consumo_FuelPromedio=('L_FuelConsumption_Gal_km', 'mean'),
            Emisiones_Promedio=('L_CO2_gkm', 'mean')
        ).reset_index()
    
        eficiencia_marcas = eficiencia_marcas.sort_values('Consumo_FuelPromedio')

        # Crear el gráfico combinado
        fig, ax1 = plt.subplots(figsize=(6, 4))

        # Barras para consumo promedio de combustible
        sns.barplot(data=eficiencia_marcas, x='OEM_Make', y='Consumo_FuelPromedio', color='blue', alpha=0.7, label='Consumo (Gal/km)', ax=ax1)
        ax1.set_ylabel('Consumo (Gal/km)')
        ax1.set_xlabel('Marca')
        ax1.tick_params(axis='y')
        ax1.set_xticklabels(eficiencia_marcas['OEM_Make'], rotation=45, ha='right')

        # Eje secundario para emisiones promedio
        ax2 = ax1.twinx()
        sns.lineplot(data=eficiencia_marcas, x='OEM_Make', y='Emisiones_Promedio', color='red', label='Emisiones CO₂ (g/km)', marker='o', ax=ax2)
        ax2.set_ylabel('Emisiones CO₂ (g/km)')
        ax2.tick_params(axis='y')

        # Añadir leyendas y título
        fig.suptitle('Marcas Más Eficientes en Consumo de Combustible vs. Emisiones de CO₂ cuando esta sin carga', fontsize=16)
        ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))
        ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.9))

        plt.scatter(dfu['OEM_Make'], dfu['precio_total_COP_Gal_km'])
        plt.xlabel('Marca del combustible ')
        plt.ylabel('Consumo de Combustible (G/km)')
        plt.xticks(rotation=90)
        st.pyplot(fig)

with col17:
        # GRAFICO DE DISPERSION DE RELACION ENTRE  LA EMISION DE CO2 Y CONSUMO DE COMBUSTIBLE POR KM Y CONSUMO ESPECIFICO DE VEHICULOS CUANDO ESTAN CARGADOS
        st.header("GRAFICO DEL CO2, GAL/KM  PRECIO /KM CUANDO EL VEHICULO ESTA CARGADO")
        st.subheader("Hallazgos")
        st.write(" Para la toma de desicion en cuanto a los vehiculos mas optimos  se escogen las marcas Reanualt, Mercedez Benz , Iveco para vehculos de categoria N3")
        # Seleccionar solo las columnas numéricas
        numeric_columns = dfu.select_dtypes(include=['number']).columns

        # Agrupar por marca de vehículo y calcular los promedios solo para columnas numéricas
        grouped_dfu = dfu.groupby('OEM_Make')[numeric_columns].mean().reset_index()

        # Crear el gráfico de dispersión
        fig,ax=plt.subplots()
        scatter = plt.scatter(grouped_dfu['R_CO2_gkm'], grouped_dfu['precio_total_COP_Gal_km'], c=grouped_dfu['Cs_R_Gal_km_Ton'], cmap='viridis', alpha=0.6)
        plt.colorbar(scatter, label='Consumo especifico (g/km * Ton)')
        plt.xlabel('CO2 (g/km)')
        plt.ylabel('Precio_total COP (Gal/Km)')
        plt.title('Relación entre Precio en COP (Gal), Consumo de CO2 (g) y Consumo especifico (Gal/Ton) de marcas Vehiculos con carga por km ')
        plt.grid(True)

        # Agregar etiquetas dinámicas por marca de vehículo
        for i in range(len(grouped_dfu)):
            plt.text(grouped_dfu['R_CO2_gkm'].iloc[i], grouped_dfu['precio_total_COP_Gal_km'].iloc[i], grouped_dfu['OEM_Make'].iloc[i], fontsize=8, alpha=0.7)

        st.pyplot(fig)

with col18:
        st.header("TABLA DEL CO2, GAL/KM  PRECIO /KM CUANDO EL VEHICULO ESTA CARGADO")
        # Crear DataFrame
        dfu = pd.DataFrame(dfu)

        # Agrupar los datos por marca de vehículo y calcular el promedio de CO2, precio del combustible y consumo específico
        dfu_agrupado = dfu.groupby('OEM_Make').agg({
            'R_CO2_gkm': 'mean',
            'precio_total_COP_Gal_km': 'mean',
            'Cs_R_Gal_km_Ton': 'mean'
        }).reset_index()

        # Renombrar las columnas para mayor claridad
        dfu_agrupado.columns = [
            'Marca',
            'CO2 (g/km)',
            'Precio del Combustible (COP/Gal/km)',
            'Consumo Específico (Gal/km * Ton)'
        ]

        # Mostrar la tabla agrupada
        st.table(dfu_agrupado)

# Botones    
st.write("---")
st.write("   ")

col6, col7, col8 = st.columns([1,1,5])

with col6:
    btnRegional = st.button('Datos regionales')
with col7:
    btnInicio = st.button('Inicio')

if btnRegional:
    st.switch_page('pages/regional.py')

if btnInicio:
    st.switch_page('main.py')