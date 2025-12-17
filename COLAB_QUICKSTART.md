# Colab Training - Quick Start

**5-minute setup for training AttriMIL on Google Colab with Google Drive dataset**

---

## Prerequisites

- [ ] Dataset in Google Drive at: `MyDrive/dataset2/`
- [ ] Code pushed to GitHub
- [ ] Google account

---

## Step 1: Push Code to GitHub (One-time)

```bash
cd ~/Documents/GitHub/AttriMIL

git add config_env.py train_colab.py colab_train_attrimil.ipynb COLAB_SETUP.md
git commit -m "Add Colab support"
git push origin main
```

---

## Step 2: Open Colab Notebook

**Option A: Upload to Colab**
1. Go to https://colab.research.google.com
2. File → Upload notebook
3. Choose `colab_train_attrimil.ipynb`

**Option B: Open from GitHub**
1. Go to https://colab.research.google.com
2. File → Open notebook → GitHub tab
3. Enter: `https://github.com/YOUR_USERNAME/AttriMIL`
4. Select `colab_train_attrimil.ipynb`

---

## Step 3: Set GPU Runtime

1. Runtime → Change runtime type
2. Hardware accelerator: **GPU**
3. Save

---

## Step 4: Run Notebook

**Click "Run all" or run cells in order:**

### Cell 1: Mount Drive
```python
from google.colab import drive
drive.mount('/content/drive')
```
→ Click link, authorize Google account

### Cell 2: Clone/Update Repo
```python
# First time: clone
!cd /content/drive/MyDrive && \
 git clone https://github.com/YOUR_USERNAME/AttriMIL.git

# Later: pull updates
!cd /content/drive/MyDrive/AttriMIL && \
 git pull origin main
```

### Cell 3: Install Dependencies
```python
!pip install -q torch torchvision scikit-learn pandas numpy tensorboard
```

### Cell 4: Navigate to Project
```python
import os
os.chdir('/content/drive/MyDrive/AttriMIL')
```

### Cell 5: Verify Dataset
```python
from config_env import get_env_config, print_config
config = get_env_config()
print_config(config)
```
→ Check that paths show `/content/drive/MyDrive/dataset2`

### Cell 6: Start Training
```python
!python train_colab.py
```
→ This runs for hours. Keep tab open!

---

## That's It!

**Training will:**
- ✅ Load data from Google Drive (no downloads)
- ✅ Save checkpoints every 30 minutes
- ✅ Resume automatically if disconnected
- ✅ Save results to Drive

---

## Daily Workflow

### Edit code locally:
```bash
# On your Mac
cd ~/Documents/GitHub/AttriMIL
vim models/AttriMIL.py
git add . && git commit -m "Update model" && git push
```

### Pull and retrain in Colab:
```python
# In Colab notebook
!cd /content/drive/MyDrive/AttriMIL && git pull origin main
# Runtime → Restart runtime
!python train_colab.py  # Resumes from checkpoint
```

---

## Monitor Training

```python
# Check GPU
!nvidia-smi

# Check progress
!tail -20 /content/drive/MyDrive/AttriMIL/results/models/training.log

# TensorBoard
%load_ext tensorboard
%tensorboard --logdir /content/drive/MyDrive/AttriMIL/results/logs
```

---

## Troubleshooting

**Dataset not found?**
```python
# Verify paths
!ls -la /content/drive/MyDrive/dataset2/
```
→ Make sure dataset is at `MyDrive/dataset2/`

**Out of memory?**
- Use Colab Pro for more GPU RAM
- Check no other notebooks running

**Disconnected?**
- Just re-run Cell 6 (training cell)
- Will resume from last checkpoint

---

## Folder Structure

### Required in Google Drive:
```
MyDrive/
├── dataset2/              # Your dataset
│   ├── video_data/
│   │   └── video_dataset.csv
│   └── video_features/
│       └── *.pt files
│
└── AttriMIL/             # Cloned from GitHub
    └── (all project files)
```

---

## Tips

- **Keep Colab tab open** - Prevents disconnection
- **Use Colab Pro** - 24h runtime instead of 12h
- **Check checkpoints** - Should save every 30 min
- **Monitor GPU** - Run `!nvidia-smi` occasionally

---

## Full Guide

See `COLAB_SETUP.md` for complete documentation.
