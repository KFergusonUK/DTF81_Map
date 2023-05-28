import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point

processed_file_path = 'LG_Processed.csv'

def preprocess_csv(file_path):
  
  # NEED TO PUT THIS IN SEPERATE FILE AS A FUNCTION - Process takes too long and needs to be a pre-processing option with count.

  # Specify the relevant types to extract (so far)
  relevant_types = [11, 12, 13, 14]

  # Initialize empty lists to store the extracted records
  street_records = []
  xref_records = []
  esu_records = []
  esu_coords = []
  countTotal = 0
  
  # Read the CSV file
  with open('LG2.csv', 'r') as file:
      for line in file:
          record = line.strip().split(',')
          record_type = int(record[0])
          
          # Check if the record type is relevant
          if record_type in relevant_types:
              if record_type == 11:
                  street_records.append(record)
              elif record_type == 12:
                  xref_records.append(record)
              elif record_type == 13:
                  # Process type 13 (ESU Record) records if needed
                  # esu_records.append(record)
                  pass
              elif record_type == 14:
                  # Process type 14 (ESU Coordinates) records
                  esu_coords.append(record)

  # Convert the lists of records into DataFrames
  df_streets = pd.DataFrame(street_records)
  df_xref = pd.DataFrame(xref_records)
  df_esu_coords = pd.DataFrame(esu_coords)
  
  # Perform further processing on the extracted DataFrames
  # 
  # For every type 11 Street record listed in df_streets, check if there is an associated esu record in df_esu_coords, by using df_xref to determine if the street USRN exists in Index 3 and if any associated ESU references exist in Index 5.  If they do add to the street as mid points.

  # If we have start and end coordinate information in the type 11 records:
  # Create a GeoDataFrame from the type 11 records
  #Pull out the matching USRN with ESU Coords, for each ESU point associated with the USRN and add to array.

  usrnEsus = []
  streets = []

  #Use this small section to setup count of processing:
  countTotal = len(street_records)
  countCurrent = 1
  
  for _, row in df_streets.iterrows():
      print("Processing record: " + str(countCurrent) + " of " + str(countTotal))
      matching_xref_rows = df_xref[df_xref.iloc[:, 3] == row[3]]
      countCurrent += 1
      if not matching_xref_rows.empty:
          # Process when there is a match
          for _, xrefrow in matching_xref_rows.iterrows():
              matching_esu = df_esu_coords[df_esu_coords.iloc[:, 3] == xrefrow[5]]
              if not matching_esu.empty:
                  # Process when there is a matching ESU record
                  for _, esurow in matching_esu.iterrows():
                      usrnEsus.append([xrefrow[3], esurow[6], esurow[7]])
          # Modify the row as needed and append it to streets
          start = Point(float(row[14]), float(row[15]))
          end = Point(float(row[16]), float(row[17]))
        
         # Check if there are associated ESU coordinates
          matching_usrn_esus = [item for item in usrnEsus if item[0] == row[3]]
          if matching_usrn_esus:
              # Create mid-point LineString using the ESU coordinates
              line_points = [start]
              for usrn_esu in matching_usrn_esus:
                  esu_point = Point(float(usrn_esu[1]), float(usrn_esu[2]))
                  line_points.append(esu_point)
              line_points.append(end)
              street = LineString(line_points)
              #print(street)
          else:
              # No associated ESU coordinates, use original start and end points
              street = LineString([start, end])
        
          streets.append(street)
      else:
          # No match, copy the row as it is to streets
          start = Point(float(row[14]), float(row[15]))
          end = Point(float(row[16]), float(row[17]))
          street = LineString([start, end])
          streets.append(street)
          

  print(streets)
  input()

#THIS BIT IS NOT WORKING CORRECTLY YET!!!
  
  #gdf_streets = gpd.GeoDataFrame(streets, columns=df_streets.columns, geometry='geometry', crs='EPSG:27700')

  # Extract the relevant columns from df_streets
  street_columns = df_streets.columns.tolist()
  street_columns.append('geometry')
  df_streets_subset = df_streets[street_columns]
  # Create the GeoDataFrame from streets and df_streets_subset
  gdf_streets = gpd.GeoDataFrame(df_streets_subset, geometry=streets, crs='EPSG:27700')

  
  # Save the processed data to a new CSV file (optional)
  gdf_streets.to_csv(processed_file_path, index=False)
  
  # Return the processed DataFrames
  return df_streets, df_xref, df_esu_coords
  