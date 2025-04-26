import numpy as np
import os
import glob
import configparser
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scattering import gaussian_kernel, construct_adjacency_matrix
from config import POS_FILES_PATH, THRESHOLD, GRAPHS_PER_ROW, GRAPHS_PER_COL, holder1_pairs, holder2_pairs

def load_coordinates():
    subject_probe_coords = []
    subject_channel_coords = []

    for file_path in glob.glob(POS_FILES_PATH):
        config = configparser.ConfigParser()
        config.read(file_path)
        subject_id = os.path.basename(file_path).split("_")[0]
        probe_coordinates = np.zeros((32, 3))
        for i in range(1, 17):
            probe_key = f"Probe1-ch{i}"
            if probe_key in config:
                probe_coordinates[i - 1] = [
                    float(config[probe_key]["X"]),
                    float(config[probe_key]["Y"]),
                    float(config[probe_key]["Z"])
                ]
            probe_key = f"Probe2-ch{i}"
            if probe_key in config:
                probe_coordinates[i + 15] = [
                    float(config[probe_key]["X"]),
                    float(config[probe_key]["Y"]),
                    float(config[probe_key]["Z"])
                ]
        
        #Channel coordiantes are midpoints between probes
        channel_coordinates = np.zeros((48, 3))
        for idx, (p1, p2) in enumerate(holder1_pairs):
            channel_coordinates[idx] = (probe_coordinates[p1 - 1] + probe_coordinates[p2 - 1]) / 2
        for idx, (p1, p2) in enumerate(holder2_pairs):
            channel_coordinates[idx + 24] = (probe_coordinates[p1 - 1] + probe_coordinates[p2 - 1]) / 2
        subject_probe_coords.append((subject_id, probe_coordinates))
        subject_channel_coords.append((subject_id, channel_coordinates))
    print(f"\nProcessed {len(subject_probe_coords)} subjects")
    print(f"Probe matrix shape: {subject_probe_coords[0][1].shape}")
    print(f"Channel matrix shape: {subject_channel_coords[0][1].shape}")
    return subject_probe_coords, subject_channel_coords

#Fix the outliers for 15052902
def fix_outlier_coordinates(subject_channel_coords, problem_subject="15052902", problem_nodes=[0, 3]):
    problem_subject_idx = None
    for idx, (subject_id, _) in enumerate(subject_channel_coords):
        if subject_id == problem_subject:
            problem_subject_idx = idx
            break
    if problem_subject_idx is None:
        print(f"Can't find subject {problem_subject}.")
        return subject_channel_coords
    
    other_coords = []
    for idx, (subject_id, coords) in enumerate(subject_channel_coords):
        if subject_id != problem_subject:
            for node in problem_nodes:
                if node < coords.shape[0]:
                    other_coords.append(coords[node])
    if not other_coords:
        print("No other subjects to compare with.")
        return subject_channel_coords
    
    # Use median of others' nodes for 1 & 3
    other_coords = np.array(other_coords)
    median_coords = np.median(other_coords, axis=0)
    subject_id, coords = subject_channel_coords[problem_subject_idx]
    for node in problem_nodes:
        if node < coords.shape[0]:
            print(f"Replacing coords for Subject {subject_id}, Node {node}:")
            print(f"  Before: {coords[node]}")
            coords[node] = median_coords
            print(f"  After: {coords[node]}")
    subject_channel_coords[problem_subject_idx] = (subject_id, coords)
    return subject_channel_coords

def plot_3d_adj_matrix(subject_channel_coords, threshold=THRESHOLD):
    n_subjects = len(subject_channel_coords)
    n_rows = (n_subjects + GRAPHS_PER_ROW - 1) // GRAPHS_PER_ROW
    n_cols = min(n_subjects, GRAPHS_PER_COL)
    fig = plt.figure(figsize=(5 * n_cols, 5 * n_rows))
    
    for idx, (subject, coords) in enumerate(subject_channel_coords):
        adj_matrix = construct_adjacency_matrix(coords, threshold)
        ax = fig.add_subplot(n_rows, n_cols, idx + 1, projection='3d')
        x_coords = coords[:, 0]
        y_coords = coords[:, 1]
        z_coords = coords[:, 2]
        
        #Plot nodes
        ax.scatter(x_coords, y_coords, z_coords, c='skyblue', s=200, edgecolor='black', alpha=0.8)
        for i in range(len(coords)):
            ax.text(x_coords[i], y_coords[i], z_coords[i], str(i), 
                   fontsize=8, color='black', ha='center', va='center')
            
        # Plot edges - could be wrong, check w/ Dhanajay
        for i in range(len(adj_matrix)):
            for j in range(i+1, len(adj_matrix)):
                if adj_matrix[i, j] > 0:
                    ax.plot([x_coords[i], x_coords[j]],
                            [y_coords[i], y_coords[j]],
                            [z_coords[i], z_coords[j]], 
                            'k-', alpha=0.3, linewidth=adj_matrix[i, j] * 3)
      
        ax.set_title(f"Subject {subject} - 3D Adjacency Matrix")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        max_range = np.max([x_coords.max() - x_coords.min(),
                           y_coords.max() - y_coords.min(),
                           z_coords.max() - z_coords.min()]) / 2.0
        mid_x = (x_coords.max() + x_coords.min()) / 2.0
        mid_y = (y_coords.max() + y_coords.min()) / 2.0
        mid_z = (z_coords.max() + z_coords.min()) / 2.0
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()