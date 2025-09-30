import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_heure(moyenne_heure):
    return px.line(moyenne_heure, x="Heure", y="Comptage horaire", title="Moyenne par heure")

def plot_jour(moyenne_jour):
    return px.bar(moyenne_jour, x="Jour", y="Comptage horaire", title="Moyenne par jour")

def plot_mois(moyenne_mois):
    return px.bar(moyenne_mois, x="Mois", y="Moyenne_jour", title="Moyenne journalière des vélos par mois")

def plot_carte(int_heure, heure=17):
  int_17h = int_heure[int_heure["Heure"] == heure]
         
  fig = px.scatter_map(
      int_17h,
      lat="lat",
      lon="lon",
      size="Velos",
      color="Velos",
      hover_name="Nom du site de comptage",
      size_max=35,
      color_continuous_scale="Viridis",
      range_color=[vmin, vmax],
      zoom=12,
      map_style="carto-positron"  
  )
   
  fig.update_traces(
      marker=dict(
          opacity=0.7,  
          sizemode="area"
      )
  )
  fig.update_layout(
    width=700,
    height=700,
    title="Trafic cycliste à Paris - 17h",
    title_x=0.5,  # centrer le titre
    margin=dict(l=20, r=20, t=50, b=20),
    coloraxis_colorbar=dict(title="Nombre de vélos"),
    map=dict(center={"lat": 48.8566, "lon": 2.3441}, zoom=10.8)  # centrage sur Paris
   )
  return fig
