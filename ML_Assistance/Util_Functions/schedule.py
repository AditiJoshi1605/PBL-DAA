import pandas as pd

def get_bus_details(stop_point: str):
    # Load and prepare the data
    df = pd.read_csv("../assets/bus_schedule.csv")
    df.columns = df.columns.str.strip()  # Clean headers
    df['Time'] = df['Time'].astype(str).str.strip() + ' ' + df['Arc'].astype(str).str.strip()

    # Normalize stop_point for case-insensitive comparison
    stop_point = stop_point.lower()
    
    incoming_buses = df[df['Next_Stop'].str.lower() == stop_point]
    on_stop_buses = df[df['Current_Location'].str.lower() == stop_point]

    results = []

    # Add "On Stop" and "Outgoing" buses (current location = stop)
    for _, row in on_stop_buses.iterrows():
        bus_id = row['Bus_No']
        driver = row['Driver_Name']
        time = row['Time']
        contact = row['Contact_No']
        next_stop = row['Next_Stop']
        
        results.append([
            driver,
            bus_id,
            "On Stop",
            [time],
            next_stop,
            ["Unknown (next row not available)"]
        ])

        # Try to find the *next* time from same bus to calculate outgoing time
        next_rows = df[(df['Bus_No'] == bus_id) & (df['Current_Location'].str.lower() != stop_point)]
        if not next_rows.empty:
            next_time = next_rows.iloc[0]['Time']
            results[-1][-1] = [next_time]  # Set outgoing time

    # Add incoming buses
    for _, row in incoming_buses.iterrows():
        bus_id = row['Bus_No']
        driver = row['Driver_Name']
        time = row['Time']
        contact = row['Contact_No']
        from_stop = row['Current_Location']
        
        results.append([
            driver,
            bus_id,
            "Incoming.",
            [time],
            stop_point.title(),
            ["Will reach at this time"]
        ])

    # Display nicely
    print(f"\n🚏 Bus Details for Stop: {stop_point.title()}\n{'='*45}")
    if not results:
        print("No buses found.")
        return

    for item in results:
        driver, bus_id, status, time, next_stop, next_time = item
        print(f"[{driver}, Bus {bus_id}, {status}, {time}, Next: {next_stop}, {next_time}]")
