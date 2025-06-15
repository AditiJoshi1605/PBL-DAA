
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

def selective(names_list):
    # Normalize the case of both names_list and 'name' column in the dataframe
    names_list = [name.strip().lower() for name in names_list]  # Strip and convert to lower case
    df_loc['name_normalized'] = df_loc['name'].str.strip().str.lower()  # Normalize 'name' column
    
    # Filter the dataframe to only include rows with the names in the list
    selected_df = df_loc[df_loc['name_normalized'].isin(names_list)]
    
    if not selected_df.empty:
        count = 0
        # Center the map around the first selected location
        center_lat, center_lon = selected_df['Latitude'].iloc[0], selected_df['Longitude'].iloc[0]
        m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

        # Add markers for the selected locations
        for index, row in selected_df.iterrows():
            # Display location name and coordinates as popup
            folium.Marker([row['Latitude'], row['Longitude']], popup=f"Loc: {row['name']}\n\nLat: {row['Latitude']}\nLon: {row['Longitude']}").add_to(m)
            count += 1
        print(f"Total selected locations plotted: {count}")
        return m
    else:
        print("No locations found in the list.")
        return None
