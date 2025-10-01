

# --- Générer PDF ---
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
from analyse import kpi_moyennes, moyennes
from visuel import plot_heure, plot_jour, plot_mois, plot_carte


# --- Fonction pour convertir un graphique Plotly en image PNG ---
def plotly_to_png_bytes(fig, width=700, height=400):
    img_bytes = fig.to_image(format="png", width=width, height=height)
    buf = io.BytesIO(img_bytes)
    return buf

def create_pdf(kpis, moyenne_heure, moyenne_jour, moyenne_mois, int_heure):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Page 1 : Titre + KPIs
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-50, "Rapport - Analyse Comptage Vélo Paris")
    
    c.setFont("Helvetica", 12)
    y_pos = height - 100
    c.drawString(50, y_pos, "KPIs :")
    y_pos -= 20
    for key, value in kpis.items():
        c.drawString(60, y_pos, f"{key} : {value}")
        y_pos -= 20

    c.showPage()  # Nouvelle page pour les graphiques

    # Graphiques
    figures = [
        plot_heure(moyenne_heure),
        plot_jour(moyenne_jour),
        plot_mois(moyenne_mois),
        plot_carte(int_heure, heure=17)
    ]

    for fig in figures:
        buf = plotly_to_png_bytes(fig)
        img = ImageReader(buf)
        # Ajuster l'image sur la page
        c.drawImage(img, 50, height-450, width=500, height=300)
        c.showPage()
        buf.close()

    c.save()
    buffer.seek(0)
    return buffer
