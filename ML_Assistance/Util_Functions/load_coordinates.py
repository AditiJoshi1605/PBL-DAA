import pandas as pd

def load_coordinates(file_path):
    coords = pd.read_csv(file_path)
    coord_dict = coords.set_index("name")[["Latitude","Longitude"]].to_dict("index")
    return coord_dict,coords