import tkinter as tk
from tkinter import ttk
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import csv
from shapely.geometry import Point


import preprocess
import preprocess_file


# File paths
input_file_path = '1355LG.csv'
uk_map_image_path = 'Miniscale_UK_resize.tif'



#CREATE SIMPLE MAP STARTS HERE:

def create_simple_map():
    # Generate the Type 11 map
    gdf_type_11 = preprocess.preprocess_type_11(input_file_path)

    # Create LineString geometries from start and end coordinates
    lines = [LineString([(row['Start Easting'], row['Start Northing']), (row['End Easting'], row['End Northing'])])
             for _, row in gdf_type_11.iterrows()]

    # Create a GeoDataFrame from the lines
    gdf = gpd.GeoDataFrame(gdf_type_11, geometry=lines)

    #print(gdf)

    return gdf


def create_single_street_map():
    # Increase the display options
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.width', None)  # Disable column width wrapping

    # Generate the single street map
    gdf_ss = preprocess.preprocess_single_street(input_file_path, selected_street_usrn)

    # Create LineString geometries from start, midpoint, and end coordinates
    lines = []
    for _, row in gdf_ss.iterrows():
        points = [(row['Start Easting'], row['Start Northing'])]  # Start point
        mid_easting_columns = [col for col in row.index if col.startswith('Mid Easting')]
        mid_northing_columns = [col for col in row.index if col.startswith('Mid Northing')]

        # Create a list of (midpoint, distance) tuples
        midpoints = []
        for mid_easting_col, mid_northing_col in zip(mid_easting_columns, mid_northing_columns):
            mid_easting_list = row[mid_easting_col]
            mid_northing_list = row[mid_northing_col]
            for mid_easting, mid_northing in zip(mid_easting_list, mid_northing_list):
                if not pd.isnull(mid_easting) and not pd.isnull(mid_northing):
                    midpoint = Point(float(mid_easting), float(mid_northing))
                    distance = midpoint.distance(Point(row['Start Easting'], row['Start Northing']))
                    midpoints.append((midpoint, distance))

        # Sort the midpoints based on their distances
        sorted_midpoints = sorted(midpoints, key=lambda x: x[1])

        # Add the sorted midpoints as points in the LineString
        for midpoint, _ in sorted_midpoints:
            points.append((midpoint.x, midpoint.y))  # Midpoint

        points.append((row['End Easting'], row['End Northing']))  # End point
        lines.append(LineString(points))

    # Create a GeoDataFrame from the lines
    gdf = gpd.GeoDataFrame(geometry=lines)
    print(lines)
    print("\n")
    print(gdf)

    return gdf









def create_simple_map_command(canvas, toolbar, ax, click_source):
    clear_output_frame()

    # Increase the display options
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.width', None)  # Disable column width wrapping
    
    # Create a new figure and axis object
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Generate the map dependant on source.
    if click_source == "simple":
      gdf = create_simple_map()
    elif click_source == "single":
      gdf = create_single_street_map()

    # Clear the existing plot
    ax.clear()

    # Check if there is data to plot
    if not gdf.empty:
        # Read the UK map image
        uk_map_image = plt.imread(uk_map_image_path)

        # Set the extent of the UK map image based on the desired coordinates
        extent = [0, 700000, 0, 1300000]

        # Plot the UK map as the background
        ax.imshow(uk_map_image, extent=extent, aspect='auto')

        # Plot the GeoDataFrame as lines
        gdf.plot(ax=ax, linestyle='-', color='blue')

        # Get the bounds of the lines data
        lines_bounds = gdf.total_bounds

        # Calculate the x and y center coordinates of the lines data
        center_x = (lines_bounds[0] + lines_bounds[2]) / 2
        center_y = (lines_bounds[1] + lines_bounds[3]) / 2

        # Calculate the width and height of the lines data
        width = lines_bounds[2] - lines_bounds[0]
        height = lines_bounds[3] - lines_bounds[1]

        # Set the new extent based on the lines data bounds
        new_extent = [center_x - width / 2, center_x + width / 2, center_y - height / 2, center_y + height / 2]

        # Set the aspect ratio to 'equal' to retain the original size
        ax.set_aspect('equal')

        # Set the new extent for the plot
        ax.set_xlim(new_extent[0], new_extent[1])
        ax.set_ylim(new_extent[2], new_extent[3])

    else:
        # Display text when there is no data to plot
        ax.text(0.5, 0.5, 'No data to plot', horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12)

    # Remove axes and axis labels
    ax.axis('off')

    # Create a canvas for displaying the plot
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Create the toolbar
    toolbar = NavigationToolbar2Tk(canvas, output_frame)
    toolbar.update()
    toolbar.pack()

    # Display the plot on the canvas
    canvas.draw()



