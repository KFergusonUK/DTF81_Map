def gui():

  import tkinter as tk
  from tkinter import ttk
  import pandas as pd
  import geopandas as gpd
  from shapely.geometry import LineString
  import matplotlib.pyplot as plt
  from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
  from matplotlib.figure import Figure
  import numpy as np
  
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
  button_create_simple_map.configure(command=lambda: create_simple_map_command(canvas, toolbar, ax))
  
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