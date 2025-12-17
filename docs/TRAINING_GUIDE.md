# AttriMIL Training Guide

## Quick Start

### Step 1: Configure Your Paths

Edit `config.py` and update the following paths to match your dataset:

```python
# Path to CSV file containing slide_id and label columns
csv_path = '/path/to/your/dataset.csv'

# Directory containing extracted features (.h5 and .pt files)
data_dir = '/path/to/your/features/'

# Directory containing train/val/test split CSV files
split_path = '/path/to/your/splits/'

# Directory to save model weights and logs
save_dir = './save_weights/your_experiment_name/'
```

### Step 2: Set Dataset Parameters

```python
# Update label dictionary to match your dataset
label_dict = {'normal_tissue': 0, 'tumor_tissue': 1}

# Number of classes
n_classes = 2

# Feature dimension (must match your extracted features)
feature_dim = 512  # 512 for ResNet18, 1024 for ResNet50
```

### Step 3: Run Training

```bash
# Activate your conda environment (if using)
conda activate attrimil

# Run training for all folds
python trainer_attrimil_abmil.py
```

## Advanced Usage

### Run a Specific Fold

Edit `config.py`:
```python
run_specific_fold = 0  # Run only fold 0
```

Then run:
```bash
python trainer_attrimil_abmil.py
```

### Run Different Folds in Parallel (on multiple GPUs)

Terminal 1 (GPU 0):
```bash
CUDA_VISIBLE_DEVICES=0 python trainer_attrimil_abmil.py  # with run_specific_fold=0
```

Terminal 2 (GPU 1):
```bash
CUDA_VISIBLE_DEVICES=1 python trainer_attrimil_abmil.py  # with run_specific_fold=1
```

### Adjust Training Parameters

Edit `config.py`:
```python
# Training settings
max_epoch = 200
learning_rate = 2e-4
early_stopping = True
early_stopping_patience = 20

# Loss weights
spatial_loss_weight = 1.0
ranking_loss_weight = 5.0
```

### Monitor Training with TensorBoard

```bash
tensorboard --logdir=./save_weights/your_experiment_name/
```

Then open your browser to `http://localhost:6006`

## Data Preparation (if not done yet)

If you haven't prepared your data with neighbor indices:

```bash
# 1. Generate neighbor indices
python create_3coords.py

# 2. Add indices to feature files
python coord_to_feature.py
```

## Output Files

After training, you'll find:

```
save_weights/your_experiment_name/
├── 0/                           # Fold 0
│   ├── s_0_checkpoint.pt       # Best model for fold 0
│   ├── s_0_checkpoint_0.pt     # Checkpoint at epoch 0
│   ├── s_0_checkpoint_10.pt    # Checkpoint at epoch 10
│   └── events.out.tfevents.*   # TensorBoard logs
├── 1/                           # Fold 1
│   └── ...
└── ...
```

## Troubleshooting

### CUDA Out of Memory
- Reduce batch size in dataloader (check `utils.py` or `dataloader.py`)
- Use a smaller model or feature dimension

### File Not Found Error
- Double-check all paths in `config.py`
- Ensure split CSV files exist (splits_0.csv, splits_1.csv, etc.)
- Verify feature files (.h5 and .pt) exist in data_dir

### Import Error
- Make sure you've installed all dependencies: `conda env create -f env.yml`
- Activate the environment: `conda activate attrimil`

## Testing After Training

Once training is complete, run evaluation:

```bash
python tester_attrimil_abmil.py
```

Make sure to update the model checkpoint path in the tester script.
