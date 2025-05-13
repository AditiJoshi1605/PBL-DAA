
import folium
import pandas as pd
df_loc = pd.read_csv('../assets/location_coordinates_final.csv')
df_loc = df_loc.dropna(subset=['Latitude','Longitude']) 
def mapper(x):
    if(x):
        count = 0
        center_lat, center_lon = df_loc['Latitude'].iloc[0], df_loc['Longitude'].iloc[0]
        m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

        # Add markers for each location
        for index, row in df_loc.iterrows():
        # Display location name and coordinates as popup
            folium.Marker([row['Latitude'], row['Longitude']], popup=f"Loc : {row['name']}\n  \nLat: {row['Latitude']}\n  Lon: {row['Longitude']}").add_to(m)
            count = count+1
        print(f"Total locations plotted : {count}")
        return m