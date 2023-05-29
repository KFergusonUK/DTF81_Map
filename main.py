import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
import preprocess
import simple
import matplot
import plotlyplot
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
    simple_detailed = input("Would you like a read in the data file for a detailed map? \nType S to create a simple map from type 11 data only.\nType M to create a MatplotLib map.\nType P to create a Plotly map.\nS/M/P? ")
    if simple_detailed == "M":
      #Create a MatPlotLib map:
      matplot.plotLib()
    elif simple_detailed == "S":
      #Create a simple map:
      simple.sMap()
    elif simple_detailed == "P":
      #Create Plotly map.
      plotlyplot.plotly_plot()
    else:
      #Else just create a simple map.
      simple.sMap()
else:
    print("You did not enter Y or N.")