#CLEAR GUI MAIN WINDOW STARTS HERE:

def clear_output_frame():
    for widget in output_frame.winfo_children():
        widget.destroy()



#SINGLE STREET SEARCH STARTS HERE:

def display_street_search():
    clear_output_frame()

    # Create the street search frame
    street_search_frame = ttk.Frame(output_frame)
    street_search_frame.pack(fill=tk.BOTH, expand=True)

    # Create the search entry
    search_entry = ttk.Entry(street_search_frame)
    search_entry.pack(pady=10)

    def perform_street_search():
      search_term = search_entry.get()
      df_type_15 = preprocess.preprocess_type_15(input_file_path)
      search_results = df_type_15[df_type_15['Street'].str.contains(search_term, case=False)]
  
      # Clear the existing search results frame
      for widget in search_results_frame.winfo_children():
          widget.destroy()
  
      if not search_results.empty:
          # Create a scrollable frame for displaying search results
          scrollable_frame = ttk.Frame(search_results_frame)
          scrollable_frame.pack(fill=tk.BOTH, expand=True)
  
          # Create a canvas inside the scrollable frame
          canvas = tk.Canvas(scrollable_frame)
          canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
  
          # Add a scrollbar to the canvas
          scrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=canvas.yview)
          scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
  
          # Configure the canvas to use the scrollbar
          canvas.configure(yscrollcommand=scrollbar.set)
  
          # Create a frame inside the canvas for the search results
          results_frame = ttk.Frame(canvas)
          canvas.create_window((0, 0), window=results_frame, anchor=tk.N)
  
          def select_street(usrn, click_source):
              global selected_street_usrn
              selected_street_usrn = usrn
              print(f"Selected street USRN: {selected_street_usrn}, Click Source: {click_source}")
              # Call create_simple_map_command with the desired arguments
              create_simple_map_command(canvas, toolbar, ax, click_source)

          # Loop through the search results and display the full row
          for idx, result in search_results.iterrows():
              result_label = ttk.Label(results_frame, text=f" {result['Street']}, {result['Town']}, USRN: {result['USRN']}")
              result_label.pack(pady=5)
  
              # Bind the click event to the select_street function
              result_label.bind('<Button-1>', lambda event, usrn=result['USRN']: select_street(usrn, click_source="single"))
  
          # Configure the canvas scrolling
          canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
  
      else:
          no_results_label = ttk.Label(search_results_frame, text="No results found")
          no_results_label.pack()
  
  
    # Create the search button
    search_button = ttk.Button(street_search_frame, text="Search", command=perform_street_search)
    search_button.pack(pady=10)

    # Create the search results frame
    search_results_frame = ttk.Frame(output_frame)
    search_results_frame.pack(fill=tk.BOTH, expand=True)



#MAIN GUI STARTS HERE:

# Create the main window
window = tk.Tk()
window.title("Street Gazetteer Map")

# Create the right-side pane for output display
output_frame = ttk.Frame(window)
output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
output_frame.pack_propagate(False)


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
button_process_LG.configure(command=lambda: preprocess_file.preprocess_csv(input_file_path))

button_create_simple_map = ttk.Button(menu_frame, text="Display Type 11 Map")
button_create_simple_map.pack(pady=10)
# Bind the button click event to the map creation function
button_create_simple_map.configure(command=lambda: create_simple_map_command(canvas, toolbar, ax, click_source="simple"))

button_street_search = ttk.Button(menu_frame, text="Street Level Search")
button_street_search.pack(pady=10)
# Bind the button click event to the street search function
button_street_search.configure(command=display_street_search)

# Initially display text instead of a plot
ax.text(0.5, 0.5, 'Click "Display Type 11 Map" to generate a simple plot', horizontalalignment='center',
        verticalalignment='center', transform=ax.transAxes, fontsize=12)
# Remove axes and axis labels
ax.axis('off')

# Display the initial text on the canvas
canvas.draw()

# Start the Tkinter event loop
window.geometry("640x480")
window.mainloop()