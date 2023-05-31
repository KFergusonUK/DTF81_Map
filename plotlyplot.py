def plotly_plot():
  
  import pandas as pd
  import plotly.graph_objects as go
  
  # Read the CSV file into a DataFrame
  df = pd.read_csv('LG_Processed.csv')
  
  # Create a list to store the LineString coordinates
  coordinates = []
  
  # Extract the LineString coordinates from the 'geometry' column
  for geometry in df['geometry']:
      coords = geometry.replace('LINESTRING (', '').replace(')', '').split(', ')
      coords = [coord.split(' ') for coord in coords]
      coords = [[float(coord[0]), float(coord[1])] for coord in coords]
      coordinates.append(coords)
  
  # Create a list to store the USRNs
  usrns = df.iloc[:, 0]
  
  # Create a trace for each LineString
  traces = []
  for i in range(len(coordinates)):
      x, y = zip(*coordinates[i])
      trace = go.Scatter(x=x, y=y, mode='lines', name=f'USRN: {usrns[i]}')
      traces.append(trace)
  
  # Create the figure and set the layout
  fig = go.Figure(data=traces, layout=go.Layout(title='Map Plot', showlegend=True))
  
  # Save the plot as an HTML file
  output_path = 'map.html'
  fig.write_html(output_path)
  
  # Print the output path for manual opening
  print(f"Plot saved as '{output_path}'")
  
