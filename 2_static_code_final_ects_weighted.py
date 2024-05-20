# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:05:33 2024

@author: Tobia
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:03:49 2024

@author: Tobia
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Set path to working directory, use relative path
csv_path = "Core_Topics_and_Lectures_weighted.csv"


# Load the CSV data with a semicolon delimiter
#csv_path = r"C:\Users\Tobia\OneDrive\Desktop\Dokumente\1.Universität\1.Master UniBe\HS_2023\Network science\Core_Topics_and_Lectures_weighted.csv"
df = pd.read_csv(csv_path, delimiter=';')

# Create a networkx graph
G = nx.Graph()

# Define specific colors for each core topic
topic_colors = {
    'Hydrology': '#3498db',  # Blue
    'Spatial Planning': '#e74c3c',  # Red
    'Business Administration': '#2ecc71',  # Green
    'Natural Hazards': '#f39c12',  # Orange
    'Methods': '#9b59b6',  # Purple
}

# Add nodes for each core topic and lecture
for topic, ects_col in zip(df.columns[::2], df.columns[1::2]):
    lectures = df[topic].dropna()
    ects_values = df[ects_col].dropna()
    for lecture, ects in zip(lectures, ects_values):
        ects = float(str(ects).replace(',', '.'))  # Convert ECTS to float
        if lecture not in G:
            G.add_node(lecture, size=200 + ects * 40, color='lightgrey', label=lecture)  # Adjust size based on ECTS
        G.add_edge(topic, lecture, color=topic_colors.get(topic, '#34495e'))

# Add nodes for each core topic separately to set their properties
for topic in df.columns[::2]:
    G.add_node(topic, size=1000, color=topic_colors.get(topic, '#34495e'), label=topic)

# Add the main topic 'Hydro Power' and connect it to all core topics
main_topic = "Hydro Power"
G.add_node(main_topic, size=1500, color='#34495e', label=main_topic)
for topic in df.columns[::2]:
    G.add_edge(main_topic, topic, color='#34495e')

# Define node positions using spring layout with specific seeds for consistency
pos = nx.spring_layout(G, seed=42, k=0.5)  # Increasing k increases spacing

# Drawing the graph
plt.figure(figsize=(14, 10))
edges = G.edges(data=True)
for start, end, data in edges:
    nx.draw_networkx_edges(G, pos, edgelist=[(start, end)], alpha=0.5, edge_color=data['color'])

for node in G.nodes(data=True):
    nx.draw_networkx_nodes(G, pos, nodelist=[node[0]], node_color=node[1]['color'], node_size=node[1]['size'])

# Draw labels
labels = nx.get_node_attributes(G, 'label')
ax = plt.gca()

# Adjust labels to avoid overlap
text_items = []
label_positions = {}
for key, (x, y) in pos.items():
    if key == main_topic:
        text = ax.text(x, y, labels[key], fontsize=13, fontweight='bold')
    elif key in topic_colors.keys():
        text = ax.text(x, y, labels[key], fontsize=10, fontweight='bold')
    else:
        text = ax.text(x, y, labels[key], fontsize=7)
    text_items.append(text)
    label_positions[key] = text

adjust_text(text_items, expand_text=(1.2, 1.3), expand_points=(1.2, 1.3), force_text=(0.5, 1.0))

# Draw short edges from the center of the nodes to the labels
for key, (x, y) in pos.items():
    label = label_positions[key]
    label_x, label_y = label.get_position()
    line = plt.Line2D([x, label_x], [y, label_y], color='grey', alpha=0.5, linewidth=0.8)
    ax.add_line(line)

plt.title('Network Visualization of Core Topics and Lectures surrounding Hydro Power', size=15)
plt.axis('off')  # Turn off the axis

# Save the plot with a high resolution
output_path = r"C:\Users\Tobia\OneDrive\Desktop\Dokumente\1.Universität\1.Master UniBe\HS_2023\Network science\GitHub_upload\static_plot_weighted_final.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
