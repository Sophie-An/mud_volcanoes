import streamlit as st
import folium
import pandas as pd
from folium import IFrame
from streamlit_folium import st_folium

# Title
st.title("Global Onshore Mud Volcano Explorer 🌋")

# Data for Mud Volcanoes (coordinates updated from the provided list)
data = {
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
        "22.983° N, -121.209° E",    # Lei-Gong-Hou, Taiwan
        "39.883° N, -140.817° E",    # Goshogake Onsen, Japan
        "42.417° N, -142.183° E",    # Niikappu, Japan
        "37.121° N, -138.558° E",    # Murono (Tokamachi), Japan
        "37.134° N, -138.578° E",    # Kamou (Tokamachi), Japan
        "10.180° N, 61.358° W",     # Devil's Woodyard, Trinidad
        "10.150° N, 61.250° W",     # Moruga Bouffe, Trinidad (approx.)
        "10.150° N, 61.347° W",     # Erin Bouffe, Trinidad (approx.)
        "10.270° N, 61.400° W",     # Digity Mud Volcano, Trinidad (approx.)
        "33.204° N, 115.579° W",    # Salton Sea (Davis–Schrimpf), California
        "39.450° N, 123.800° W",    # Mendocino Coast, California (approx.)
        "62.113° N, 145.975° W",    # Tolsona, Alaska
        "62.467° N, 144.250° W"     # Klawasi Group, Alaska
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

# Create a DataFrame
df = pd.DataFrame(data)

# Function to create the popup for each volcano
def create_popup(row):
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
    iframe = IFrame(popup_html, width=250, height=300)
    return folium.Popup(iframe, max_width=300)

# Function to set the color based on whether the volcano is eruptive
def get_color(eruptive):
    return 'red' if eruptive == "Yes" else 'green'

# Function to convert coordinates to decimal degrees
def convert_to_decimal_degrees(coord):
    # Split the coordinate string into latitude and longitude
    lat_str, lon_str = coord.split(", ")
    
    # Remove any en-dash (–) and replace with hyphen (-) for negative values
    lon_str = lon_str.replace("–", "-")
    
    # Extract latitude (e.g., '22.983° N') and longitude (e.g., '121.209° E')
    lat_deg, lat_dir = lat_str.split("°")
    lon_deg, lon_dir = lon_str.split("°")
    
    # Convert to decimal degrees
    lat_decimal = -float(lat_deg) if lat_dir == "N" else float(lat_deg)
    lon_decimal = float(lon_deg) if lon_dir == "E" else -float(lon_deg)
    
    return lat_decimal, lon_decimal

# Initialize map, centered around the average coordinates
m = folium.Map(location=[25, 25], zoom_start=2)

# Add circles to the map for each mud volcano
for _, row in df.iterrows():
    # Extract and convert coordinates to decimal degrees
    lat, lon = convert_to_decimal_degrees(row['Coordinates'])
    
    # Determine if the volcano is eruptive
    eruptive = row['Eruptive?']
    
    # Add circle marker with the popup
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color=get_color(eruptive),
        fill=True,
        fill_color=get_color(eruptive),
        fill_opacity=0.6,
        popup=create_popup(row)
    ).add_to(m)

# Save map to an HTML file
# m.save("mud_volcano_map_corrected.html")

# Streamlit map display
st.subheader("Mud Volcano Map")
st_data = st_folium(m, width = 700, height = 500)

# data table
with st.expander("Show Volcano Data Table"):
    st.dataframe(df.drop(columns=["lat","lon"]);
