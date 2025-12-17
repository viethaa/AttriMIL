# Google Colab Setup Checklist

Use this checklist to set up your Colab training environment.

---

## ✅ Phase 1: Local Setup (One-time)

### 1.1 Verify New Files Exist
```bash
cd ~/Documents/GitHub/AttriMIL
ls -1 config_env.py train_colab.py colab_train_attrimil.ipynb COLAB_*.md
```

**Expected output:**
```
COLAB_QUICKSTART.md
COLAB_REFACTOR_SUMMARY.md
COLAB_SETUP.md
colab_train_attrimil.ipynb
config_env.py
train_colab.py
```

- [ ] All 6 files present

### 1.2 Test Configuration
```bash
python -c "from config_env import get_env_config, print_config; print_config(get_env_config())"
```

**Expected output:**
- `Environment: local`
- `Running in Colab: False`
- Paths show `./data/full_dataset`

- [ ] Config test passes

### 1.3 Commit & Push to GitHub
```bash
git add config_env.py train_colab.py colab_train_attrimil.ipynb \
        COLAB_*.md COLAB_CHECKLIST.md

git commit -m "Add Google Colab support with Drive integration"

git push origin main
```

- [ ] Code pushed to GitHub
- [ ] Verified on GitHub web interface

---

## ✅ Phase 2: Google Drive Setup (One-time)

### 2.1 Upload Dataset to Drive

**Check what you need:**
- [ ] `video_dataset.csv` file
- [ ] `splits/` directory with split files
- [ ] `video_features/` directory with `.pt` files

**Option A: Using Google Drive Web**
1. Go to https://drive.google.com
2. Create folder: `dataset2`
3. Upload your dataset files

**Option B: Using rclone (Recommended)**
```bash
# Install rclone
brew install rclone

# Configure (one-time)
rclone config

# Copy dataset
rclone copy ./local_dataset_path/ gdrive:dataset2/ --progress
```

- [ ] Dataset uploaded to `MyDrive/dataset2/`
- [ ] Verified structure matches requirements

### 2.2 Verify Drive Structure
Required structure:
```
MyDrive/
└── dataset2/
    ├── video_data/
    │   ├── video_dataset.csv
    │   └── splits/
    │       └── splits_0.csv
    └── video_features/
        └── *.pt files
```

- [ ] Structure verified

---

## ✅ Phase 3: Clone Repo to Drive (One-time)

### 3.1 Open Temporary Colab Notebook
1. Go to https://colab.research.google.com
2. File → New notebook

### 3.2 Run Setup Commands
```python
# Cell 1: Mount Drive
from google.colab import drive
drive.mount('/content/drive')
```
- [ ] Drive mounted successfully

```python
# Cell 2: Clone repo
!cd /content/drive/MyDrive && \
 git clone https://github.com/YOUR_USERNAME/AttriMIL.git
```
Replace `YOUR_USERNAME` with your GitHub username

- [ ] Repo cloned to Drive

```python
# Cell 3: Verify
!ls -la /content/drive/MyDrive/AttriMIL/ | head -20
```
- [ ] Files visible in Drive

---

## ✅ Phase 4: First Training Run

### 4.1 Upload Notebook to Colab
1. Go to https://colab.research.google.com
2. File → Upload notebook
3. Choose: `colab_train_attrimil.ipynb`

- [ ] Notebook uploaded

### 4.2 Set GPU Runtime
1. Runtime → Change runtime type
2. Hardware accelerator: **GPU**
3. Click Save

- [ ] GPU runtime set

### 4.3 Run Setup Cells

**Cell 1: Mount Drive**
```python
from google.colab import drive
drive.mount('/content/drive')
```
- [ ] Drive mounted

**Cell 2: Update Code**
```python
!cd /content/drive/MyDrive/AttriMIL && \
 git pull origin main
```
- [ ] Latest code pulled

**Cell 3: Install Dependencies**
```python
!pip install -q torch torchvision scikit-learn pandas numpy tensorboard
```
- [ ] Dependencies installed

**Cell 4: Navigate to Project**
```python
import os
os.chdir('/content/drive/MyDrive/AttriMIL')
print(os.getcwd())
```
- [ ] In correct directory

