# 🚲 Analyse des Comptages de Vélos à Paris

## 📌 Contexte
Ce projet analyse les données de comptage de vélos issues de l’[Open Data de la Ville de Paris](https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/).  
La période étudiée couvre **septembre 2024 à août 2025**.

Objectif : identifier les tendances d’usage du vélo à Paris (pics horaires, jours les plus fréquentés, variations saisonnières, analyse géographique).

---

## 🛠️ Outils utilisés
- **Python** (Pandas, Numpy, Matplotlib, Seaborn, Plotly, Geopandas)
- **SQLite** (requêtes rapides)
- **FPDF** (génération du rapport PDF)
- **Streamlit** (application interactive)

---

## 📊 Analyses effectuées
- **Nettoyage des données** : suppression des capteurs défectueux, extraction des variables temporelles (heure, jour, mois).
- **Analyses statistiques** :
  - Moyennes horaires, journalières et mensuelles
  - Identification des pics de trafic
  - Jours/mois les plus et les moins fréquentés
- **Analyse géographique** : carte des flux à 17h (heure de pointe).
- **Visualisations** : bar charts, line charts, carte interactive.
- **Livrable client** : rapport PDF structuré (page de garde, résumé exécutif, KPIs, analyses, conclusion).

---

## 📑 Livrables
- 📘 [Rapport PDF](./rapport_velo.pdf)  
- 🌐 [Application Streamlit interactive](https://testappvelo-3tskhjcmgulxgj47aa4rnp.streamlit.app/)  

---

## 🚀 Résultats clés
- **Trafic moyen journalier** : ~XX 000 vélos  
- **Pics horaires** : 8h–9h et 17h–19h  
- **Jour le plus fréquenté** : Mardi  
- **Mois les plus fréquentés** : Mai à Septembre  
- **Mois les plus calmes** : Décembre à Février  
- Forte concentration du trafic **dans l’hypercentre parisien** et le long de la Seine.

---

## 👨‍💻 Auteur
Projet réalisé par **Barnabé Willenbucher – Data Analyst Freelance**  
📧 Contact : barnabe.willenbucher@outlook.fr 
💼 [LinkedIn](https://www.linkedin.com/) | [Portfolio](https://monportfolio.com)  
