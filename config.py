import os
from pathlib import Path

#Files
DATA_DIR = "/Users/judesack/THESIS_CODE/CLEANED_DATA/COMBINED PROBES"
POS_FILES_PATH = "/Users/judesack/THESIS_CODE/GSTH/notebooks/POS_files/*subject*.pos"
OUTPUT_DIR = "/Users/judesack/THESIS_CODE/GSTH/notebooks/scattering_coefficients/MLP_data_new"
fnirs_data = "/Users/judesack/THESIS_CODE/GSTH/notebooks/baseline_data/combined_fnirs_data.csv"
scattering_data = "/Users/judesack/THESIS_CODE/GSTH/notebooks/scattering_coefficients/MLP_data_new/combined_data.csv"
results_dir = 'baseline_classification_results'
output_dir = "baseline_data"
visualization_dir = 'latent_visualization_results'
extended_results_dir = 'extended_latent_results'
attention_results_dir = 'attention_results'
weights_viz_dir = 'weight_visualization_comparison_results'

# Constants - (play around with threshold & t_value)
THRESHOLD = 0.33  # ask Smita about this. changed from 0.6.
T_VALUE = 200
GRAPHS_PER_ROW = 3
GRAPHS_PER_COL = 3
MARKER_SIZE = 50
ALPHA = 0.7

# Based on Tachibana's experimental paradigm 
TASK_SEGMENTS = [
    (0, 250, 'Pre'),
    (250, 650, 'Rest 1'),
    (650, 1050, 'Sham'),
    (1050, 1450, 'Rest 2'),
    (1450, 1850, 'Improv 1'),
    (1850, 2250, 'Rest 3'),
    (2250, 2650, 'Scale 1'),
    (2650, 3050, 'Rest 4'),
    (3050, 3450, 'Improv 2'),
    (3450, 3850, 'Rest 5'),
    (3850, 4250, 'Scale 2'),
    (4250, 4650, 'Rest 6'),
    (4650, 5050, 'Improv 3'),
    (5050, 5450, 'Rest 7'),
    (5450, 5850, 'Scale 3'),
    (5850, 6250, 'Rest 8'),
    (6250, 6650, 'Improv 4'),
    (6650, 7050, 'Rest 9'),
    (7050, 7450, 'Scale 4'),
    (7450, 7850, 'Rest 10')
]

expected_shape = (7850, 48)

holder1_pairs = [
    (1, 2), (2, 3), (3, 4), (1, 5), (2, 6), (3, 7), (4, 8),
    (5, 6), (6, 7), (7, 8), (5, 9), (6, 10), (7, 11), (8, 12),
    (9, 10), (10, 11), (11, 12), (9, 13), (10, 14), (11, 15), (12, 16),
    (13, 14), (14, 15), (15, 16)
]

holder2_pairs = [
    (17, 18), (18, 19), (19, 20), (17, 21), (18, 22), (19, 23), (20, 24),
    (21, 22), (22, 23), (23, 24), (21, 25), (22, 26), (23, 27), (24, 28),
    (25, 26), (26, 27), (27, 28), (25, 29), (26, 30), (27, 31), (28, 32),
    (29, 30), (30, 31), (31, 32)
]