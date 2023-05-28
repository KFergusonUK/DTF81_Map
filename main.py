import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
import preprocess
import simple

# File paths
input_file_path = 'LG2.csv'
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
          df_processed = pd.read_csv(processed_file_path)

          # Extract the necessary information for plotting on the map
          streets = []
          for _, row in df_processed.iterrows():
              # Process the row and append it to streets
              # ...
              continue
              #ADD CODE HERE. ******

          gdf_streets = gpd.GeoDataFrame(streets, columns=df_processed.columns, geometry='geometry', crs='EPSG:27700')

         # Plot the data on a map
          gdf_streets.plot()

          # Display the map
          import matplotlib.pyplot as plt
          plt.axis("off")
          plt.show()

      except FileNotFoundError:
          print("Processed file not found. Please run the initial setup to create the mapping file.")
    else:
      #Create a simple map if any response other than Y:
      simple.sMap()
else:
    print("You did not enter Y or N.")
