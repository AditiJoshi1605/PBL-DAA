import pandas as pd
from duckduckgo_search import DDGS
import time
import re
import csv
import os

# Set working directory to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_distance_from_search(origin, destination):
    query = f"distance from {origin}, Dehradun to {destination}, Dehradun in km"
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query)
            for r in results:
                txt = r.get("body", "")
                match = re.search(r"(\d+(?:\.\d+)?)\s*(?:km|kilometers)", txt.lower())
                if match:
                    return float(match.group(1))
        return None
    except Exception as e:
        print(f"Error getting distance from {origin} to {destination}: {e}")
        return None


def build_distance_matrix(locations):
    n = len(locations)
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0
                continue

            origin = locations[i]
            destination = locations[j]
            print(f"Searching: {origin} → {destination}")
            distance = get_distance_from_search(origin, destination)
            if distance is not None:
                matrix[i][j] = round(distance, 2)
            else:
                matrix[i][j] = "N/A"

            time.sleep(1.5)  # avoid rate limiting

    return matrix

def save_matrix_csv(locations, matrix, output_file="distance_matrix_output.csv"):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["", "name"] + locations)  # Header row
        for i, row in enumerate(matrix):
            writer.writerow([i, locations[i]] + row)

def main():
    input_csv = "final_routes.csv"  # Your input CSV file (must have a column named 'name')
    df = pd.read_csv(input_csv)
    locations = df['name'].dropna().tolist()
    

    matrix = build_distance_matrix(locations)
    save_matrix_csv(locations, matrix)
    print(f"✅ Saved distance matrix to 'distance_matrix_output.csv'")

if __name__ == "__main__":
    main()
