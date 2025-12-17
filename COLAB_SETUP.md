# Google Colab Training Setup Guide

Complete guide to train AttriMIL on Google Colab with dataset in Google Drive

## Overview

This setup allows you to:
- ✅ Train on Google Colab's free GPU
- ✅ Keep 1TB dataset in Google Drive (no local copies needed)
- ✅ Edit code locally in VS Code/Warp
- ✅ Sync via GitHub
- ✅ Auto-save checkpoints to Drive (survives disconnections)
- ✅ Resume training automatically

---

## Prerequisites

### 1. Google Drive Structure

Your Google Drive should have this structure:

```
MyDrive/
├── dataset2/                          # Your 1TB dataset
│   ├── video_data/
│   │   ├── video_dataset.csv         # Video metadata
│   │   └── splits/                   # Train/val/test splits
│   │       └── splits_0.csv
│   └── video_features/               # Extracted features
│       ├── video_001.pt
│       ├── video_002.pt
│       └── ...
│
└── AttriMIL/                         # GitHub repo (cloned to Drive)
    ├── config_env.py                 # Auto-detects environment
    ├── train_colab.py               # Colab training script
    ├── colab_train_attrimil.ipynb   # Jupyter notebook
    ├── models/
    ├── dataloader_video.py
    └── ...
```

### 2. Local Machine Setup

**Clone repository:**
```bash
cd ~/Documents/GitHub
git clone https://github.com/YOUR_USERNAME/AttriMIL.git
cd AttriMIL
```

**Verify new files exist:**
```bash
ls -1 config_env.py train_colab.py colab_train_attrimil.ipynb
```

---

## Setup Steps

### Step 1: Upload Dataset to Google Drive

**Option A: Using Google Drive Web Interface**
1. Go to https://drive.google.com
2. Create folder: `dataset2`
3. Upload your dataset folders:
   - `video_data/`
   - `video_features/`

**Option B: Using rclone (Recommended for large datasets)**
```bash
# Install rclone
brew install rclone  # Mac
# or
sudo apt install rclone  # Linux

# Configure Google Drive
rclone config  # Follow prompts to add Google Drive

# Copy dataset to Drive (this will take time for 1TB)
rclone copy ./local_dataset/ remote:dataset2/ --progress --transfers 8
```

**Option C: Copy your existing Drive folder**
If dataset is already in Drive (e.g., shared folder), just copy/move it to `MyDrive/dataset2`

---

### Step 2: Push Code to GitHub

From your local machine:

```bash
cd ~/Documents/GitHub/AttriMIL

# Add new files
git add config_env.py train_colab.py colab_train_attrimil.ipynb COLAB_SETUP.md

# Commit
git commit -m "Add Colab training support with Google Drive integration"

# Push to GitHub
git push origin main
```

---

### Step 3: Clone Repository to Google Drive

**Open Google Colab:** https://colab.research.google.com

**Create a new notebook temporarily** and run:

```python
# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Clone your repo to Drive
!cd /content/drive/MyDrive && \
 git clone https://github.com/YOUR_USERNAME/AttriMIL.git

# Verify
!ls -la /content/drive/MyDrive/AttriMIL/
```

**You only need to do this once!** Future updates use `git pull`

---

### Step 4: Upload & Run Colab Notebook

1. **Upload notebook to Colab:**
   - Go to: https://colab.research.google.com
   - File → Upload notebook
   - Choose `colab_train_attrimil.ipynb` from your local machine
   - Or: File → Open notebook → GitHub → Enter your repo URL

2. **Set GPU runtime:**
   - Runtime → Change runtime type
   - Hardware accelerator: **GPU**
   - GPU type: T4 (free) or A100/V100 (Colab Pro)
   - Save

3. **Run all cells:**
   - Runtime → Run all
   - Or: Run cells one-by-one (Ctrl+Enter / Cmd+Enter)

---

## Training Workflow

### 1. Edit Code Locally

**On your Mac:**
```bash
cd ~/Documents/GitHub/AttriMIL

# Edit files in VS Code / Warp
code .

# Make changes to models, configs, etc.
vim models/AttriMIL.py

# Test locally (optional - if you have small test dataset)
python train_colab.py  # Will use local paths automatically
```

### 2. Push to GitHub

```bash
# Commit changes
git add .
git commit -m "Update model architecture"
git push origin main
```

### 3. Pull in Colab & Retrain

**In Colab notebook:**

```python
# Pull latest code
!cd /content/drive/MyDrive/AttriMIL && git pull origin main

# Restart runtime (Runtime → Restart runtime)
# Then re-run training cells
```

