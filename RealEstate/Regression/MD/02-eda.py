#%%
import pandas as pd
import geopandas as gpd
import plotly.express as px

df = pd.read_csv("Clean_MD_Property_Data.csv", 
                 index_col=0)

geo_df = gpd.read_file("MD.geojson")

zipcode_mean = df.groupby('zipcode')['consideration'].mean().reset_index()

geo_df = geo_df.merge(zipcode_mean, 
                      left_on='ZCTA5N',
                      right_on='zipcode', 
                      how='left')

fig = px.choropleth_mapbox(geo_df,
                           geojson=geo_df.geometry,
                           locations=geo_df.index,  # Ensure this matches the column name
                           color='consideration',
                           center={"lat": df.latitude.mean(), "lon": df.longitude.mean()},
                           mapbox_style="open-street-map")

fig.show()

# %%
