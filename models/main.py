import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from models.login import check_login

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
    st.sidebar.success("Sesión activa")
    st.title("Bienvenido a la app Streamlit")
    st.write("Contenido principal.")

if st.session_state.logged_in:
    app_content()
else:
    login_page()
