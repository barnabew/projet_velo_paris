import pandas as pd
import pandas as pd

def moyennes(df):

     jours_fr = {
          0: "Lundi", 1: "Mardi", 2: "Mercredi",
          3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"
      }

      mois_fr = {
          1: "Janvier",2: "Février",3: "Mars",4: "Avril",
          5: "Mai",6: "Juin",7: "Juillet",8: "Août",
          9: "Septembre",10: "Octobre",11: "Novembre",12: "Décembre"
      }

      jours_par_mois = (
          df.groupby("Mois_num")["Date et heure de comptage"]
            .apply(lambda x: x.dt.date.nunique())
            .reset_index(name="Nb_jours")
      )

    
    moyenne_heure = (
        (df.groupby("Heure")["Comptage horaire"].sum() / 365)
        .reset_index().round(1)
        .sort_values(by="Heure")
    )
    moyenne_jour = (
        (df.groupby("Jour_num")["Comptage horaire"].sum() / 52)
        .reset_index().round(1)
        .sort_values(by="Jour_num", ascending=True)
    )
    
    moyenne_jour["Jour"] = moyenne_jour["Jour_num"].map(jours_fr)

    somme_mois = df.groupby("Mois_num")["Comptage horaire"].sum().reset_index(name="Total_velos")
    moyenne_mois = somme_mois.merge(jours_par_mois, on="Mois_num")
    moyenne_mois["Moyenne_jour"] = (moyenne_mois["Total_velos"] / moyenne_mois["Nb_jours"]).round(1)

    moyenne_mois["Mois"] = moyenne_mois["Mois_num"].map(mois_fr)
    
    int_heure = df.groupby(["Nom du site de comptage","lat","lon","Heure"]).agg(Velos=("Comptage horaire","sum")).reset_index()
    return moyenne_heure, moyenne_jour, moyenne_mois, int_heure


def kpi_moyennes(df):
  moyenne_heure, moyenne_jour, moyenne_mois, int_heure = moyennes(df)
  
  vmin = int_heure["Velos"].min()
  vmax = int_heure["Velos"].max()

  pic_matin = moyenne_heure.idxmax() if moyenne_heure.index[0] < 12 else "Non défini"
  pic_soir = moyenne_heure.idxmax() if moyenne_heure.index[0] >= 12 else "Non défini"

  moyenne_annee = df.groupby("Jour")["Comptage horaire"].sum() / 365
  jour_max = moyenne_annee.idxmax()
  jour_min = moyenne_annee.idxmin()
  
  mois_max = moyenne_mois.loc[moyenne_mois["Moyenne_jour"].idxmax(), "Mois"]
  mois_min = moyenne_mois.loc[moyenne_mois["Moyenne_jour"].idxmin(), "Mois"]
  
  # Trafic moyen journalier
  trafic_moyen = int(df["Comptage horaire"].sum() / 365)
  return {
             "Pic du matin": "8h - 9h",
             "Pic du soir": "17h - 19h",
             "Jour le plus chargé": jour_max,
             "Jour le moins chargé": jour_min,
             "Mois le plus chargé": mois_max,
             "Mois le moins chargé": mois_min
         },moyenne_heure, moyenne_jour, moyenne_mois, int_heure

  
