import tkinter as tk
from tkinter import ttk
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import preprocess

# File paths
input_file_path = '1355LG.csv'


import csv
import numpy as np
import geopandas as gpd
from shapely.geometry import LineString

def create_simple_map():
    # Specify the column numbers to be read from the CSV file
    columns_to_read = [0, 14, 15, 16, 17]

    # Specify the column names for better readability
    column_names = ['Type', 'Start Easting', 'Start Northing', 'End Easting', 'End Northing']

    # Initialize an empty list to store the valid rows
    rows = []

    # Read the CSV file
    with open(input_file_path, 'r') as file:
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
                    rows.append([row[0], start_easting, start_northing, end_easting, end_northing])
                except ValueError:
                    pass

    # Create a DataFrame from the list of valid rows
    df = pd.DataFrame(rows, columns=column_names)

    # Create LineString geometries from start and end coordinates
    lines = [LineString([(row['Start Easting'], row['Start Northing']), (row['End Easting'], row['End Northing'])])
             for _, row in df.iterrows()]

    # Create a GeoDataFrame from the lines
    gdf = gpd.GeoDataFrame(df, geometry=lines)

    return gdf


def create_simple_map_command(canvas, toolbar, ax):
    # Generate the simple map
    gdf = create_simple_map()

    # Clear the existing plot
    ax.clear()

    # Check if there is data to plot
    if not gdf.empty:
        # Plot the GeoDataFrame as lines
        gdf.plot(ax=ax, linestyle='-', color='blue')

    else:
        # Display text when there is no data to plot
        ax.text(0.5, 0.5, 'No data to plot', horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12)

    # Remove axes and axis labels
    #ax.axis('off')

    # Display the plot on the canvas
    canvas.draw()

    # Update the toolbar
    toolbar.update()


# Create the main window
window = tk.Tk()
window.title("Street Gazetteer Map")

# Create the right-side pane for output display
output_frame = ttk.Frame(window)
output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a new figure and axis object
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

# Create a canvas for displaying the plot
canvas = FigureCanvasTkAgg(fig, master=output_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create the toolbar
toolbar = NavigationToolbar2Tk(canvas, output_frame)
toolbar.update()
toolbar.pack()

# Create the left-side menu
menu_frame = ttk.Frame(window)
menu_frame.pack(side=tk.LEFT, fill=tk.Y)

label = ttk.Label(menu_frame, text="Menu")
label.pack()

# Add menu buttons
button_process_LG = ttk.Button(menu_frame, text="Process Level 3 File")
button_process_LG.pack(pady=10)
# Bind the button click event to the map creation function
button_process_LG.configure(command=lambda: preprocess.preprocess_csv(input_file_path))

button_create_simple_map = ttk.Button(menu_frame, text="Display Type 11 Map")
button_create_simple_map.pack(pady=10)
# Bind the button click event to the map creation function
button_create_simple_map.configure(command=lambda: create_simple_map_command(canvas, toolbar, ax))

button_street_search = ttk.Button(menu_frame, text="Street Level Search")
button_street_search.pack(pady=10)
# Bind the button click event to the map creation function
#button_street_search.configure(command=lambda: create_simple_map_command(canvas, toolbar, ax))

# Initially display text instead of a plot
ax.text(0.5, 0.5, 'Click "Display Type 11 Map" to generate a simple plot', horizontalalignment='center',
        verticalalignment='center', transform=ax.transAxes, fontsize=12)
# Remove axes and axis labels
ax.axis('off')

# Display the initial text on the canvas
canvas.draw()

# Start the Tkinter event loop
window.mainloop()
