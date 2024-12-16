import streamlit as st
import pandas as pd
import utilidades as util

# Título e icono de la página
st.set_page_config(page_title="Impulso Verde", page_icon="🔋", layout="wide")

util.generarMenu()

with st.container():
            col_img, col_text = st.columns([1, 3])

            with col_img:
                st.image("Logo.png", width=180)

            with col_text:
                st.markdown("<h1 style='font-size: 4em; color: green;'>Impulso Verde</h1>", unsafe_allow_html=True)
                st.subheader("**Promoviendo un parque automotor sostenible**")
                unsafe_allow_html=True
st.write("---")

# División para introducción y datos del equipo
col1, col2 = st.columns([3,1])

with col1:
     st.header("¿Por qué surgió la idea")
     st.write("El proyecto **Impulso Verde: Por un Parque Automotor Más Sostenible** surge como una respuesta a la creciente necesidad de promover la transición energética en el sector transporte, uno de los mayores contribuyentes a las emisiones de gases de efecto invernadero (GEI) en Colombia. El objetivo principal es analizar y mostrar los beneficios ambientales, económicos y operativos de la transición de vehículos convencionales a eléctricos o híbridos. A través de herramientas avanzadas de análisis de datos y visualización, este proyecto busca proporcionar información clave que facilite la toma de decisiones hacia una movilidad más sostenible. Para cumplir con este propósito, se analizarán diferentes categorías como el tipo de vehículo, nivel de emisión, consumo de combustible o energía, autonomía, consumo por peso, rendimiento por marca, proyección de costos operativos a largo plazo, y costos por cantidad de vehículos. Estos indicadores serán fundamentales para evaluar la viabilidad y el impacto de la electrificación del parque automotor.")

with col2: #Contenido de la columna derecha
    st.subheader("Integrantes del grupo:") #Subheader
    st.markdown(
        """
        *   Erialeth Mejía Orozco
        *   Walter Castañeda Díaz
        *   Omar Andrés Gómez Calao
        *   Leonardo Yarce Ospina
        *   Juan José Jiménez Ortiz
        """
    )     
st.write("   ")
st.write("   ")
# Botones para ir a cada página del menú
col3, col4, col5, col6 = st.columns([1,1,1,1])  # Crea 4 columnas

with col3:
    btnUrbano = st.button('Datos urbanos')
with col4:
    btnRegional = st.button('Datos regionales')
with col5:
    btnNacional = st.button('Datos nacionales')
with col6:
    btnElectricos = st.button('Datos Eléctricos')

if btnUrbano:
    st.switch_page('pages/urbano.py')

if btnRegional:
    st.switch_page('pages/regional.py')

if btnNacional:
    st.switch_page('pages/nacional.py')

if btnElectricos:
    st.switch_page('pages/electricos.py')