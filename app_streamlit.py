#-------------------------------------------------------------------
#-------------------------------------------------------------------
#----------------------   PROJET VELO PARIS   ----------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------

# Ces données proviennent du portail d'open data de la ville de Paris
# https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/
# Elles ont était prise entre le 01/09/2024 et le 31/08/2025

import kaleido


# === 1. Importation des librairies ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# === 2. Chargement des données ===


df = pd.read_csv("comptage-velo-donnees-compteurs-annee.zip",compression='zip',sep=";")


# === 3. Nettoyage des données ===

#On selectionne les colonnes qui nous interesse
df = df[["Date et heure de comptage",
         "Identifiant du site de comptage",
         "Identifiant du compteur",
         "Nom du site de comptage",
         "Comptage horaire",
         "Coordonnées géographiques"
        ]]


#On supprime les lignes où il ya des valeurs manquantes
df=df.dropna()


#enlever les capteurs defecteux
defecteux = (
    df.groupby("Identifiant du site de comptage")
    .agg(Moyenne_velo =("Comptage horaire","mean"))
    .reset_index()
)

defecteux2 = defecteux[defecteux["Moyenne_velo"] == 0]

sites_defectueux = defecteux2["Identifiant du site de comptage"].tolist()

df = df[~df["Identifiant du site de comptage"].isin(sites_defectueux)]



# On nettoye les noms d'adresses
df["Nom du site de comptage"] = (
    df["Nom du site de comptage"]
    .str.replace(r"^(Face\s*au\s*\d+\s*)", "", regex=True)
    .str.replace(r"^(Totem\s*\d+\s*)", "", regex=True)   # supprime "Totem + numéro"
    .str.replace(r"^\d+\s*", "", regex=True)            # supprime juste un numéro au début
    .str.strip()
)




# On converti en datetime , en forcant l'utc
df["Date et heure de comptage"] = pd.to_datetime(df["Date et heure de comptage"], errors="coerce", utc=True)

# On retire le fuseau horaire
df["Date et heure de comptage"] =(df["Date et heure de comptage"].dt.tz_convert(None))

# Création de la variable heure du comptage
df["Heure"] = df["Date et heure de comptage"].dt.hour + 1

# Création de la variable jour du comptage
df["Jour"] = df["Date et heure de comptage"].dt.day_name()
# Transformation des jours en francais
jours_fr = { 
    "Monday": "Lundi",
    "Tuesday": "Mardi", 
    "Wednesday": "Mercredi", 
    "Thursday": "Jeudi", 
    "Friday": "Vendredi", 
    "Saturday": "Samedi", 
    "Sunday": "Dimanche" 
}

df["Jour"] = df["Jour"].map(jours_fr)

# Creation des variables latitutes et longitudes des capteurs
df[["lat", "lon"]] = df["Coordonnées géographiques"].str.split(",", expand=True).astype(float)

# Création de la variable mois du comptage
df["Mois"] = df["Date et heure de comptage"].dt.month_name()

# Variables utile pour calcul sur les mois 
# On crée la variable mois sur les calcul de la partie 4. car on doit prendre en compte le nombre de jours par mois
df["Mois_num"] = df["Date et heure de comptage"].dt.month  # pour trier

#calcul du nombre de jour par mois
jours_par_mois = (
    df.groupby("Mois_num")["Date et heure de comptage"]
      .apply(lambda x: x.dt.date.nunique())
      .reset_index(name="Nb_jours")
)





#Petite verification des variables
print(" Vérification doublons et valeurs manquantes")
print("Nombre de doublons :", df.duplicated().sum())
print("Valeurs manquantes restantes :")
print(df.isnull().sum())



# === 4. Analyse des données ===


# Calcul de la moyenne journaliere de vélo
moyenne_jours = round(df["Comptage horaire"].sum() / 365,1)

# On trouve les 10 sites ayant la plus petite moyennes journaliere
moyenne_bot_site = (
    (df.groupby("Nom du site de comptage")["Comptage horaire"].sum() / 365)
    .reset_index()
    .round(1)
    .sort_values(by="Comptage horaire",ascending=True)
    .head(10)
)

