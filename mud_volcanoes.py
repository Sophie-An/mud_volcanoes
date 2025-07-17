import streamlit as st
import folium
import pandas as pd
from folium import IFrame
from streamlit_folium import st_folium
from folium import FeatureGroup


# Title
st.title("Global Mud Volcano Explorer 🌋")

# ---------- Mud Volcano Data ----------
mud_data = {
    "Mud Volcano": [
        "Lei-Gong-Hou", "Goshogake Onsen", "Niikappu", "Murono (Tokamachi)", "Kamou (Tokamachi)", "Devil's Woodyard", 
        "Moruga Bouffe", "Erin Bouffe", "Digity Mud Volcano", "Salton Sea (Davis-Schrimpf)", "Mendocino Coast", 
        "Tolsona", "Klawasi Group"
    ],
    "Country/Region": [
        "Eastern Taiwan", "Tohoku, Japan", "Hokkaido, Japan", "Niigata Basin, Japan", "Niigata Basin, Japan", "Trinidad & Tobago", 
        "Trinidad & Tobago", "Trinidad & Tobago", "Trinidad & Tobago", "Southern California, USA", "Northern California, USA", 
        "Alaska, USA", "Alaska, USA"
    ],
    "Coordinates": [
        "22.983° N, 121.209° E", "39.883° N, 140.817° E", "42.417° N, 142.183° E", "37.121° N, 138.558° E", "37.134° N, 138.578° E",
        "10.180° N, 61.358° W", "10.150° N, 61.250° W", "10.150° N, 61.347° W", "10.270° N, 61.400° W", 
        "33.204° N, 115.579° W", "39.450° N, 123.800° W", "62.113° N, 145.975° W", "62.467° N, 144.250° W"
    ],
    "Nearest City/Town": [
        "Chenggong Township", "Kazuno, Akita", "Niikappu Town", "Tokamachi City", "Tokamachi City", "Princes Town", 
        "Moruga", "Los Iros", "Barrackpore", "Niland", "Fort Bragg", "Paxson", "Chitina"
    ],
    "Distance to City": [
        "20 km", "12 km", "<5 km", "<10 km", "<10 km", "~4 km", "<2 km", "~2 km", "~3 km", "~12 km", "~8 km", "~40 km", "~30 km"
    ],
    "Gas Infrastructure Nearby": [
        "Limited rural pipelines", "Regional gas supply", "Local propane distribution", "Onshore gas network", "Onshore gas network", 
        "National grid access", "Regional oil/gas field", "Regional oil/gas field", "National grid access", "Gas and geothermal infra", 
        "PG&E natural gas grid", "Remote – no pipelines", "Remote – no pipelines"
    ],
    "Eruptive?": [
        "No", "No", "Yes", "Yes", "No", "Yes", "No", "No", "No", "No", "No", "No", "No"
    ],
    "Methane Flow (tons/yr)": [
        29, None, None, 20, 3.7, None, None, None, 3, 3.41, None, None, None
    ],
    "Morphology": [
        "Shield", "Salsa ponds, gryphons, and mud pots", "Cone", "Cone", "Cone", "Cone", "Cone", "Mud pools", "Cone", "Mud Pots", 
        "Cone/Dome", "Cone", "Cone, Mud pools"
    ],
    "Size": [
        "150 m x 50 m", None, "70 m x 100 m", "130 m x 180 m", "20 cm diameter vent", "< 30 cm tall", "1000 m x 670 m, 30 m tall", 
        "0.25 ha area, < 20 ft tall", "63 ft tall", "100 m x 100 m", "< 2 m tall", "180 m x 270 m x 8 m", "35 m diameter, 50-100 m tall"
    ]
}

mud_df = pd.DataFrame(mud_data)

# ---------- Gas Seep Data ----------
gas_data = {
    "Gas Seep": [
        "Enriquillo Basin", "Kushiro Gas Field", "Kyushu Island", "Chihpen & Hengchun", "Taipei Basin",
        "Alberta Gas Seeps", "San Juan Basin", "Great Basin", "Basin and Range Province"
    ],
    "Country/Region": [
        "Dominican Republic", "Japan (Hokkaido)", "Japan", "Taiwan", "Taiwan",
        "Canada (Alberta)", "USA (New Mexico)", "USA (Nevada)", "USA (Nevada)"
    ],
    "Coordinates": [
        "18.5°N, 71.0°W", "43.0°N, 144.0°E", "32.0°N, 130.0°E", "22.0°N, 120.7°E", "25.0°N, 121.5°E",
        "52.0°N, 114.0°W", "36.5°N, 107.5°W", "39.5°N, 116.5°W", "39.0°N, 112.0°W"
    ],
    "Nearest City/Town": [
        "Santo Domingo", "Kushiro", "Nagasaki", "Taitung", "Taipei",
        "Calgary", "Farmington", "Ely", "Delta"
    ],
    "Distance to City": [
        "~200 km", "~20 km", "~40-60 km", "~80 km", "~15 km", "~50-60 km", "~30-40 km", "~80 km", "~50 km"
    ],
    "Gas Infrastructure Nearby": [
        "Limited infrastructure", "Well-developed gas infrastructure", "Extensive infrastructure",
        "Moderate infrastructure", "Extensive infrastructure", "Extensive pipeline network",
        "Significant pipeline network", "Minimal infrastructure", "Natural gas pipelines nearby"
    ],
    "Size": [
        "Small", "Small to medium", "Small", "Small to medium", "Small",
        "Small to medium", "Medium to large", "Small to medium", "Medium to large"
    ]
}

