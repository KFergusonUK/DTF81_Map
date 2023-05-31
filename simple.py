import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt

input_file_path = 'LG.csv'

def sMap():
    # Specify the column numbers to be read from the CSV file
    columns_to_read = [0, 14, 15, 16, 17]

    # Specify the column names for better readability
    column_names = ['Type', 'Start Easting', 'Start Northing', 'End Easting', 'End Northing']

    # Specify the data types for the columns with mixed types
    column_dtypes = {'Type': str, 'Start Easting': float, 'Start Northing': float,
                     'End Easting': float, 'End Northing': float}

    # Read the CSV file and select only the desired columns
    df = pd.read_csv(input_file_path, delimiter=',', header=None, skiprows=1, usecols=columns_to_read, names=column_names, dtype=column_dtypes)

    # Filter rows where the 'Type' column is either "11", "12", or "13"
    df = df[df['Type'].isin(['11'])]

    # Create LineString geometries from start and end coordinates
    lines = [LineString([(row['Start Easting'], row['Start Northing']), (row['End Easting'], row['End Northing'])])
             for _, row in df.iterrows()]

    # Create a GeoDataFrame from the lines
    gdf = gpd.GeoDataFrame(df, geometry=lines)

    # Create a plot of the data
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the GeoDataFrame as lines
    if not gdf.empty:  # Check if the GeoDataFrame is not empty
        gdf.plot(ax=ax, linestyle='-', color='blue')

        # Customize the plot appearance
        ax.set_aspect('equal')
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')
        ax.set_title('Street Gazetteer (Type 11) Map')

        # Display the plot
        plt.axis("off")
        plt.show()
    else:
        print("No data to plot.")