**Cell 5: Verify Dataset**
```python
from config_env import get_env_config, print_config
config = get_env_config()
print_config(config)
```

**Expected output:**
- `Environment: colab`
- `Running in Colab: True`
- Paths show `/content/drive/MyDrive/dataset2`

- [ ] Config shows Colab environment
- [ ] Dataset paths correct

**Cell 6: Start Training**
```python
!python train_colab.py
```

- [ ] Training started
- [ ] No errors in first epoch
- [ ] Checkpoints being saved

---

## ✅ Phase 5: Verify Training Works

### 5.1 Check Outputs

**Monitor GPU:**
```python
!nvidia-smi
```
- [ ] GPU being used

**Check Checkpoints:**
```python
!ls -lh /content/drive/MyDrive/AttriMIL/results/models/
```
- [ ] Checkpoints appear

**Monitor Training:**
```python
!tail -30 /content/drive/MyDrive/AttriMIL/results/logs/training.log
```
- [ ] Loss decreasing
- [ ] No errors

### 5.2 Test Resume
1. Runtime → Interrupt execution (stop training)
2. Re-run Cell 6 (training cell)

Expected:
- Should print "Loading checkpoint: ..."
- Should resume from last epoch

- [ ] Resume works correctly

---

## ✅ Phase 6: Daily Workflow Setup

### 6.1 Bookmark Colab Notebook
1. Save notebook to Drive
2. Bookmark the Colab URL

- [ ] Notebook bookmarked

### 6.2 Test Edit → Push → Pull → Train
**On Mac:**
```bash
# Make a small change
echo "# Test comment" >> config_env.py
git add . && git commit -m "Test sync" && git push
```

**In Colab:**
```python
!cd /content/drive/MyDrive/AttriMIL && git pull origin main
!grep "Test comment" config_env.py  # Should find it
```

- [ ] Changes sync correctly

---

## ✅ Optional: Advanced Setup

### TensorBoard
```python
%load_ext tensorboard
%tensorboard --logdir /content/drive/MyDrive/AttriMIL/results/logs
```
- [ ] TensorBoard working (optional)

### Colab Pro
- [ ] Considered Colab Pro for longer runtimes (optional)

### Auto-reconnect
- [ ] Browser extension to prevent idle timeout (optional)

---

## 🎉 You're Done!

### What You Can Do Now:

✅ Edit code locally in VS Code/Warp
✅ Push to GitHub
✅ Pull in Colab
✅ Train on free GPU
✅ Dataset streams from Drive (no download)
✅ Checkpoints auto-save every 30 min
✅ Resume automatically if disconnected

---

## Quick Reference

### Daily Workflow:
```bash
# Mac: Edit & push
vim models/AttriMIL.py
git add . && git commit -m "Update" && git push

# Colab: Pull & train
!cd /content/drive/MyDrive/AttriMIL && git pull
!python train_colab.py
```

### If Disconnected:
Just re-run the training cell:
```python
!python train_colab.py  # Auto-resumes from checkpoint
```

### Monitor Training:
```python
!nvidia-smi  # Check GPU
!tail -20 /content/drive/MyDrive/AttriMIL/results/logs/training.log
```

---

## Troubleshooting

### Common Issues:

**"Drive not mounted"**
→ Re-run Cell 1 (mount Drive)

**"Dataset not found"**
→ Verify dataset at `MyDrive/dataset2/`
→ Check paths in Cell 5 output

**"Out of memory"**
→ Use Colab Pro
→ Restart runtime: Runtime → Restart runtime

**"Training disconnected"**
→ Normal for long training
→ Just re-run training cell to resume

**"Cannot find module"**
→ Re-run Cell 3 (install dependencies)
→ Verify in correct directory (Cell 4)

---

## Documentation

- **Quick Start:** `COLAB_QUICKSTART.md` (5 min guide)
- **Full Setup:** `COLAB_SETUP.md` (complete guide)
- **Summary:** `COLAB_REFACTOR_SUMMARY.md` (what changed)
- **This Checklist:** `COLAB_CHECKLIST.md`

---

## Support

Having issues? Check:
1. This checklist
2. `COLAB_QUICKSTART.md`
3. `COLAB_SETUP.md` (Troubleshooting section)
4. GitHub issues

---

**Happy Training! 🚀**
