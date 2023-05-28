import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
import preprocess
import simple
import re
import matplotlib.pyplot as plt


from shapely import wkt

# File paths
input_file_path = 'LG.csv'
processed_file_path = 'LG_Processed.csv'

# Ask user if initial pre-processing is required
setup_file = input("Would you like to create a mapping file from your input data? This is required, for a detailed map, when a new data source is added (initial setup will take some time). Y/N?: \n")

if setup_file == "Y":
    # Preprocess the CSV file (optional)
    df_streets, df_xref, df_esu_coords = preprocess.preprocess_csv(input_file_path)

elif setup_file == "N":
    simple_detailed = input("Would you like a read in the data file for a detailed map, type N to create a simple map from type 11 data only. Y/N? ")
    if simple_detailed == "Y":
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

              print(df)
            
              # Plot the geometries on a map
              gdf.plot()
          
              # Display the map
              plt.show()
          else:
              print("The 'geometry' column does not exist in the DataFrame.")
          
      except FileNotFoundError:
          print("Processed file not found. Please run the initial setup to create the mapping file.")

        


    else:
      #Create a simple map if any response other than Y:
      simple.sMap()
else:
    print("You did not enter Y or N.")