---

## How It Works

### Environment Auto-Detection

`config_env.py` automatically detects where it's running:

```python
from config_env import get_env_config

config = get_env_config()

# In Colab:
# config['dataset_root'] = '/content/drive/MyDrive/dataset2'
# config['save_dir'] = '/content/drive/MyDrive/AttriMIL/results/models'

# On Mac:
# config['dataset_root'] = './data/full_dataset'
# config['save_dir'] = './results/models'
```

### Streaming / Lazy Loading

The dataloader only loads features when needed:

```python
class Video_MIL_Dataset:
    def __getitem__(self, idx):
        # Features loaded on-demand (not all at once)
        features = torch.load(feature_path)
        return features, label
```

**Benefits:**
- ✅ No need to download entire dataset
- ✅ Works with 1TB datasets in Drive
- ✅ Minimal memory usage

### Checkpoint System

Automatically saves to Drive every 30 minutes:

```python
checkpoint_mgr = ColabCheckpointManager(
    save_dir='/content/drive/MyDrive/AttriMIL/results/models',
    interval_minutes=30
)
```

**If Colab disconnects:**
1. Re-run training cell
2. Automatically resumes from last checkpoint
3. No data loss!

---

## Folder Structure

### Complete Project Layout

```
AttriMIL/                              # Your GitHub repo
├── config_env.py                      # ✨ NEW: Environment detection
├── train_colab.py                     # ✨ NEW: Colab training script
├── colab_train_attrimil.ipynb        # ✨ NEW: Jupyter notebook
├── COLAB_SETUP.md                    # ✨ NEW: This guide
│
├── config.py                          # Original config (Camelyon16)
├── config_video.py                    # Original video config (local paths)
│
├── dataloader_video.py               # Video dataloader (works with both)
├── trainer_video.py                   # Original trainer
│
├── models/                            # Model definitions
│   └── AttriMIL.py
│
├── data/                              # Local data (Mac only)
│   └── full_dataset/
│
└── results/                           # Training outputs
    ├── models/                        # Saved checkpoints
    └── logs/                          # TensorBoard logs
```

### Google Drive Layout

```
MyDrive/
├── dataset2/                          # 1TB dataset (never downloaded)
│   ├── video_data/
│   │   ├── video_dataset.csv
│   │   └── splits/
│   │       └── splits_0.csv
│   └── video_features/
│       └── *.pt files
│
└── AttriMIL/                         # Git repo cloned to Drive
    ├── (same as above)
    └── results/                      # Persists across Colab sessions
        ├── models/
        │   ├── best_latest.pt
        │   ├── checkpoint_latest.pt
        │   └── periodic_epoch_*.pt
        └── logs/
            └── tensorboard_events
```

---

## Code Snippets

### Dataset Loader (Configurable)

The dataloader automatically uses the right paths:

```python
from config_env import get_env_config

config = get_env_config()

# Works on both Colab and local
dataset = Video_MIL_Dataset(
    csv_path=config['csv_path'],          # Auto-detected path
    feature_dir=config['feature_dir'],    # Auto-detected path
    label_dict=config['label_dict']
)
```

### Training Script

Minimal example:

```python
# train_colab.py (already created for you)

from config_env import get_env_config, is_colab

# Mount Drive if in Colab
if is_colab():
    from google.colab import drive
    drive.mount('/content/drive')

# Get config (auto-detects environment)
config = get_env_config()

# Load data (from Drive in Colab, local otherwise)
dataset = Video_MIL_Dataset(
    csv_path=config['csv_path'],
    feature_dir=config['feature_dir']
)

# Train
model = AttriMIL(...)
optimizer = ...

for epoch in range(config['max_epoch']):
    train(...)

    # Auto-saves to Drive every 30 min
    if checkpoint_mgr.should_save():
        checkpoint_mgr.save_checkpoint(...)
```

### Colab Setup Cell

Essential Colab cell (already in notebook):

```python
# Cell 1: Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Cell 2: Clone/update repo
!cd /content/drive/MyDrive && \
 git clone https://github.com/YOUR_USERNAME/AttriMIL.git

# Or pull updates
!cd /content/drive/MyDrive/AttriMIL && \
 git pull origin main

# Cell 3: Navigate to project
import os
os.chdir('/content/drive/MyDrive/AttriMIL')

# Cell 4: Run training
!python train_colab.py
```

---

## Tips & Best Practices

### 1. GitHub Syncing

**Push code from Mac:**
```bash
git add .
git commit -m "Update model"
git push origin main
```

