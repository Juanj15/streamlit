import streamlit as st

def generarMenu():
    with st.sidebar:
        st.page_link('main.py', label = "Inicio", icon = "🏠")
        st.page_link('pages/urbano.py', label = "Trayecto urbano", icon = "🏙️")
        st.page_link('pages/regional.py', label = "Trayecto regional", icon = "🏔️")
        st.page_link('pages/nacional.py', label = "Trayecto largo", icon = "🗺️")
        st.page_link('pages/electricos.py', label = "Eléctricos", icon = "🔋")


