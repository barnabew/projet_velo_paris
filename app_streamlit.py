import streamlit as st
from data import chargement_nettoyage
from analyse import kpi_moyennes, moyennes
from visuel import plot_heure, plot_jour, plot_mois, plot_carte
from texts import texts




# === 4. Analyse des données ===


# Calcul de la moyenne journaliere de vélo
moyenne_jours = round(df["Comptage horaire"].sum() / 365,1)


# Moyennes par heure
moyenne_heure = (
    (df.groupby("Heure")["Comptage horaire"].sum() / 365)
    .reset_index().round(1)
    .sort_values(by="Heure")
)

# Moyennes par jour
moyenne_jour = (
    (df.groupby("Jour")["Comptage horaire"].sum() / 52)
    .reset_index().round(1)
)

# Moyennes par mois (corrigées par nb de jours du mois)
somme_mois = df.groupby("Mois_num")["Comptage horaire"].sum().reset_index(name="Total_velos")
moyenne_mois = somme_mois.merge(jours_par_mois, on="Mois_num")
moyenne_mois["Moyenne_jour"] = (moyenne_mois["Total_velos"] / moyenne_mois["Nb_jours"]).round(1)
# Traduction des mois en français
mois_fr = {
    "January": "Janvier","February": "Février","March": "Mars","April": "Avril",
    "May": "Mai","June": "Juin","July": "Juillet","August": "Août",
    "September": "Septembre","October": "Octobre","November": "Novembre","December": "Décembre"
}
moyenne_mois["Mois"] = moyenne_mois["Mois_num"].apply(lambda x: pd.to_datetime(str(x), format="%m").month_name())
moyenne_mois["Mois"] = moyenne_mois["Mois"].map(mois_fr)



# Grouper par site et heure
int_heure = df.groupby(["Nom du site de comptage", "lat", "lon", "Heure"]).agg(
    Velos=("Comptage horaire", "sum")
).reset_index()


# Récupère les valeurs min et max pour l'échelle fixe
vmin = int_heure["Velos"].min()
vmax = int_heure["Velos"].max()



# Pic du matin et du soir
pic_matin = moyenne_heure.idxmax() if moyenne_heure.index[0] < 12 else "Non défini"
pic_soir = moyenne_heure.idxmax() if moyenne_heure.index[0] >= 12 else "Non défini"

# Jours avec le plus et le moins de trafic
moyenne_annee = df.groupby("Jour")["Comptage horaire"].sum() / 365
jour_max = moyenne_annee.idxmax()
jour_min = moyenne_annee.idxmin()

# Mois avec le plus et le moins de trafic
# Assurez-vous que 'Moyenne_jour' dans moyenne_mois est déjà calculée
mois_max = moyenne_mois.loc[moyenne_mois["Moyenne_jour"].idxmax(), "Mois"]
mois_min = moyenne_mois.loc[moyenne_mois["Moyenne_jour"].idxmin(), "Mois"]

# Trafic moyen journalier
trafic_moyen = int(df["Comptage horaire"].sum() / 365)



# === Streamlit App ===


st.set_page_config(page_title="Analyse Comptage Vélo Paris", layout="wide")


df = load_and_clean_data()
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
         st.plotly_chart(plot_carte(int_heure,heure=17), use_container_width=True)

         st.markdown(texts["carte"])

#Conclusion

with onglets[5]:
         st.markdown(texts["conclusion"])