**Pull in Colab:**
```python
!cd /content/drive/MyDrive/AttriMIL && git pull origin main
```

**Pro tip:** Create a cell at top of notebook:
```python
# Quick update cell
!cd /content/drive/MyDrive/AttriMIL && \
 git pull origin main && \
 echo "✓ Code updated!"
```

### 2. Prevent Colab Disconnection

**Keep tab active:**
- Don't close Colab tab
- Browser extension: "Colab Auto-Clicker" (prevent idle timeout)

**Use Colab Pro:**
- 24-hour runtime (vs 12 hours free)
- Better GPUs (A100/V100 vs T4)
- Worth it for multi-day training

**Periodic saves:**
```python
# Already built into train_colab.py
checkpoint_mgr = ColabCheckpointManager(
    interval_minutes=30  # Adjust as needed
)
```

### 3. Monitor Training

**TensorBoard in Colab:**
```python
%load_ext tensorboard
%tensorboard --logdir /content/drive/MyDrive/AttriMIL/results/logs
```

**Check GPU usage:**
```python
!nvidia-smi
```

**Monitor checkpoints:**
```python
!ls -lh /content/drive/MyDrive/AttriMIL/results/models/
```

### 4. Testing Locally First

Before long Colab training, test locally:

```bash
# Create small test dataset
mkdir -p data/test_features
cp data/full_dataset/video_features/sample*.pt data/test_features/

# Run quick test
python train_colab.py --max_epoch 2
```

---

## Troubleshooting

### Dataset Not Found

**Error:** `FileNotFoundError: CSV file not found`

**Solution:**
```python
# Verify paths
from config_env import get_env_config, print_config
config = get_env_config()
print_config(config)

# Check if files exist
import os
print(os.path.exists(config['csv_path']))
print(os.path.exists(config['feature_dir']))

# List Drive contents
!ls -la /content/drive/MyDrive/dataset2/
```

### Out of Memory

**Error:** `CUDA out of memory`

**Solutions:**
1. Use Colab Pro (more GPU RAM)
2. Reduce effective batch size (though MIL uses batch=1)
3. Use gradient accumulation
4. Check for memory leaks

### Slow Training

**Possible causes:**
- Slow Drive access (normal for large files)
- Network throttling
- CPU bottleneck (feature loading)

**Solutions:**
1. Use Colab Pro (faster storage)
2. Reduce `num_workers` to 0
3. Pre-cache features (if enough RAM)

### Git Issues

**Can't pull updates:**
```python
# Reset any local changes
!cd /content/drive/MyDrive/AttriMIL && \
 git reset --hard origin/main && \
 git pull origin main
```

---

## Example Session

### Complete Training Session

```python
# ============================================
# Colab Notebook - Complete Training Session
# ============================================

# Cell 1: Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Cell 2: Update code from GitHub
!cd /content/drive/MyDrive/AttriMIL && \
 git pull origin main

# Cell 3: Setup environment
import os
os.chdir('/content/drive/MyDrive/AttriMIL')

# Cell 4: Verify setup
from config_env import get_env_config, print_config
config = get_env_config()
print_config(config)

!ls {config['feature_dir']} | head -10

# Cell 5: Start training
!python train_colab.py

# Cell 6: Monitor with TensorBoard (optional)
%load_ext tensorboard
%tensorboard --logdir {config['log_dir']}

# Cell 7: Check progress
!tail -50 {config['log_dir']}/training.log

# Cell 8: After training - download results
!tar -czf /content/results.tar.gz -C {config['save_dir']} .
from google.colab import files
files.download('/content/results.tar.gz')
```

---

## Summary

### What You Can Do Now

✅ **Edit locally** - VS Code / Warp on your Mac
✅ **Train on Colab** - Free GPU, dataset in Drive
✅ **GitHub sync** - Push/pull code seamlessly
✅ **Auto-checkpoints** - Survive disconnections
✅ **No downloads** - Stream data from Drive
✅ **Resume training** - Automatically from last checkpoint

### Next Steps

1. ✅ Push new code to GitHub
2. ✅ Clone repo to Google Drive
3. ✅ Upload notebook to Colab
4. ✅ Run training!
5. ✅ Edit code → Push → Pull → Retrain

**You're ready to train!** 🚀

---

## Support

**Issues?**
- Check this guide first
- Verify paths in `config_env.py`
- Test locally before Colab
- Check GitHub issues

**Want to customize?**
- Edit `config_env.py` for paths
- Modify `train_colab.py` for training logic
- Update notebook for your workflow
