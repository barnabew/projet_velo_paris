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

with st.expander("Introduction"):
    st.markdown(textes["introduction"])
    

# Sommaire

titres_onglets = ["Résumé Exécutif","Analyse par heure","Analyse par jour","Analyse par mois","Analyse par compteur","Conclusion"]
onglets = st.tabs(titres_onglets)



with onglets[0]:
         st.subheader("KPIs")
         cols = st.columns(4)
         for i, (title, value) in enumerate(kpis.items()):
                  with cols[i % 4]:
                     st.metric(title, value)

         
         st.markdown(textes["resume"])
  

# --- Moyenne par heure ---
with onglets[1]:
         st.header("Moyenne des vélos par heure")
         
         st.plotly_chart(plot_heure(moyenne_heure), use_container_width=True)
         
         st.markdown(textes["heure"])


# --- Moyenne par jour ---
with onglets[2]:
         st.header("Moyenne des vélos par jour")
         st.plotly_chart(plot_jour(moyenne_jour), use_container_width=True)

         st.markdown(textes["jour"])


# --- Moyenne par mois ---
with onglets[3]:
         st.header("Moyenne des vélos par mois")
         st.plotly_chart(plot_mois(moyenne_mois), use_container_width=True)
         st.markdown(
                f"""
                <div style="max-width: 800px; margin:auto; text-align: justify;">
                    {textes['resume']}
                </div>
                """,
                unsafe_allow_html=True
        )
         st.markdown(textes["mois"])


# --- Carte interactive par heure ---
with onglets[4]:

         int_17h = int_heure[int_heure["Heure"] == 17]

         st.markdown(
                f"""
                <div style="max-width: 800px; margin:auto; text-align: justify;">
                    {textes['resume']}
                </div>
                """,
                unsafe_allow_html=True
         )
         st.header("Carte interactive des vélos par site et heure")
         st.plotly_chart(plot_carte(int_heure,heure=17), use_container_width=True)
    
         st.markdown(textes["carte"])

#Conclusion

with onglets[5]:
         st.markdown(textes["conclusion"])
