from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_informe_pdf(nombre_archivo_dwg, cumple, observaciones, datos_extraidos, ruta_destino):
    '''
    Genera un PDF de informe técnico.
    '''
    c = canvas.Canvas(ruta_destino, pagesize=A4)
    ancho, alto = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, alto - 50, "Informe Técnico de Validación de Plano")

    c.setFont("Helvetica", 11)
    c.drawString(50, alto - 100, f"Nombre del archivo: {nombre_archivo_dwg}")
    c.drawString(50, alto - 120, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.drawString(50, alto - 150, "Resultado:")
    if cumple:
        c.setFillColorRGB(0, 0.5, 0)  # verde
        c.drawString(120, alto - 150, "CUMPLE con la normativa.")
    else:
        c.setFillColorRGB(1, 0, 0)  # rojo
        c.drawString(120, alto - 150, "NO CUMPLE con la normativa.")
    c.setFillColorRGB(0, 0, 0)

    c.drawString(50, alto - 180, "Observaciones:")
    texto_obs = observaciones if observaciones else "Sin observaciones adicionales."
    c.drawString(120, alto - 180, texto_obs)

    c.drawString(50, alto - 220, "Datos extraídos del plano:")
    y = alto - 240
    for clave, valor in datos_extraidos.items():
        c.drawString(70, y, f"- {clave}: {valor}")
        y -= 20

    c.save()
    return ruta_destino
