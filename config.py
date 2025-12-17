"""
Configuration file for AttriMIL training
Modify the paths and parameters below to match your dataset and experiment settings
"""

# ========================
# DATA PATHS
# ========================
# Path to CSV file containing slide_id and label columns
csv_path = '/Users/vietha/Documents/GitHub/AttriMIL/camelyon16_attrimil/camelyon16_total.csv'

# Directory containing extracted features (.h5 and .pt files)
data_dir = '/Users/vietha/Documents/GitHub/AttriMIL/camelyon16_attrimil/'

# Directory containing train/val/test split CSV files (splits_0.csv, splits_1.csv, etc.)
split_path = '/Users/vietha/Documents/GitHub/AttriMIL/camelyon16_attrimil/splits/'

# Directory to save model weights and logs
save_dir = './save_weights/camelyon16_attrimil_phikon/'

# ========================
# DATASET SETTINGS
# ========================
# Label dictionary: map label names to integer indices
# Example for binary classification: {'normal_tissue': 0, 'tumor_tissue': 1}
# Example for multi-class: {'class_0': 0, 'class_1': 1, 'class_2': 2}
label_dict = {'normal_tissue': 0, 'tumor_tissue': 1}

# Number of classes in your dataset
n_classes = 2

# Random seed for reproducibility
seed = 1

# ========================
# MODEL SETTINGS
# ========================
# Feature dimension (should match your extracted features)
# 512 for ResNet18, 1024 for ResNet50, 2048 for ResNet101, 768 for Phikon
feature_dim = 768

# ========================
# TRAINING SETTINGS
# ========================
# Maximum number of epochs
max_epoch = 150

# Learning rate
learning_rate = 2e-4

# SGD momentum
momentum = 0.9

# Weight decay (L2 regularization)
weight_decay = 1e-5

# Early stopping (set to True to enable)
early_stopping = False

# Early stopping patience (number of epochs without improvement)
early_stopping_patience = 20

# Minimum epochs before early stopping can trigger
min_epochs_before_early_stop = 50

# ========================
# LOSS WEIGHTS
# ========================
# Weight for spatial constraint loss
spatial_loss_weight = 1.0

# Weight for ranking constraint loss
ranking_loss_weight = 5.0

# ========================
# LOGGING SETTINGS
# ========================
# Enable TensorBoard logging
writer_flag = True

# Save checkpoint every N epochs
save_checkpoint_freq = 10

# Print training stats every N batches
print_freq = 20

# ========================
# CROSS-VALIDATION
# ========================
# Number of folds to run (set to 1 for single train/val/test split)
# Set to 5 if you have splits_0.csv through splits_4.csv
num_folds = 1

# Specific fold to run (set to None to run all folds)
# Useful for parallel training on different GPUs
run_specific_fold = None  # or set to 0 for a specific fold
