#%%
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Read the data
df = pd.read_csv("Clean_NYC_Property_Data.csv", 
                 index_col=0)

# Read GeoDataFrame from GeoJSON file
geo_df = gpd.read_file("NYC.geojson")

# Group by borough and calculate mean market value
borough_mean = df.groupby('zipcode')['market_value'].mean().reset_index()
geo_df.ZCTA5CE10 = geo_df.ZCTA5CE10.astype(float)

# Merge borough_mean with geo_df based on 'boro_code'
geo_df = geo_df.merge(borough_mean, 
                      left_on='ZCTA5CE10',
                      right_on='zipcode', 
                      how='left')

# Plot
fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,  # Ensure this matches the column name
                           color='market_value',
                           mapbox_style="open-street-map")

fig.show()
# %%
