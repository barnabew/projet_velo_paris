import pandas as pd

def chargement_nettoyage():
      df = pd.read_csv("comptage-velo-donnees-compteurs-annee.zip",compression='zip',sep=";")
      
      df = df[["Date et heure de comptage",
               "Identifiant du site de comptage",
               "Identifiant du compteur",
               "Nom du site de comptage",
               "Comptage horaire",
               "Coordonnées géographiques"
              ]]
      
      df=df.dropna()
      
      defecteux = (
          df.groupby("Identifiant du site de comptage")
          .agg(Moyenne_velo =("Comptage horaire","mean"))
          .reset_index()
      )
      
      defecteux2 = defecteux[defecteux["Moyenne_velo"] == 0]
      
      sites_defectueux = defecteux2["Identifiant du site de comptage"].tolist()
      
      df = df[~df["Identifiant du site de comptage"].isin(sites_defectueux)]
      
      df["Nom du site de comptage"] = (
          df["Nom du site de comptage"]
          .str.replace(r"^(Face\s*au\s*\d+\s*)", "", regex=True)
          .str.replace(r"^(Totem\s*\d+\s*)", "", regex=True)   # supprime "Totem + numéro"
          .str.replace(r"^\d+\s*", "", regex=True)            # supprime juste un numéro au début
          .str.strip()
      )
      
      df["Date et heure de comptage"] = pd.to_datetime(df["Date et heure de comptage"], errors="coerce", utc=True)
      
      df["Date et heure de comptage"] =(df["Date et heure de comptage"].dt.tz_convert(None))
      
      df["Heure"] = df["Date et heure de comptage"].dt.hour + 1
      
      df["Jour"] = df["Date et heure de comptage"].dt.day_name()
      
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
      
      df[["lat", "lon"]] = df["Coordonnées géographiques"].str.split(",", expand=True).astype(float)
      
      df["Mois"] = df["Date et heure de comptage"].dt.month_name()
      
      df["Mois_num"] = df["Date et heure de comptage"].dt.month  # pour trier
      
      jours_par_mois = (
          df.groupby("Mois_num")["Date et heure de comptage"]
            .apply(lambda x: x.dt.date.nunique())
            .reset_index(name="Nb_jours")
      )
      return df        
