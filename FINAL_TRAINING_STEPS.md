# 🎯 FINAL STEPS TO START TRAINING

## ✅ What's Already Done:
- All code pushed to GitHub: https://github.com/viethaa/AttriMIL
- Training scripts created (train_colab.py, extract_features_colab.py, etc.)
- Auto-detection script created (auto_find_and_train.py)
- Videos exist in Google Drive shared folder

## 🚨 Current Issue:
Videos are in "Shared with me" but need to be in "My Drive/dataset2/" for Colab to access them.

---

## 📂 OPTION 1: Copy Videos Manually (Most Reliable)

### In Google Drive Web Browser (https://drive.google.com):

1. **Go to "Shared with me"** (left sidebar)
2. **Find dataset2 folder** (the one shared by your friend)
3. **Open each class folder** (Adenoma, Malignant, Normal)
4. **For each folder:**
   - Select all videos (Ctrl+A or Cmd+A)
   - Right-click → "Make a copy"
   - Choose destination: My Drive/dataset2/[class name]/
   - Wait for copy to complete (happens in cloud, fast)

### Expected Structure:
```
My Drive/
└── dataset2/
    ├── Adenoma/
    │   └── *.avi (all Adenoma videos)
    ├── Malignant/
    │   └── *.avi (all Malignant videos)
    └── Normal/
        └── *.avi (all Normal videos)
```

---

## 🤖 OPTION 2: Auto-Detection (If Videos Are Already Accessible)

If Colab can already see the videos somewhere in your Drive:

### In Colab:

```python
# Cell 1: Setup
from google.colab import drive
drive.mount('/content/drive')

# Cell 2: Clone repo
%cd /content/drive/MyDrive
!git clone https://github.com/viethaa/AttriMIL.git
%cd AttriMIL

# Cell 3: Auto-find videos
!python auto_find_and_train.py
```

This will search your entire Drive for .avi files and configure paths automatically.

---

## 🚀 Complete Training Pipeline (After Videos Are in Place)

### In Colab:

```python
# Cell 1: Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Cell 2: Navigate to project
%cd /content/drive/MyDrive/AttriMIL
!git pull origin main

# Cell 3: Verify videos exist
!ls -la /content/drive/MyDrive/dataset2/
!find /content/drive/MyDrive/dataset2 -name "*.avi" | wc -l

# Cell 4: Extract features (30-60 min)
!python extract_features_colab.py

# Cell 5: Create CSV dataset
!python create_dataset_csv_colab.py

# Cell 6: Train model
!python train_colab.py
```

---

## ⏱️ Time Estimates:
- **Copy videos** (if using Option 1): 10-30 minutes
- **Feature extraction**: 30-60 minutes (one-time, depends on video count)
- **CSV creation**: < 1 minute
- **Training**: 2-4 hours (150 epochs with early stopping)

---

## 📊 Expected Output:

### Feature Extraction:
```
Processing Normal (label=0)
Found 100 videos
Normal: 100%|████████| 100/100
✓ Successfully processed: 300 videos
```

### Training:
```
Epoch 1/150
Train Loss: 0.8543 | Acc: 0.6571
Val Loss: 0.7234 | Acc: 0.7111
✓ New best model saved!
```

---

## 🆘 Troubleshooting:

### "CSV file not found"
→ Run `create_dataset_csv_colab.py` first

### "No videos found"
→ Check videos are in `/content/drive/MyDrive/dataset2/Adenoma/`, etc.

### "Feature files not found"
→ Run `extract_features_colab.py` first

### "Out of memory"
→ Use Colab Pro or reduce batch size

---

## 📝 Quick Reference Commands:

```bash
# Check if videos exist
!find /content/drive/MyDrive/dataset2 -name "*.avi" | head -10

# Count videos per class
!ls /content/drive/MyDrive/dataset2/Adenoma/*.avi | wc -l
!ls /content/drive/MyDrive/dataset2/Malignant/*.avi | wc -l
!ls /content/drive/MyDrive/dataset2/Normal/*.avi | wc -l

# Update code from GitHub
%cd /content/drive/MyDrive/AttriMIL
!git pull origin main

# Monitor training
!tail -20 /content/drive/MyDrive/AttriMIL/results/logs/training.log

# Check GPU
!nvidia-smi
```

---

## ✅ Success Checklist:

- [ ] Videos copied to My Drive/dataset2/[Adenoma|Malignant|Normal]/
- [ ] Colab can see videos (verified with `find` command)
- [ ] Features extracted (`.pt` files in video_features/)
- [ ] CSV created (video_dataset.csv exists)
- [ ] Training started (seeing epoch outputs)
- [ ] Checkpoints saving to Drive (every 30 min)

---

## 🎓 Final Notes:

- **Everything is on GitHub**: Changes are saved at https://github.com/viethaa/AttriMIL
- **Automatic checkpointing**: Model saves every 30 min to Drive
- **Auto-resume**: If disconnected, just re-run training cell
- **Edit locally, train in Colab**: Push changes to GitHub, pull in Colab

**The hardest part is getting the videos copied. Once that's done, everything else is automated!**

---

## 📞 When You're Ready:

1. Restart your browser/terminal to fix clipboard issue
2. Follow Option 1 to copy videos
3. Run the training pipeline in Colab
4. You'll be training in less than 1 hour after videos are copied!

Good luck! 🚀
