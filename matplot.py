import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
import re
import matplotlib.pyplot as plt

def plotLib():
  
  
  # try to read the processed data from the file
      try:

          # Helper function to convert coordinates to LineString
          def create_linestring(coords):
              if len(coords) >= 2:
                  return LineString(coords)
              else:
                  return None
                    
          # Read the CSV file into a DataFrame
          df = pd.read_csv('LG_Processed.csv', header=None, names=['record_type', 'geometry'])
          
          # Check if the 'geometry' column exists
          if 'geometry' in df.columns:
              # Extract coordinates and convert to LineString
              df['geometry'] = df['geometry'].apply(
                  lambda x: create_linestring([
                      tuple(map(float, coord.split())) for coord in re.findall(r'\d+\.\d+ \d+\.\d+', x)
                  ])
              )
          
              # Create a GeoDataFrame with the correct geometry type
              gdf = gpd.GeoDataFrame(df, geometry='geometry')

              #print(df)
            
              # Plot the geometries on a map
              gdf.plot()
          
              # Display the map
              plt.show()
          else:
              print("The 'geometry' column does not exist in the DataFrame.")
          
      except FileNotFoundError:
          print("Processed file not found. Please run the initial setup to create the mapping file.")