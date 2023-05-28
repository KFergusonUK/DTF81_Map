import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point

processed_file_path = 'LG_Processed.csv'

def preprocess_csv(file_path):
    # Specify the relevant types to extract (so far)
    relevant_types = [11, 12, 13, 14]

    # Initialize empty lists to store the extracted records
    street_records = []
    xref_records = []
    esu_coords = []
    records_count = 0

    # Read the CSV file
    with open(file_path, 'r') as file:
        for line in file:
            record = line.strip().split(',')
            record_type = int(record[0])

            # Check if the record type is relevant
            if record_type in relevant_types:
                if record_type == 11:
                    street_records.append(record)
                    records_count += 1
                elif record_type == 12:
                    xref_records.append(record)
                elif record_type == 13:
                    pass
                elif record_type == 14:
                    esu_coords.append(record)

    # Convert the lists of records into DataFrames
    df_streets = pd.DataFrame(street_records)
    df_xref = pd.DataFrame(xref_records)
    df_esu_coords = pd.DataFrame(esu_coords)

    usrnEsus = []
    streets = []
    current_row = 0

    for _, row in df_streets.iterrows():
        current_row += 1
        print("Now processing record " + str(current_row) + " of " + str(records_count))
        matching_xref_rows = df_xref[df_xref.iloc[:, 3] == row[3]]

        if not matching_xref_rows.empty:
            for _, xrefrow in matching_xref_rows.iterrows():
                matching_esu = df_esu_coords[df_esu_coords.iloc[:, 3] == xrefrow[5]]
                if not matching_esu.empty:
                    for _, esurow in matching_esu.iterrows():
                        usrnEsus.append([xrefrow[3], esurow[6], esurow[7]])

        start = Point(float(row[14]), float(row[15]))
        end = Point(float(row[16]), float(row[17]))

        matching_usrn_esus = [item for item in usrnEsus if item[0] == row[3]]

        if matching_usrn_esus:
            line_points = [start]
            for usrn_esu in matching_usrn_esus:
                esu_point = Point(float(usrn_esu[1]), float(usrn_esu[2]))
                line_points.append(esu_point)
            line_points.append(end)
            street = LineString(line_points)
        else:
            street = LineString([start, end])

        streets.append(street)

    # Create a new column named "geometry" in df_streets_subset
    df_streets['geometry'] = streets
    df_streets_subset = df_streets[[3, 'geometry']]

    # Create the GeoDataFrame from streets and df_streets_subset
    gdf_streets = gpd.GeoDataFrame(df_streets_subset, geometry='geometry', crs='EPSG:27700')

    # Save the processed data to a new CSV file
    gdf_streets.to_csv(processed_file_path, index=False)

    # Return the processed DataFrames
    return df_streets, df_xref, df_esu_coords
