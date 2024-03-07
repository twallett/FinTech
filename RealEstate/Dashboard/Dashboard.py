#%%

# To run this file go to terminal and run the following command:
# $ streamlit run Dashboard.py

from leafmap.common import hex_to_rgb
import leafmap.colormaps as cm
import geopandas as gpd
import streamlit as st 
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")

st.header("Streamlit Real Estate Dashboard 🏘️")

r1_col1, r1_col2 = st.columns(2)

# Location filter
with r1_col1:
    location_filter = st.selectbox('State',
                                   ('Select a state', 'Maryland', 'New York City'))

# Plot type filter
with r1_col2:
    geo_filter = st.selectbox('Plot type',
                              ('Select a plot type', 'Zipcode', 'Heatmap', 'HexagonLayer'))
    
if (location_filter == 'Select a state') or (geo_filter == 'Select a plot type'):
    st.stop()

@st.cache_data    
def load_data(path):
    return pd.read_csv(path)

@st.cache_data    
def load_gpd(path):
    return gpd.read_file(path)
       
if geo_filter == 'Zipcode':
        
    if location_filter == 'Maryland':
        path = "Clean_MD_Property_Data.csv"
        df = load_data(path)
        path_gpd = "MD.geojson"
        gdf = load_gpd(path_gpd)
    
        # Housing Filter
        housing_filter = st.selectbox('Housing Features',
                                      ('Select a feature', 'consideration', 'land_value', 'land_improvements', 'sqft', 'year_built', 'grade'))
        
        
        if (housing_filter == 'Select a feature'):
            st.stop()
        
        median = df.groupby('zipcode')[housing_filter].median().reset_index()
        gdf = gdf.merge(median,
                        left_on='ZCTA5N',
                        right_on='zipcode', 
                        how='left')
        gdf = gdf.sort_values(by=housing_filter, ascending=True)
        gdf.dropna(inplace=True)
        
    if location_filter == 'New York City':
        path = "Clean_NYC_Property_Data.csv"
        df = load_data(path)
        path_gpd = "NYC.geojson"
        gdf = load_gpd(path_gpd)
        gdf.ZCTA5CE10 = gdf.ZCTA5CE10.astype(float)
        
        # Housing Filter 
        housing_filter = st.selectbox('Housing Features',
                                  ('Select a feature', 'market_value'))
        
        if (housing_filter == 'Select a feature'):
            st.stop()
        
        median = df.groupby('zipcode')[housing_filter].median().reset_index()
        gdf = gdf.merge(median,
                        left_on='ZCTA5CE10',
                        right_on='zipcode',
                        how='left')
        gdf = gdf.sort_values(by=housing_filter, ascending=True)
        gdf.dropna(inplace=True)
        
        
    palettes = cm.list_colormaps() 
    
    r2_col1, r2_col2 = st.columns(2)   
                
    with r2_col1: 
        palette = st.selectbox("Color palette", palettes, index=palettes.index("Blues"))

    with r2_col2:
        if housing_filter in ['consideration', 'land_value', 'land_improvements']:
            elevation = st.slider("Elevation", min_value=0.1, max_value=1.0)
        elif housing_filter in ['market_value']:
            elevation = st.slider("Elevation", min_value=0.001, max_value=0.01)
        else:
            elevation = st.slider("Elevation", min_value=1, max_value=50)
        
    colors = cm.get_palette(palette)
    colors = [hex_to_rgb(c) for c in colors]
    for i, ind in enumerate(gdf.index):
        index = int(i / (len(gdf) / len(colors)))
        if index >= len(colors):
            index = len(colors) - 1
        gdf.loc[ind, "R"] = colors[index][0]
        gdf.loc[ind, "G"] = colors[index][1]
        gdf.loc[ind, "B"] = colors[index][2]

    initial_view_state = pdk.ViewState(
            latitude=df.latitude.mean(),
            longitude=df.longitude.mean(),
            zoom=3,
            max_zoom=16,
            pitch=0,
            bearing=0,
            height=700,
            width=None,
        )

    geojson = pdk.Layer(
            "GeoJsonLayer",
            gdf,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation= housing_filter,
            elevation_scale=elevation,
            # get_fill_color="color",
            get_fill_color=f"[R, G, B]",
            get_line_color=[0, 0, 0],
            get_line_width=2,
            line_width_min_pixels=1,
        )

    layers = [geojson]

    tooltip = {
            "html": "<b>Zipcode:</b> {zipcode} <br><b>Median Value:</b> {" +
            housing_filter +
            "}",
            "style": {"backgroundColor": "steelblue", "color": "white"},
            }

    r = pdk.Deck(
            layers=layers,
            initial_view_state=initial_view_state,
            map_style="light",
            tooltip=tooltip,
        )

    r3_col1, r3_col2 = st.columns([6, 1])
    with r3_col1:
        st.pydeck_chart(r)
    with r3_col2:
        st.write(
                cm.create_colormap(
                    palette,
                    label=f"Median {housing_filter}",
                    width=0.2,
                    height=3,
                    orientation="vertical",
                    vmin=gdf[housing_filter].min(),
                    vmax=gdf[housing_filter].max(),
                    font_size=10,
                )
            )

if geo_filter == 'Heatmap':
    
    if location_filter == 'Maryland':
        path = "Clean_MD_Property_Data.csv"
        df = load_data(path)
        
        # Housing Filter
        housing_filter = st.selectbox('Housing Features',
                                      ('Select a feature', 'consideration', 'land_value', 'land_improvements', 'sqft', 'year_built', 'grade'))
        
        if (housing_filter == 'Select a feature'):
            st.stop()        
        
    if location_filter == 'New York City':
        path = "Clean_NYC_Property_Data.csv"
        df = load_data(path)
        df = df.sample(200000)
        
        # Housing Filter 
        housing_filter = st.selectbox('Housing Features',
                                      ('Select a feature', 'market_value'))
        
        if (housing_filter == 'Select a feature'):
            st.stop()

    initial_view_state = pdk.ViewState(
        latitude=df.latitude.mean(),
        longitude=df.longitude.mean(),
        zoom=3,
        max_zoom=16,
        pitch=0,
        bearing=0,
        height=900,
        width=None,
    )
    
    heatmap = pdk.Layer(
        "HeatmapLayer",
        data=df,
        opacity=0.9,
        get_position=["longitude", "latitude"],
        aggregation=pdk.types.String("MEAN"),
        threshold=1,
        get_weight=housing_filter,
        pickable=True
        )

    r = pdk.Deck(
                layers=[heatmap],
                initial_view_state=initial_view_state,
                map_provider="mapbox",
                map_style=pdk.map_styles.SATELLITE,
            )
    
    st.pydeck_chart(r)

if geo_filter == 'HexagonLayer':
    
    if location_filter == 'Maryland':
        path = "Clean_MD_Property_Data.csv"
        df = load_data(path)
    
    if location_filter == 'New York City':
        path = "Clean_NYC_Property_Data.csv"
        df = load_data(path)
        df = df.sample(200000)

    initial_view_state = pdk.ViewState(
        latitude=df.latitude.mean(),
        longitude=df.longitude.mean(),
        zoom=3,
        max_zoom=16,
        pitch=0,
        bearing=0,
        height=900,
        width=None,
    )
    
    hexagon = pdk.Layer(
        "HexagonLayer",
        df,
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=1,
    )

    r = pdk.Deck(
                layers=[hexagon],
                initial_view_state=initial_view_state,
                map_provider="mapbox",
                map_style=pdk.map_styles.LIGHT,
            )
    
    st.pydeck_chart(r)

# %%