# On trouve les 10 sites ayant la plus grande moyennes journaliere
moyenne_top_site = (
    (df.groupby("Nom du site de comptage")["Comptage horaire"].sum() / 365)
    .reset_index()
    .round(1)
    .sort_values(by="Comptage horaire",ascending=False)
    .head(10)
)


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
    .sort_values(by="Comptage horaire", ascending=False)
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
         kpi_items = {
                  "Trafic moyen journalier": f"{metrics['trafic_moyen']} vélos",
                 "Pic du matin": metrics["pic_matin"],
                 "Pic du soir": metrics["pic_soir"],
                 "Jour le plus chargé": metrics["jour_max"],
                 "Jour le moins chargé": metrics["jour_min"],
                 "Mois le plus chargé": metrics["mois_max"],
                 "Mois le moins chargé": metrics["mois_min"]
             }
         for i, (title, value) in enumerate(kpi_items.items()):
                  with cols[i % 4]:
                     st.metric(title, value)

         
         st.write("- Le trafic moyen journalier ne reflète pas la réalité car les mêmes vélos ont pu être comptabilisés plusieurs fois.\n"
    "- Les pics d'utilisation se situent à 8h et entre 17h et 19h, correspondant aux trajets domicile-travail.\n"
    "- Le jour le plus chargé est le mardi, mais l'activité reste élevée aussi le mercredi et le jeudi.\n"
    "- Les mois de mai à septembre affichent les volumes les plus élevés, tandis que l'hiver (décembre, janvier, février) est plus calme.\n\n"
    "Ces résultats mettent en évidence les grandes tendances de l'usage du vélo à Paris et servent de base pour les analyses détaillées dans les pages suivantes."
                 )
  

# --- Moyenne par heure ---
with onglets[1]:
         st.header("Moyenne des vélos par heure")
         fig3 = px.line(
             moyenne_heure, 
             x="Heure", 
             y="Comptage horaire", 
             title="Moyenne des vélos par heure",  
             markers=True
         )
         st.plotly_chart(fig3, use_container_width=True)
         
         st.write("Le trafic cycliste est très faible pendant la nuit, quasi inexistant.\n\n"
             "Dès 7h, l'activité commence à augmenter rapidement, culminant entre 8h et 9h avec un premier pic marqué."
             "Au cours de la journée, le trafic reste relativement stable et modéré, avant de connaître un second pic important en fin d'après-midi, entre 17h et 19h.\n\n "
             "Ces pics correspondent principalement aux déplacements quotidiens des usagers entre leur domicile et leur lieu de travail, illustrant le rôle du vélo dans la mobilité urbaine quotidienne."
         )


# --- Moyenne par jour ---
with onglets[2]:
         st.header("Moyenne des vélos par jour")
         fig4 = px.bar(
             moyenne_jour, 
             x="Jour", 
             y="Comptage horaire", 
             title="Moyenne des vélos par jour", 
             color="Comptage horaire"
         )
         st.plotly_chart(fig4, use_container_width=True)

         st.write("Le trafic cycliste est très faible pendant la nuit, quasi inexistant.\n\n"
                  "L'activité cycliste varie au cours de la semaine, avec un trafic globalement plus important en semaine. "
                  "Le mardi enregistre le volume le plus élevé, mais le mercredi et le jeudi restent très proches, avec seulement de faibles écarts. "
                  "Cette répartition reflète clairement l'usage du vélo pour les déplacements domicile-travail.\n\n"
                  "Le lundi et le vendredi présentent des volumes légèrement inférieurs, ce qui pourrait s'expliquer par une plus forte pratique du télétravail ces jours-là.\n\n"
                  "Le samedi présente une activité intéressante, probablement liée aux sorties de loisirs et aux courses personnelles, tandis que le dimanche reste le jour le plus calme, indiquant un usage plus récréatif que professionnel."
         )


# --- Moyenne par mois ---
with onglets[3]:
         st.header("Moyenne des vélos par mois")
         fig5 = px.bar(
             moyenne_mois, 
             x="Mois", 
             y="Moyenne_jour", 
             title="Moyenne journalière des vélos par mois", 
             color="Moyenne_jour"
         )
         st.plotly_chart(fig5, use_container_width=True)

         st.write("Les mois de mai à septembre affichent les niveaux de trafic les plus élevés, en lien avec des conditions météorologiques favorables et une luminosité accrue. "
             "À l'inverse, l'hiver (décembre, janvier, février) présente une baisse significative de l'activité cycliste.\n\n"
             "Il convient de rappeler que ces observations portent sur une seule année de données. "
             "Ainsi, un mois exceptionnellement ensoleillé, comme un juin particulièrement beau, pourrait accentuer le trafic observé, tandis qu'un mois pluvieux pourrait le réduire. "
             "Ces variations doivent être prises en compte pour interpréter correctement les tendances saisonnières."
         )


