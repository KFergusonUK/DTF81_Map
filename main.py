import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt

# Path to the Geoplace DTF8.1 format CSV file
dtf_file_path = 'LG.csv'

# Read the DTF8.1 format CSV file into a DataFrame
df = pd.read_csv(dtf_file_path, delimiter=',', header=None, skiprows=1)

# Select the columns for start and end coords
start_easting = df.iloc[:, 14].astype(float)
start_northing = df.iloc[:, 15].astype(float)
end_easting = df.iloc[:, 16].astype(float)
end_northing = df.iloc[:, 17].astype(float)

# Create LineString geometries from start and end coordinates
lines = [LineString([(start_easting[i], start_northing[i]), (end_easting[i], end_northing[i])])
         for i in range(len(df))]

# Create a GeoDataFrame from the lines
gdf = gpd.GeoDataFrame(df, geometry=lines)

# Create a plot of the data
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the GeoDataFrame as lines
gdf.plot(ax=ax, linestyle='-', color='blue')

# Customize the plot appearance
ax.set_aspect('equal')
ax.set_xlabel('Easting')
ax.set_ylabel('Northing')
ax.set_title('Street Gazetteer Data Map')

# Display the plot
plt.show()
