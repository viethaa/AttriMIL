# 🚀 START HERE - Your Exact Next Steps

**Goal:** Get your AttriMIL code training on Google Colab GPU with dataset in Google Drive

**Time needed:** 10 minutes

---

## Where You Are Now

✅ Code ready for Colab (I built the integration)
✅ Local datasets removed (92GB freed)
✅ gitignore configured (won't commit large files)
⏳ **NEXT:** Push to GitHub and start training

---

## STEP 1: Push Your Code to GitHub (2 minutes)

### Option A: Quick Script (Easiest)

```bash
# From AttriMIL directory
./PUSH_TO_GITHUB.sh
```

This automatically:
- Adds all files
- Creates commit with detailed message
- Pushes to GitHub

### Option B: Manual Commands

```bash
# Add files
git add config_env.py train_colab.py colab_train_attrimil.ipynb \
        COLAB_*.md DATASET_*.md .gitignore data/ docs/ scripts/

# Commit
git commit -m "Add Colab support with Drive integration (freed 92GB)"

# Push
git push origin main
```

### Verify It Worked

1. Go to: `https://github.com/YOUR_USERNAME/AttriMIL`
2. Check you see:
   - `config_env.py`
   - `train_colab.py`
   - `colab_train_attrimil.ipynb`
   - `COLAB_QUICKSTART.md`
3. Verify `data/` folders are empty (only README files)

✅ **Checkpoint:** Code on GitHub? → Move to Step 2

---

## STEP 2: Upload Dataset to Google Drive (5 minutes setup, hours upload)

### Create Folder Structure

In Google Drive, create:
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

### Upload Options

**Option A: Using rclone (Recommended for 1TB)**
```bash
# Install rclone
brew install rclone  # Mac

# Configure Google Drive
rclone config
# Follow prompts to add your Google Drive

# Upload dataset (this will take hours for large datasets)
rclone copy /path/to/local/dataset/ gdrive:dataset2/ --progress --transfers 8
```

**Option B: Google Drive Web Interface**
- Go to https://drive.google.com
- Create folder `dataset2`
- Upload your dataset folders
- (Slow for large files, but works)

**Option C: If you already have it in Drive**
- Just rename/move existing folder to `dataset2`
- Verify structure matches above

✅ **Checkpoint:** Dataset in `MyDrive/dataset2/`? → Move to Step 3

---

## STEP 3: Open Colab and Clone Your Repo (2 minutes)

### A. Open Colab
Go to: https://colab.research.google.com

### B. Upload Your Notebook

**Option 1: Upload File**
- File → Upload notebook
- Choose `colab_train_attrimil.ipynb` from your local machine

**Option 2: From GitHub**
- File → Open notebook → GitHub tab
- Enter: `https://github.com/YOUR_USERNAME/AttriMIL`
- Select `colab_train_attrimil.ipynb`

### C. Set GPU Runtime
- Runtime → Change runtime type
- Hardware accelerator: **GPU**
- GPU type: T4 (free tier) or better
- Click **Save**

✅ **Checkpoint:** Notebook open in Colab with GPU? → Move to Step 4

---

## STEP 4: Run the Notebook (1 minute per cell)

### Run These Cells in Order:

**Cell 1: Mount Google Drive**
```python
from google.colab import drive
drive.mount('/content/drive')
```
→ Click the link, authorize your Google account
→ ✅ Should show "Mounted at /content/drive"

**Cell 2: Clone Repository**
```python
# First time only
!cd /content/drive/MyDrive && \
 git clone https://github.com/YOUR_USERNAME/AttriMIL.git

# Or if already cloned, pull updates
!cd /content/drive/MyDrive/AttriMIL && \
 git pull origin main
```
→ ✅ Should show "Cloning into..." or "Already up to date"

**Cell 3: Install Dependencies**
```python
!pip install -q torch torchvision scikit-learn pandas numpy tensorboard
```
→ ✅ Should install packages

**Cell 4: Navigate to Project**
```python
import os
os.chdir('/content/drive/MyDrive/AttriMIL')
print(os.getcwd())
```
→ ✅ Should print `/content/drive/MyDrive/AttriMIL`

**Cell 5: Verify Setup (IMPORTANT!)**
```python
from config_env import get_env_config, print_config
config = get_env_config()
print_config(config)
```
→ ✅ Should show:
- `Environment: colab`
- `Running in Colab: True`
- `Dataset Root: /content/drive/MyDrive/dataset2`

**Cell 6: Verify Dataset Exists**
```python
import os
print("CSV exists:", os.path.exists(config['csv_path']))
print("Features exist:", os.path.exists(config['feature_dir']))

# List first few features
!ls {config['feature_dir']} | head -10
```
→ ✅ Should show `True` for both
→ ✅ Should list `.pt` files

**Cell 7: START TRAINING! 🚀**
```python
!python train_colab.py
```
→ This runs for hours
→ Keep browser tab open
→ Checkpoints save to Drive every 30 min

---

## STEP 5: Monitor Training

### Check Progress
```python
# In a new cell (while training runs)
!tail -20 /content/drive/MyDrive/AttriMIL/results/logs/training.log
```

### Check GPU Usage
```python
!nvidia-smi
```

### View Checkpoints
```python
!ls -lh /content/drive/MyDrive/AttriMIL/results/models/
```

### TensorBoard (Optional)
```python
%load_ext tensorboard
%tensorboard --logdir /content/drive/MyDrive/AttriMIL/results/logs
```

---

## 🔥 What Happens Automatically

Thanks to the code I built:

✅ **Auto-detects Colab** - No manual configuration
✅ **Auto-mounts Drive** - Handled by `train_colab.py`
✅ **Auto-configures paths** - Uses `/content/drive/MyDrive/dataset2`
✅ **Auto-checkpoints** - Saves to Drive every 30 min
✅ **Auto-resumes** - If disconnected, just re-run Cell 7

---

## 💡 Daily Workflow (After Initial Setup)

### Edit Code Locally
```bash
# On your Mac in Warp/VS Code
cd ~/Documents/GitHub/AttriMIL
vim models/AttriMIL.py

# Push changes
git add . && git commit -m "Update model" && git push
```

### Update in Colab
```python
# In Colab
!cd /content/drive/MyDrive/AttriMIL && git pull origin main

# Restart runtime
# Runtime → Restart runtime

# Re-run training cell
!python train_colab.py  # Automatically resumes from checkpoint
```

---

## 🆘 Troubleshooting

### "Dataset not found"
```python
# Check paths
from config_env import get_env_config
config = get_env_config()
print("Looking for CSV at:", config['csv_path'])
print("Exists?", os.path.exists(config['csv_path']))

# Verify Drive structure
!ls -la /content/drive/MyDrive/dataset2/
```
→ Make sure dataset is at `MyDrive/dataset2/`

### "Drive not mounted"
```python
# Re-mount
from google.colab import drive
drive.mount('/content/drive', force_remount=True)
```

### "Out of memory"
- Use Colab Pro (more GPU RAM)
- Or reduce batch size in config

### "Disconnected"
- Normal for long training
- Just re-run Cell 7 (`!python train_colab.py`)
- It will automatically resume from last checkpoint

---

## 📊 Progress Checklist

Use this to track your setup:

- [ ] **Step 1:** Code pushed to GitHub
- [ ] **Step 2:** Dataset uploaded to `MyDrive/dataset2/`
- [ ] **Step 3:** Notebook open in Colab with GPU
- [ ] **Step 4 - Cell 1:** Drive mounted
- [ ] **Step 4 - Cell 2:** Repo cloned to Drive
- [ ] **Step 4 - Cell 3:** Dependencies installed
- [ ] **Step 4 - Cell 4:** In correct directory
- [ ] **Step 4 - Cell 5:** Config shows Colab environment
- [ ] **Step 4 - Cell 6:** Dataset verified
- [ ] **Step 4 - Cell 7:** Training started
- [ ] **Step 5:** Training running, checkpoints saving

---

## 🎯 Summary

**What ChatGPT recommended:**
1. ✅ GitHub for code
2. ✅ Clone in Colab
3. ✅ Mount Drive
4. ✅ Reference dataset from Drive
5. ✅ Save checkpoints to Drive

**What I already built:**
- All of the above, **fully automated**
- Auto-detection (no manual path changes)
- Auto-checkpointing every 30 min
- Auto-resume after disconnection
- Complete documentation

**Your action items:**
1. Run `./PUSH_TO_GITHUB.sh` (2 min)
2. Upload dataset to Drive (hours, but one-time)
3. Open Colab notebook (2 min)
4. Run cells in order (5 min)
5. Training starts! 🚀

---

## 📚 Documentation

- **This file** - Quick start (you are here)
- `COLAB_QUICKSTART.md` - 5-minute guide
- `COLAB_SETUP.md` - Complete documentation
- `COLAB_CHECKLIST.md` - Detailed checklist
- `COMMIT_GUIDE.md` - Git instructions

---

## ⚡ Quick Commands Reference

```bash
# STEP 1: Push to GitHub
./PUSH_TO_GITHUB.sh

# Or manually
git add . && git commit -m "Add Colab support" && git push

# STEP 2: Upload dataset (using rclone)
rclone copy /local/dataset/ gdrive:dataset2/ --progress
```

```python
# STEP 3-4: In Colab notebook

# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Clone repo (first time)
!cd /content/drive/MyDrive && \
 git clone https://github.com/YOUR_USERNAME/AttriMIL.git

# Navigate
import os
os.chdir('/content/drive/MyDrive/AttriMIL')

# Start training
!python train_colab.py
```

---

**Ready? Start with Step 1!** 🚀

Questions? Check the troubleshooting section above or see `COLAB_SETUP.md` for detailed help.
