import pandas as pd
import json
import plotly.express as px
import geopandas as gpd
import streamlit as st

# Load the data
data = json.load(open('GRUENRAUM_BAUM.json'))
# Transform data
trees = []
for tree in data['features']:
    dict = {}
    dict['lon'] = tree['geometry']['coordinates'][0]
    dict['lat'] = tree['geometry']['coordinates'][1]
    dict['gattung'] = tree['properties']['GATTUNG']
    dict['art'] = tree['properties']['ART_SORTE']
    dict['baumhoehe'] = tree['properties']['BAUMHOEHE']
    dict['kr_durchmesser'] = tree['properties']['KR_DURCHMESSER']
    dict['st_umfang'] = tree['properties']['ST_UMFANG']
    dict['pflanzjahr'] = tree['properties']['PFLANZJAHR']
    trees.append(dict)
df = pd.DataFrame(trees)

df_geo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon,df.lat), crs='EPSG:2056')
# Change projection
esg_epsg = 4326 # # EPSG code for ESG
df_geo = df_geo.to_crs(crs=esg_epsg)
df['lon_trans'] = df_geo.get_coordinates()['x']
df['lat_trans'] = df_geo.get_coordinates()['y']

# Creating plot
fig = px.scatter_mapbox(df[df['gattung']=='Picea'], lat='lat_trans', lon='lon_trans', color='art',
                        hover_name='art', size='baumhoehe',
                        title='Standorte Tannen (Picea) in Luzern')
fig.update_layout(mapbox_style="open-street-map")

# Creating Web App
st.header("Tannen in Luzern", divider="grey")
st.write(f"""
Wo kann in weihnachtlicher Stimmung Glühwein getrunken werden? 
""")

# Display Plot
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write("Quelle: https://opendata.swiss/de/dataset/baume-standort-und-informationen")
