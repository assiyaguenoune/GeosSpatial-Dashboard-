import geopandas as gpd
import pandas as pd
import folium
import streamlit as st
from shapely.geometry import Point
from datetime import datetime, timedelta
import numpy as np
from streamlit_folium import folium_static

    # Charger le shapefile initial

chemin_vers_shapefile = "./communes_wgs84/communes_wgs84/communes_wgs84.shp"
gdf_initial = gpd.read_file(chemin_vers_shapefile)

    # Charger le shapefile contenant les bordures
shapefile_path = "./communes_wgs84/communes_wgs84/communes_wgs84.shp"
gdf_bordures = gpd.read_file(shapefile_path)



    # Extraire la géométrie des bordures
geometrie_bordures = gdf_bordures.geometry.unary_union 
    # Générer des points aléatoires à l'intérieur des bordures
nombre_de_points = 3000
points = []

for _ in range(nombre_de_points):
    point = None
    while point is None or not point.within(geometrie_bordures):
            x = np.random.uniform(gdf_bordures.bounds.minx.min(), gdf_bordures.bounds.maxx.max())
            y = np.random.uniform(gdf_bordures.bounds.miny.min(), gdf_bordures.bounds.maxy.max())
            point = Point(x, y)
    points.append(point)

    # Définir les propriétés de la géométrie et des attributs
geometry = points
propriete1 = [f"Propriete_{i}" for i in range(1, 3001)]
propriete2 = np.random.uniform(0, 100, 3000)
propriete3 = np.random.uniform(0, 100, 3000)
propriete4 = [datetime.now() - timedelta(days=i) for i in range(3000)]

attributs_jour = {
        f"Attibut1Jour-{i}": np.random.uniform(0, 100, 3000) for i in range(7)
    }
attributs_jour.update({
        f"Attibut2Jour-{i}": np.random.uniform(0, 20, 3000) for i in range(7)
    })
attributs_jour.update({
        f"Attibut3Jour-{i}": np.random.uniform(0, 50, 3000) for i in range(7)
    })

    # Créer le DataFrame
data = {
        'geometry': geometry,
        'propriete1': propriete1,
        'propriete2': propriete2,
        'propriete3': propriete3,
        'propriete4': propriete4
    }
data.update(attributs_jour)

df = pd.DataFrame(data)

    # Créer un GeoDataFrame
    
gdf = gpd.GeoDataFrame(df)
    # type: ignore # type: ignore 
    # Sauvegarder en format geoparquet
gdf.to_parquet('dataset.geoparquet', index=False)
    # type: ignore # type: ignore

# Sidebar pour choisir la colonne à cartographier
selected_column = st.sidebar.selectbox('Choisir la colonne à cartographier', gdf.columns)

# Afficher la carte
st.title('Dashboard GeoAnalytique')
st.header('Volet Cartographie du jour J')

# Créer une carte Folium
m2 = folium.Map(location=[gdf['geometry'].y.mean(), gdf['geometry'].x.mean()], zoom_start=6)
# Ajouter des marqueurs à la carte
for idx, row in gdf.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=row[selected_column]).add_to(m2)
# Afficher la carte avec Streamlit Folium
folium_static(m2)

st.map(gdf)

# Sidebar pour filtrer les données par jour
selected_day = st.sidebar.slider('Choisir le jour', -6, 0, -1)

# Filtrer les données en fonction du jour sélectionné
filtered_data = gdf[gdf[f"Attibut1Jour{selected_day}"].notnull()]

# Afficher les informations sur les données filtrées
st.subheader(f'Données pour le jour {selected_day}')
st.write(filtered_data)

# Afficher le GeoDataFrame
st.header('GeoDataFrame')
st.write(gdf)
