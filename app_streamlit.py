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


# Trie par heures des moyennes journaliere
moyenne_heure = (
    (df.groupby("Heure")["Comptage horaire"].sum() / 365)
    .reset_index()
    .round(1)
    .sort_values(by="Heure")
)   

#Trie par jour de la semaine des moyennes journaliere
moyenne_jour = (
    (df.groupby("Jour")["Comptage horaire"].sum() / 365 )
    .reset_index()
    .round(1)
    .sort_values(by="Comptage horaire",ascending=False)
)


#Trie par mois des moyennes journaliere

#calcul du nombre de vélos par mois
somme_mois = (
    df.groupby("Mois_num")["Comptage horaire"]
    .sum()
    .reset_index(name="Total_velos")
)

# Assemblage du nombre de vélos par jour et du nombre de jours par mois
moyenne_mois = somme_mois.merge(jours_par_mois,on="Mois_num")

# Moyenne pour chaque mois par jours = moyenne mois / nombre de jours
moyenne_mois["Moyenne_jour"] = (moyenne_mois["Total_velos"] / moyenne_mois["Nb_jours"]).round(1)

# Permet d'avoir les noms en anglais des mois
moyenne_mois["Mois"] = (
    moyenne_mois["Mois_num"]
    .apply(lambda x : pd.to_datetime(str(x), format="%m").month_name())
)


# Transformation des noms de mois en francais
mois_fr = {
    "January": "Janvier",
    "February": "Février",
    "March": "Mars",
    "April": "Avril",
    "May": "Mai",
    "June": "Juin",
    "July": "Juillet",
    "August": "Août",
    "September": "Septembre",
    "October": "Octobre",
    "November": "Novembre",
    "December": "Décembre"
}

moyenne_mois["Mois"]=moyenne_mois["Mois"].map(mois_fr)







# === 5. Visualisation des données ===

# Graphique line des moyennes journaliere selon l'heure
fig3 = px.line(
    moyenne_heure, 
    x="Heure", 
    y="Comptage horaire", 
    title="Moyenne des vélos par heure",  
    markers=True
)




# Graphique bar des moyennes journaliere selon le jour de la semaines
fig4 = px.bar(
    moyenne_jour, 
    x="Jour", 
    y="Comptage horaire", 
    title="Moyenne des vélos par jour", 
    color="Comptage horaire"
)





# Graphique bar des moyennes journaliere selon les mois
fig5 = px.bar(
    moyenne_mois, 
    x="Mois", 
    y="Moyenne_jour", 
    title="Moyenne des vélos par jour", 
    color="Moyenne_jour"
)




# Carte interactive par heure

# Grouper par site et heure
int_heure = df.groupby(["Nom du site de comptage", "lat", "lon", "Heure"]).agg(
    Velos=("Comptage horaire", "sum")
).reset_index()


# Récupère les valeurs min et max pour l'échelle fixe
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
    range_color=[vmin, vmax]  # Fixe l'échelle de couleur
)

# Ajuste l'opacité pour un effet plus fondu
fig6.update_traces(marker=dict(opacity=0.6, sizemode='area', sizeref=2.*max(int_heure['Velos'])/(40.**2)))

# Optionnel : style de la légende pour être plus lisible
fig6.update_layout(coloraxis_colorbar=dict(title="Nombre de vélos"))



# === Streamlit App ===
st.set_page_config(page_title="Analyse Comptage Vélo Paris", layout="wide")

st.title("Analyse des Comptages de Vélo à Paris (2024-2025)")


# --- Moyenne par heure ---
st.header("Moyenne des vélos par heure")
fig3 = px.line(
    moyenne_heure, 
    x="Heure", 
    y="Comptage horaire", 
    title="Moyenne des vélos par heure",  
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)

# --- Moyenne par jour ---
st.header("Moyenne des vélos par jour")
fig4 = px.bar(
    moyenne_jour, 
    x="Jour", 
    y="Comptage horaire", 
    title="Moyenne des vélos par jour", 
    color="Comptage horaire"
)
st.plotly_chart(fig4, use_container_width=True)

# --- Carte interactive par heure ---
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
fig6.update_traces(marker=dict(opacity=0.6, sizemode='area', sizeref=2.*max(int_heure['Velos'])/(40.**2)))
fig6.update_layout(coloraxis_colorbar=dict(title="Nombre de vélos"))
fig6.update_layout(
    width=800,   # largeur
    height=800,  # hauteur identique -> carré
    margin=dict(l=0, r=0, t=0, b=0)
)
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.plotly_chart(fig6, use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)
