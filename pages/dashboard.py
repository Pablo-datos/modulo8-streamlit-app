import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
import sys

# Registrar ruta a controladores
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers.export_pdf import generar_pdf_top15

def show():
    st.title("📊 Dashboard – Análisis Driblab")

    # --- Fuente 1: CSV local ---
    try:
        df = pd.read_csv("data/driblab_top5.csv")
        st.subheader("📁 Datos desde CSV: Driblab TOP 5")
        st.dataframe(df)
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo CSV.")
        return
    except Exception as e:
        st.error(f"⚠️ Error cargando CSV: {e}")
        return

    # --- Fuente 2: API externa ---
    try:
        st.subheader("🌐 Usuarios simulados desde API pública (jsonplaceholder)")
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        if response.status_code == 200:
            data = response.json()
            df_api = pd.DataFrame([{
                "Nombre": user["name"],
                "Usuario": user["username"],
                "Email": user["email"],
                "Ciudad": user["address"]["city"]
            } for user in data])
            st.dataframe(df_api)
        else:
            st.warning("⚠️ No se pudo conectar con la API.")
    except Exception as e:
        st.error(f"Error cargando datos desde la API: {e}")

    # --- Visualización: Gráfico Top 15 ---
    try:
        st.subheader("📊 Valor estimado de jugadores (Top 15)")
        top_valores = df.sort_values(by='Valor (€)', ascending=False).head(15)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_valores['Nombre'], top_valores['Valor (€)'], color='royalblue')
        ax.invert_yaxis()
        ax.set_xlabel("Valor en Euros (€)")
        ax.set_title("Top 15 jugadores según valor estimado")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"⚠️ No se pudo generar el gráfico: {e}")

    # --- Exportación a PDF ---
    st.markdown("## 📤 Exportar a PDF")

    if st.button("📄 Exportar Top 15 a PDF"):
        try:
            ruta_pdf = generar_pdf_top15(df)
            with open(ruta_pdf, "rb") as f:
                st.download_button(
                    label="📥 Descargar informe en PDF",
                    data=f,
                    file_name="top15_valor.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"No se pudo generar el PDF: {e}")

    # --- Botón para impresión navegador ---
    st.markdown("""
        <br>
        <button onclick="window.print()">🖨️ Imprimir esta página</button>
        """, unsafe_allow_html=True)
