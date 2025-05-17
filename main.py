import streamlit as st
import sys
import os

# Asegura que se puedan importar módulos locales
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models.login import check_login
from pages import dashboard, datos_crudos  # Importaciones directas

# Inicializar estado de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Inicio de Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Inicio de sesión exitoso 🎯")
        else:
            st.error("Usuario o contraseña incorrectos")

def app_content():
    st.sidebar.title("Menú de Navegación")
    page = st.sidebar.radio("Ir a:", ["Dashboard", "Datos Crudos"])

    if page == "Dashboard":
        dashboard.show()
    elif page == "Datos Crudos":
        datos_crudos.show()

# Flujo principal de la app
if st.session_state.logged_in:
    app_content()
else:
    login_page()
