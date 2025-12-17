"""
Configuration file for AttriMIL training on video dataset
Adapted for 3-class polyp classification (Normal, Adenoma, Malignant)
"""

# ========================
# DATA PATHS
# ========================
# Path to CSV file containing video_id, category, and label columns
csv_path = '/Users/vietha/Documents/GitHub/AttriMIL/video_data/video_dataset.csv'

# Directory containing extracted video features (.pt files)
data_dir = '/Users/vietha/Documents/GitHub/AttriMIL/video_features/'

# Directory containing train/val/test split CSV files (splits_0.csv)
split_path = '/Users/vietha/Documents/GitHub/AttriMIL/video_data/splits/'

# Directory to save model weights and logs
save_dir = './save_weights/video_attrimil/'

# ========================
# DATASET SETTINGS
# ========================
# Label dictionary: map category names to integer indices
# Normal: 0, Adenoma: 1, Malignant: 2
label_dict = {'Normal': 0, 'Adenoma': 1, 'Malignant': 2}

# Number of classes in dataset
n_classes = 3

# Random seed for reproducibility
seed = 1

# ========================
# MODEL SETTINGS
# ========================
# Feature dimension (ResNet50 features)
feature_dim = 2048

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
early_stopping = True

# Early stopping patience (number of epochs without improvement)
early_stopping_patience = 20

# Minimum epochs before early stopping can trigger
min_epochs_before_early_stop = 50

# ========================
# LOSS WEIGHTS
# ========================
# Weight for temporal constraint loss (adapted from spatial constraint)
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
num_folds = 1

# Specific fold to run (set to None to run all folds)
run_specific_fold = None  # or set to 0 for a specific fold
