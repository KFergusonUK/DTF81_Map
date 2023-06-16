def preprocess_type_11(file_path):

    import csv
    import pandas as pd
    import geopandas as gpd
  
    # Specify the column numbers to be read from the CSV file
    columns_to_read = [0, 14, 15, 16, 17]

    # Specify the column names for better readability
    column_names = ['Type', 'Start Easting', 'Start Northing', 'End Easting', 'End Northing']

    # Initialize an empty list to store the valid rows
    rows = []

    # Read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == '11':  # Filter rows where the 'Type' column is "11" only
                # Check if the coordinate values can be converted to float
                try:
                    start_easting = float(row[14])
                    start_northing = float(row[15])
                    end_easting = float(row[16])
                    end_northing = float(row[17])
                    rows.append([row[3], start_easting, start_northing, end_easting, end_northing])
                except ValueError:
                    pass

    # Create a DataFrame from the list of valid rows
    df = pd.DataFrame(rows, columns=column_names)

    return df




def preprocess_type_15(file_path):

    import csv
    import pandas as pd
    import geopandas as gpd
    
    # Specify the column numbers to be read from the CSV file
    columns_to_read = [0, 3, 4, 6]

    # Specify the column names for better readability
    column_names = ['Type', 'USRN', 'Street', 'Town']

    # Initialize an empty list to store the valid rows
    rows = []

    # Read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == '15':  # Filter rows where the 'Type' column is "15" only
                rows.append([row[col_idx] for col_idx in columns_to_read])

    # Create a DataFrame from the list of valid rows
    df = pd.DataFrame(rows, columns=column_names)

    return df


import csv
import pandas as pd
import numpy as np

def preprocess_single_street(file_path, selected_street_usrn):
    # Increase the display options
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.width', None)  # Disable column width wrapping

    # Specify the column names for better readability
    column_names = ['USRN', 'Start Easting', 'Start Northing', 'End Easting', 'End Northing', 'Mid Eastings', 'Mid Northings']

    # Initialize empty lists to store the valid rows
    rows = []

    # Read the CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == '11' and row[3] == selected_street_usrn:  # Filter rows where the 'Type' column is "11" and USRN matches
                # Check if the coordinate values can be converted to float
                try:
                    start_easting = float(row[14])
                    start_northing = float(row[15])
                    end_easting = float(row[16])
                    end_northing = float(row[17])
                    rows.append([row[3], start_easting, start_northing, end_easting, end_northing, [], []])
                except ValueError:
                    pass

    # Read the CSV file again to extract XRef (type 12) and ESU (type 14) records
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        rows_list = list(reader)  # Convert the reader object to a list

    esu_coords = {}
    for row in rows_list:
        if row[0] == '12' and row[3] == selected_street_usrn:  # Filter XRef records where USRN matches
            esu_id = row[5]
            matching_esu_rows = [r for r in rows_list if r[0] == '14' and r[3] == esu_id]  # Find matching ESU records
            esu_points = []
            for esu_row in matching_esu_rows:
                try:
                    esu_easting = float(esu_row[6])
                    esu_northing = float(esu_row[7])
                    esu_points.append((esu_easting, esu_northing))
                except ValueError:
                    pass
            esu_coords[esu_id] = esu_points

    # Append the mid eastings and mid northings to the corresponding rows
    for row in rows:
        usrn = row[0]
        start_easting, start_northing, end_easting, end_northing = row[1], row[2], row[3], row[4]
        mid_eastings = []
        mid_northings = []
        for esu_id in esu_coords:
            esu_points = esu_coords[esu_id]
            mid_eastings.extend([point[0] for point in esu_points])
            mid_northings.extend([point[1] for point in esu_points])
        row[5] = mid_eastings
        row[6] = mid_northings

    # Create a DataFrame from the rows list using the column names
    df = pd.DataFrame(rows, columns=column_names)

    # Replace empty lists with NaN values
    df.replace([], np.nan, inplace=True)

    print(df)
    return df