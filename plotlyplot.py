def plotly_plot():
  
  import pandas as pd
  import plotly.graph_objects as go
  import plotly.offline as offline
  
  # Read the data from CSV file
  df = pd.read_csv("LG_Processed.csv")
  
  # Extract coordinates and create LineString objects
  lines = []
  for index, row in df.iterrows():
      coords = row['geometry'].replace('LINESTRING (', '').replace(')', '').split(', ')
      line = []
      for c in coords:
          if ' ' in c:
              line.append([float(coord) for coord in c.split()])
          else:
              line[-1].extend([float(coord) for coord in c.split()])
      lines.append(line)
  
  # Create Plotly figure
  fig = go.Figure()
  for line in lines:
      fig.add_trace(go.Scattermapbox(
          lat=[point[1] for point in line],
          lon=[point[0] for point in line],
          mode='lines',
          line=dict(width=3),
          hovertemplate='USRN: %{text}',
          text=[f"USRN: {row[0]}" for row in df.itertuples()],
          hoverinfo='text',
      ))
  
  # Find the minimum and maximum coordinates for setting the map bounds
  all_coords = [coord for line in lines for coord in line]
  min_lon = min(coord[0] for coord in all_coords)
  max_lon = max(coord[0] for coord in all_coords)
  min_lat = min(coord[1] for coord in all_coords)
  max_lat = max(coord[1] for coord in all_coords)
  
  # Set layout properties and zoom in on the relevant area
  fig.update_layout(
      mapbox=dict(
          center=dict(lat=(min_lat + max_lat) / 2, lon=(min_lon + max_lon) / 2),
          zoom=10
      ),
      showlegend=False
  )
  
  # Save the figure as a standalone HTML file
  offline.plot(fig, filename='map.html', auto_open=False)
  
  # Open the HTML file in a separate browser tab
  import webbrowser
  webbrowser.open('map.html')
  