# --- Carte interactive par heure ---
with onglets[4]:
         st.header("Carte interactive des vélos par site et heure")
         vmin = int_heure["Velos"].min()
         vmax = int_heure["Velos"].max()
         
         fig6 = px.scatter_mapbox(
             int_heure,
             lat="lat",
             lon="lon",
             size="Velos",
             color="Velos",
             animation_frame="Heure",
             hover_name="Nom du site de comptage",
             size_max=40,
             zoom=12,
             mapbox_style="open-street-map",
             color_continuous_scale="Viridis",
             range_color=[vmin, vmax]
         )
         
         
         # Ajuste l'opacité pour un effet plus fondu
         fig6.update_traces(marker=dict(opacity=0.6, sizemode='area', sizeref=2.*max(int_heure['Velos'])/(40.**2)))
         
         # Optionnel : style de la légende pour être plus lisible
         fig6.update_layout(coloraxis_colorbar=dict(title="Nombre de vélos"))
         
         
         # Mise en page carrée et centrée
         fig6.update_layout(
             width=700,
             height=700,
             margin=dict(l=20, r=20, t=50, b=20),
             coloraxis_colorbar=dict(title="Nombre de vélos"),
             map=dict(center={"lat": 48.8566, "lon": 2.3441}, zoom=10.7)  # centrage sur Paris
         )
         st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
         st.plotly_chart(fig6, use_container_width=False)
         st.markdown("</div>", unsafe_allow_html=True)

         st.write("L'analyse de la carte à 17h met en évidence une forte concentration du trafic cycliste "
             "dans l'hypercentre parisien, avec des volumes particulièrement élevés sur les axes centraux "
             "et le long de la Seine. On observe également des flux notables vers l'ouest (Boulogne, Neuilly, "
             "Issy-les-Moulineaux) et vers le sud (Montrouge, Ivry), traduisant l'importance des corridors "
             "d'entrée et de sortie de la capitale.\n\n"
             "A mesure que l'on s'éloigne du centre, l'intensité décroît, mais les points de comptage "
             "témoignent d'une pratique cycliste significative en périphérie immédiate. "
             "Le choix de 17h illustre clairement l'heure de pointe du soir, marquée par des flux soutenus "
             "liés aux déplacements domicile-travail. Cette répartition souligne le rôle central des "
             "infrastructures cyclables parisiennes et l'importance des connexions avec la petite couronne "
             "pour accompagner la croissance de l'usage du vélo."
         )

#Conclusion

with onglets[5]:
         st.write("L'analyse des données met en avant le rôle central du vélo dans la mobilité urbaine parisienne. "
             "Les flux horaires montrent des pics clairs le matin (8h-9h) et en fin d'après-midi (17h-19h), "
             "correspondant aux déplacements domicile-travail. Ces tendances sont complétées par une répartition hebdomadaire "
             "indiquant un trafic plus soutenu du mardi au jeudi, tandis que le lundi et le vendredi affichent des volumes un peu plus faibles, "
             "probablement liés à une plus forte pratique du télétravail. Les usages deviennent plus récréatifs le samedi et le dimanche.\n\n"
    
             "Les variations mensuelles soulignent une forte saisonnalité, avec un trafic plus élevé de mai à septembre et "
             "une baisse sensible en hiver. Il est important de rappeler que ces observations portent sur une seule année de données, "
             "ce qui implique que des conditions météorologiques particulières peuvent accentuer ou réduire ces tendances.\n\n"
    
             "L'analyse géographique des capteurs - à interpréter avec prudence car leur implantation reste inégale et "
             "certains arrondissements en sont dépourvus - met en évidence une concentration particulièrement"
             "forte des flux cyclistes dans le centre de Paris, notamment autour de Châtelet et des grands axes convergents. "
             "Les volumes plus modérés observés en périphérie traduisent une densité moindre, " 
             "ce qui souligne à la fois le rôle structurant du coeur de la capitale et la nécessité de développer "
             "des infrastructures adaptées pour accompagner l'usage du vélo dans les zones moins centrales. \n\n"
   
    
             "Ces éléments permettent non seulement de mieux comprendre les comportements des cyclistes parisiens, "
             "mais aussi de guider l'amélioration des infrastructures et des politiques de mobilité durable. "
             "Une des améliorations possibles serait peut-être l'ajout de nouveaux axes cyclables, "
             "à considérer en fonction des heures, des saisons et des jours.\n\n"
         )
