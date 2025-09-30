import streamlit as st
from data import chargement_nettoyage
from analyse import kpi_moyennes, moyennes
from visuel import plot_heure, plot_jour, plot_mois, plot_carte
from texts import texts


# === Streamlit App ===


st.set_page_config(page_title="Analyse Comptage Vélo Paris", layout="wide")


df = chargement_nettoyage()
kpis, moyenne_heure, moyenne_jour, moyenne_mois, int_heure = kpi_moyennes(df)


st.title("Rapport - Analyse des Comptages de Vélos à Paris")

st.markdown("### Auteur : Barnabé Willenbucher - Data Analyst Freelance")
st.markdown("#### Données : Ville de Paris (Open Data - Année 2024)")

st.write("Ce rapport présente une étude approfondie des flux de vélos à Paris.\n\n"
    "À partir des données issues des compteurs automatiques, nous mettons en évidence "
    "les principales tendances d'utilisation du vélo : horaires de pointe, jours les plus actifs "
    "et variations saisonnières. L'objectif est de fournir des éléments concrets pour "
    "comprendre les comportements cyclistes et éclairer les décisions en matière de mobilité urbaine."
)

# Sommaire

titres_onglets = ["Résumé Exécutif","Analyse par heure","Analyse par jour","Analyse par mois","Analyse par compteur","Conclusion"]
onglets = st.tabs(titres_onglets)



with onglets[0]:
         st.subheader("KPIs")
         cols = st.columns(4)
         for i, (title, value) in enumerate(kpis.items()):
                  with cols[i % 4]:
                     st.metric(title, value)

         
         st.markdown(texts["resume"])
  

# --- Moyenne par heure ---
with onglets[1]:
         st.header("Moyenne des vélos par heure")
         
         st.plotly_chart(plot_heure(moyenne_heure), use_container_width=True)
         
         st.markdown(texts["heure"])


# --- Moyenne par jour ---
with onglets[2]:
         st.header("Moyenne des vélos par jour")
         st.plotly_chart(plot_jour(moyenne_jour), use_container_width=True)

         st.markdown(texts["jour"])


# --- Moyenne par mois ---
with onglets[3]:
         st.header("Moyenne des vélos par mois")
         st.plotly_chart(plot_mois(moyenne_mois), use_container_width=True)

         st.markdown(texts["mois"])


# --- Carte interactive par heure ---
with onglets[4]:

         int_17h = int_heure[int_heure["Heure"] == 17]

         
         st.header("Carte interactive des vélos par site et heure")
         st.plotly_chart(plot_carte(int_heure,kpis,heure=17), use_container_width=True)

         st.markdown(texts["carte"])

#Conclusion

with onglets[5]:
         st.markdown(texts["conclusion"])
