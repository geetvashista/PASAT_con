import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# File Path
Alpha_path = Path('C:/Users/Admin/Desktop/data/Alpha/')
Theta_path = Path('C:/Users/Admin/Desktop/data/Theta/')

# Getting file names
Alpha_files = sorted(Alpha_path.glob('for_num*.xlsx'))
Theta_files = sorted(Theta_path.glob('Theta_for_num*.xlsx'))

# dataframe storage
Alpha_dfs = []
Theta_dfs = []

# Load Alpha files into Alpha_dfs
for file in Alpha_files:
    df = pd.read_excel(file, index_col=0)
    Alpha_dfs.append(df)

# Load Theta files into Theta_dfs
for file in Theta_files:
    df = pd.read_excel(file, index_col=0)
    Theta_dfs.append(df)

# Defining brain regions and their respective colors
regions = {
    'frontal': ['FP1', 'FP2', 'AF7', 'AF8', 'AF3', 'AF4', 'F7', 'F8', 'F5', 'F6', 'F3', 'F4', 'F1', 'F2', 'FZ', 'FPZ'],
    'central': ['FC5', 'FC6', 'FC3', 'FC4', 'FC1', 'FC2', 'FCZ', 'C5', 'C6', 'C3', 'C4', 'C1', 'C2', 'CZ'],
    'parietal': ['CP5', 'CP6', 'CP3', 'CP4', 'CP1', 'CP2', 'CPZ', 'P7', 'P8', 'P5', 'P6', 'P3', 'P4', 'P1', 'P2', 'PZ'],
    'occipital': ['PO7', 'PO8', 'PO3', 'PO4', 'POZ', 'O1', 'O2', 'OZ', 'IZ'],
    'temporal': ['FT7', 'FT8', 'FT9', 'FT10', 'T7', 'T8', 'T9', 'T10', 'TP7', 'TP8', 'TP9', 'TP10', 'M1', 'M2']
}

color_map = {
    'frontal': '#FF0000',   # Red
    'central': '#228B22',   # Green
    'parietal': '#0000FF',  # Blue
    'occipital': '#800080', # Purple
    'temporal': '#FFA500'   # Orange
}

# Put Electrode colours into one place
electrode_color_map = {electrode: color for region, electrodes in regions.items() for electrode in electrodes for color in [color_map[region]]}

# Function to plot data
def plot_frequency_band(frequency_name, dataframes, color_map):
    for i, df in enumerate(dataframes):
        if df.empty:
            print(f"Skipping empty {frequency_name} DataFrame {i + 1}")
            continue

        plt.figure(figsize=(10, 6))

        # Plot each row in the DataFrame
        for row_label in df.index:
            color = electrode_color_map.get(row_label.upper(), 'black')
            plt.plot(df.columns, df.loc[row_label], label=row_label, color=color)

        # Customize the graph
        plt.title(f"{frequency_name} - #{i + 1}")
        plt.xlabel('Rotation')
        plt.ylabel('PLI Value')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.ylim(-0.05, .05)
        plt.tight_layout()

    plt.show() # Showing all plots

# looping through both Alpha and Theta frequency bands
for frequency_name, dataframes in [('Alpha', Alpha_dfs), ('Theta', Theta_dfs)]:
    plot_frequency_band(frequency_name, dataframes, color_map)