gas_df = pd.DataFrame(gas_data)

# ---------- Coordinate Converter ----------
# def convert_to_decimal(coord):
#     lat_str, lon_str = coord.split(", ")
#     lat_val = float(lat_str[:-2])
#     lon_val = float(lon_str[:-2])
#     lat = lat_val if 'N' in lat_str else -lat_val
#     lon = lon_val if 'E' in lon_str else -lon_val
#     return lat, lon

def convert_to_decimal(coord):
    lat_str, lon_str = coord.split(", ")
    lat_deg, lat_dir = lat_str.split("°")
    lon_deg, lon_dir = lon_str.split("°")
    lat = float(lat_deg) if lat_dir.strip() == "N" else -float(lat_deg)
    lon = float(lon_deg) if lon_dir.strip() == "E" else -float(lon_deg)
    return lat, lon

mud_df[['lat', 'lon']] = mud_df['Coordinates'].apply(lambda x: pd.Series(convert_to_decimal(x)))
gas_df[['lat', 'lon']] = gas_df['Coordinates'].apply(lambda x: pd.Series(convert_to_decimal(x)))

# ---------- Create Map ----------
m = folium.Map(location=[30, 0], zoom_start=2)
mud_group = FeatureGroup(name='Mud Volcanoes')
gas_group = FeatureGroup(name='Gas Seeps')

# ---------- Add Mud Volcano Markers ----------
for _, row in mud_df.iterrows():
    popup_html = f"""
    <b>Name:</b> {row['Mud Volcano']}<br>
    <b>Location:</b> {row['Country/Region']}<br>
    <b>Nearest City/Town:</b> {row['Nearest City/Town']} ({row['Distance to City']})<br>
    <b>Gas Infrastructure Nearby:</b> {row['Gas Infrastructure Nearby']}<br>
    <b>Eruptive?</b> {row['Eruptive?']}<br>
    <b>Methane Flow (tons/yr):</b> {row['Methane Flow (tons/yr)']}<br>
    <b>Morphology:</b> {row['Morphology']}<br>
    <b>Size:</b> {row['Size']}<br>
    """
    popup = folium.Popup(IFrame(popup_html, width=250, height=300), max_width=300)
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color='red' if row['Eruptive?'] == 'Yes' else 'green',
        fill=True,
        fill_color='red' if row['Eruptive?'] == 'Yes' else 'green',
        fill_opacity=0.7,
        popup=popup
    ).add_to(mud_group)

# ---------- Add Gas Seep Markers ----------
for _, row in gas_df.iterrows():
    popup_html = f"""
    <b>Name:</b> {row['Gas Seep']}<br>
    <b>Location:</b> {row['Country/Region']}<br>
    <b>Nearest City/Town:</b> {row['Nearest City/Town']} ({row['Distance to City']})<br>
    <b>Gas Infrastructure Nearby:</b> {row['Gas Infrastructure Nearby']}<br>
    <b>Size:</b> {row['Size']}<br>
    """
    popup = folium.Popup(IFrame(popup_html, width=250, height=200), max_width=300)
    folium.Marker(
        location=[row['lat'], row['lon']],
        icon=folium.Icon(color='blue', icon='cloud'),
        popup=popup
    ).add_to(gas_group)

# ---------- Add Groups and Controls ----------
mud_group.add_to(m)
gas_group.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)

# Streamlit map display
st.subheader("Mud Volcano and Gas Seep Map")
st_data = st_folium(m, width=700, height=500)

# Optional table display
with st.expander("Show Mud Volcano Data Table"):
    st.dataframe(mud_df.drop(columns=["lat", "lon"]))

with st.expander("Show Gas Seep Data Table"):
    st.dataframe(gas_df.drop(columns=["lat", "lon"]))
