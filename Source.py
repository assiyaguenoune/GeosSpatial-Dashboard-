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

m2