# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:22:10 2024

@author: Tobia
"""
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Set path to working directory, use relative path
csv_path = "Core_Topics_and_Lectures_weighted.csv"

# Load the CSV data with a semicolon delimiter
#csv_path = r"C:\Users\Tobia\OneDrive\Desktop\Dokumente\1.Universität\1.Master UniBe\HS_2023\Network science\Core_Topics_and_Lectures_weighted.csv"
df = pd.read_csv(csv_path, delimiter=';')

# Create a NetworkX graph
G = nx.Graph()

# Define specific colors for each core topic
topic_colors = {
    'Hydrology': '#3498db',  # Blue
    'Spatial Planning': '#e74c3c',  # Red
    'Business Administration': '#2ecc71',  # Green
    'Natural Hazards': '#f39c12',  # Orange
    'Methods': '#9b59b6',  # Purple
    'Hydro Power': '#34495e'   # Dark blue/grey
}

# Initialize a dictionary to store total ECTS for each core topic
core_topic_ects = {topic: 0 for topic in df.columns[::2]}

# Add nodes for each core topic and lecture
for topic, ects_col in zip(df.columns[::2], df.columns[1::2]):
    G.add_node(topic, size=30, color=topic_colors.get(topic, 'grey'), 
               title=f"{topic}\nTotal ECTS: 0\nConnections: 0", font={'size': 18, 'color': topic_colors.get(topic, 'grey'), 'vadjust': -10, 'bold': True})
    lectures = df[topic].dropna()
    ects_values = df[ects_col].dropna()
    for lecture, ects in zip(lectures, ects_values):
        ects = float(str(ects).replace(',', '.'))  # Convert ECTS to float if necessary
        if lecture not in G:
            G.add_node(lecture, size=15 + ects * 2, color='lightgrey', 
                       title=f"{lecture}\nECTS: {ects}\nConnections: 1\nCore Topic: {topic}", font={'size': 12, 'color': 'black', 'vadjust': 10})
        else:
            # Update the lecture node title with the new connection
            connections = G.degree(lecture) + 1
            title = f"{lecture}\nECTS: {ects}\nConnections: {connections}\nCore Topic: {topic}"
            G.nodes[lecture]['title'] = title
        G.add_edge(topic, lecture)
        core_topic_ects[topic] += ects  # Accumulate the ECTS for the core topic

# Adjust the size and title of core topic nodes based on the total ECTS and number of connections
max_ects = max(core_topic_ects.values())  # Find the maximum total ECTS for scaling
for topic in df.columns[::2]:
    connections = G.degree(topic)
    total_ects = core_topic_ects[topic]
    scaled_size = (total_ects / max_ects) * 50 + 30  # Scale size down but keep relative differences
    G.nodes[topic]['size'] = scaled_size + connections * 2  # Adjust size based on ECTS and connections
    G.nodes[topic]['title'] = f"{topic}\nTotal ECTS: {total_ects}\nConnections: {connections}"

# Add the main topic 'Hydro Power' and connect it to all core topics
G.add_node("Hydro Power", size=50, color=topic_colors['Hydro Power'], 
           title="Hydro Power", font={'size': 24, 'color': topic_colors['Hydro Power'], 'vadjust': -10, 'bold': True})
for topic in df.columns[::2]:
    G.add_edge("Hydro Power", topic)

# Initialize PyVis network visualization
net = Network(notebook=True, width="1000px", height="700px", bgcolor='#222222', font_color='white')

# Set the physics options to increase edge length and distance between nodes
net.set_options('''
{
  "nodes": {
    "font": {
      "size": 14,
      "face": "Helvetica"
    }
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "smooth": false
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -8000,
      "centralGravity": 0.05,
      "springLength": 400,
      "springConstant": 0.005,
      "damping": 0.09 
    },
    "maxVelocity": 50,
    "minVelocity": 0.1,
    "timestep": 0.5
  }
}
''')

# Add nodes and edges to the PyVis network, making sure lectures are in front of core topics
for node, attrs in G.nodes(data=True):
    net.add_node(node, **attrs)
for start, end, attrs in G.edges(data=True):
    net.add_edge(start, end, **attrs)

# Generate the visualization
output_file = r"C:\Users\Tobia\OneDrive\Desktop\Dokumente\1.Universität\1.Master UniBe\HS_2023\Network science\GitHub_upload\interactive_plot_final.html"
net.show(output_file)
