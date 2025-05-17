import pandas as pd
from fpdf import FPDF
import tempfile
import os

def generar_pdf_top15(df):
    top15 = df.sort_values(by="Valor (€)", ascending=False).head(15)

    class PDF(FPDF):
        pass

    pdf = PDF()
    pdf.add_page()

    # Ruta a la fuente correcta
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(200, 10, txt="Top 15 Jugadores por Valor (€)", ln=True, align="C")

    for _, row in top15.iterrows():
        valor = f"{row['Valor (€)']:,}".replace(",", ".")
        linea = f"{row['Nombre']} - {row['Equipo']} - {valor} €"
        pdf.cell(200, 10, txt=linea, ln=True)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name
