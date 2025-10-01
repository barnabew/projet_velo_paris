import streamlit as st
from data import chargement_nettoyage
from analyse import kpi_moyennes, moyennes
from visuel import plot_heure, plot_jour, plot_mois, plot_carte
from textes import textes


# === Streamlit App ===


st.set_page_config(page_title="Analyse Comptage Vélo Paris", layout="wide")


df = chargement_nettoyage()
kpis, moyenne_heure, moyenne_jour, moyenne_mois, int_heure = kpi_moyennes(df)


st.title("Rapport - Analyse des Comptages de Vélos à Paris")
st.markdown("### Auteur : Barnabé Willenbucher - Data Analyst Freelance")
st.markdown("#### Données : Ville de Paris (Open Data - Année 2024)")

# Fonction helper pour texte full-width avec padding
def style_textes(txt):
    st.markdown(
        f"""
        <div style="padding: 0 40px; text-align: justify;">
            {txt}
        </div>
        """,
        unsafe_allow_html=True
    )

with st.expander("Introduction"):
    style_textes(textes["introduction"])

with st.expander("Conclusion"):
    style_textes(textes["conclusion"])

# Sommaire
titres_onglets = ["Résumé Exécutif","Analyse par heure","Analyse par jour","Analyse par mois","Analyse par compteur"]
onglets = st.tabs(titres_onglets)

# --- Résumé Exécutif ---
with onglets[0]:
    st.header("Résumé Exécutif")
    col1, col2 = st.columns([1, 2])  # KPIs 1/3, texte 2/3
    
    # KPIs à gauche
    with col2:
        cols = st.columns(3)
        for i, (title, value) in enumerate(kpis.items()):
            col = cols[i % 3]   # choisir la bonne colonne (0,1,2)
            with col:
                st.metric(title, value)
    
    # Texte résumé à droite
    with col1:
        style_textes(textes["resume"])

# --- Analyse par heure ---
with onglets[1]:
    st.header("Moyenne des vélos par heure")
    col1, col2 = st.columns([1, 2])  # texte 1/3, graphique 2/3
    with col2:
        st.plotly_chart(plot_heure(moyenne_heure), use_container_width=True)
    with col1:
        style_textes(textes["heure"])

# --- Analyse par jour ---
with onglets[2]:
    st.header("Moyenne des vélos par jour")
    col1, col2 = st.columns([1, 2])
    with col2:
        st.plotly_chart(plot_jour(moyenne_jour), use_container_width=True)
    with col1:
        style_textes(textes["jour"])

# --- Analyse par mois ---
with onglets[3]:
    st.header("Moyenne des vélos par mois")
    col1, col2 = st.columns([1, 2])
    with col2:
        st.plotly_chart(plot_mois(moyenne_mois), use_container_width=True)
    with col1:
        style_textes(textes["mois"])

# --- Carte interactive par heure ---
with onglets[4]:
    st.header("Carte interactive des vélos par site et heure")
    col1, col2 = st.columns([1, 2])
    with col2:
        st.plotly_chart(plot_carte(int_heure, heure=17), use_container_width=True)
    with col1:
        style_textes(textes["carte"])

    
