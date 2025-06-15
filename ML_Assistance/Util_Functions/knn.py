import pandas as pd
from typing import List, Tuple

# Path to the distance log file
DISTANCE_LOG_CSV = "../assets/distances_log.csv"

def nearest(stop_name: str, k: int = 10) -> List[Tuple[str, float]]:
    

    """
    Find the k nearest stations to a given stop using the precomputed distance log.

    Parameters:
        stop_name (str): Name of the stop to search from.
        k (int): Number of nearest stations to return.

    Returns:
        List of (station_name, distance) tuples sorted by nearest.
    """




    df = pd.read_csv(DISTANCE_LOG_CSV)

    if stop_name not in df['name'].values:
        raise ValueError(f"Stop '{stop_name}' not found in the distance log.")

    # Extract the row for the given stop
    row = df[df['name'] == stop_name].iloc[0]

    # Drop irrelevant columns (like index or name itself)
    distances = row.drop(labels=['name'])

    # Remove empty values and self-distance
    cleaned_distances = distances.dropna()
    cleaned_distances = cleaned_distances[cleaned_distances.index != stop_name]

    # Convert to list of (stop, distance) tuples
    nearest = [(station, float(dist)) for station, dist in cleaned_distances.items()]

    # Sort by distance
    nearest.sort(key=lambda x: x[1])



    return nearest[:k]
