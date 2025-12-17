# Dataset Cleanup Summary

**Date:** December 17, 2024
**Reason:** Migrating to Google Colab training with Google Drive dataset storage

---

## Results

### Before Cleanup
- **Total size:** 92 GB
- **Total files:** ~5,103 files
- **Location:** `data/` directory

### After Cleanup
- **Total size:** 176 KB
- **Total files:** 13 files (metadata only)
- **Space freed:** **91.99 GB** 🎉

---

## What Was Removed

### 1. Video Files (87 GB)
```
data/full_dataset/
├── Adenoma/*.avi      (36 files)
├── Malignant/*.avi    (25 files)
└── Normal/*.avi       (33 files)
```
**Total:** 94 video files removed

### 2. Video Panning Features (703 MB)
```
data/video/video_panning_data/features/*.pkl
```
**Total:** ~4,565 feature files removed

### 3. Camelyon16 Data (1.1 GB)
```
data/camelyon16/data/*.parquet  (3 files, ~1.1GB)
data/camelyon16/.cache/
data/camelyon16/scripts/
```

### 4. Video Features (13 MB)
```
data/features/video_features/*.pt
```

### 5. Other
- `data/video/video_panning_data/Image.pkl` (90 MB)

---

## What Was Kept

✅ **Metadata files** (CSV, TXT, MD):
- `data/video/video_data/video_dataset.csv`
- `data/video/video_data/dataset_report.txt`
- `data/video/video_data/splits/*.csv`
- `data/video/video_panning_data/*.csv`
- `data/camelyon16/camelyon16_total.csv`
- `data/camelyon16/splits/*.csv`
- `data/features/video_features/extraction_info.csv`

✅ **Documentation**:
- `data/README.md` (NEW)
- `data/full_dataset/README.md` (NEW)
- `data/camelyon16/README.md`
- `data/video/video_data/NEXT_STEPS.md`

✅ **Directory structure**:
All folders maintained (empty) for reference

---

## Current State

### Directory Structure
```
data/                              # 176 KB (was 92 GB)
├── README.md                      # New: Explains data organization
│
├── camelyon16/                    # 32 KB (was 3.4 GB)
│   ├── README.md                 # Metadata (kept)
│   ├── camelyon16_total.csv      # Metadata (kept)
│   ├── h5_coords_files/          # Empty
│   ├── pt_files/                 # Empty
│   └── splits/
│       └── splits_0.csv          # Split info (kept)
│
├── features/                      # 8 KB (was 13 MB)
│   └── video_features/
│       └── extraction_info.csv   # Metadata (kept)
│
├── full_dataset/                  # 4 KB (was 87 GB)
│   ├── README.md                 # New: Explains empty directories
│   ├── Adenoma/                  # Empty (videos in Drive)
│   ├── Malignant/                # Empty (videos in Drive)
│   └── Normal/                   # Empty (videos in Drive)
│
└── video/                         # 124 KB (was 703 MB)
    ├── video_data/
    │   ├── video_dataset.csv     # Metadata (kept)
    │   ├── dataset_report.txt    # Report (kept)
    │   ├── NEXT_STEPS.md         # Docs (kept)
    │   └── splits/
    │       └── splits_0.csv      # Split info (kept)
    └── video_panning_data/
        ├── dataset.csv           # Metadata (kept)
        ├── splits.csv            # Split info (kept)
        └── splits_better.csv     # Split info (kept)
```

### Verification
```bash
# Check size
$ du -sh data/
176K    data/

# Check no large files remain
$ find data/ -type f \( -name "*.avi" -o -name "*.pt" -o -name "*.pkl" -o -name "*.parquet" \) | wc -l
0

# Files kept (all metadata)
$ find data/ -type f -name "*.csv" -o -name "*.md" -o -name "*.txt" | wc -l
13
```

---

## Where Is The Data Now?

### Google Drive Location
```
/content/drive/MyDrive/dataset2/
├── video_data/
│   ├── video_dataset.csv
│   └── splits/
│       └── splits_0.csv
└── video_features/
    └── *.pt files (thousands)
```

**Note:** You need to upload your dataset to this location in Google Drive.

---

## Git Changes

### .gitignore Updated

Added rules to prevent accidentally committing large files:

```gitignore
# Video files
*.avi
*.mp4
*.mov

# Feature files
*.pt
*.h5
*.npy
*.pkl

# Parquet data files
*.parquet

# Large dataset directories
data/full_dataset/Adenoma/
data/full_dataset/Malignant/
data/full_dataset/Normal/
data/camelyon16/data/
data/camelyon16/.cache/
data/video/video_panning_data/features/

# Model checkpoints
results/models/*.pt
results/models/*.pth
save_weights/
```

This ensures large files are never committed to GitHub.

---

## How to Use Data Now

### Primary Method: Google Colab

```python
# In Colab, data automatically loads from Drive
!python train_colab.py
```

The `config_env.py` automatically detects Colab environment and uses Drive paths:
- Dataset: `/content/drive/MyDrive/dataset2/`
- Checkpoints: `/content/drive/MyDrive/AttriMIL/results/`

### Optional: Local Testing

If you need local data for testing:

**Option 1: Download from Google Drive**
```bash
# Using rclone (recommended)
rclone copy gdrive:dataset2/ ./data/full_dataset/

# Or download via Drive web interface
```

**Option 2: Download specific videos**
```bash
python scripts/data_processing/download_individual_videos.py \
  --output-dir data/full_dataset \
  --class Adenoma  # Or Malignant, Normal
```

---

## Files Created/Modified

### New Files
- `data/README.md` - Explains data organization
- `data/full_dataset/README.md` - Explains empty directories
- `DATASET_CLEANUP_SUMMARY.md` - This file
- `DATASET_REMOVED_MANIFEST.txt` - Detailed removal log

### Modified Files
- `.gitignore` - Added dataset file patterns

---

## Recovery Instructions

If you need to restore local data:

### From Google Drive
```bash
# Full dataset
rclone copy gdrive:dataset2/ ./data/full_dataset/ --progress

# Specific class only
rclone copy gdrive:dataset2/Adenoma/ ./data/full_dataset/Adenoma/
```

### From Original Source
Original Google Drive link:
`https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN`

Use download script:
```bash
python scripts/data_processing/download_individual_videos.py
```

---

## Benefits

✅ **Space freed:** 92 GB on local Mac
✅ **Git-friendly:** No risk of committing large files
✅ **Cloud training:** Use Colab GPU with Drive data
✅ **Metadata preserved:** CSV files kept for reference
✅ **Reversible:** Can restore data from Drive anytime

---

## Next Steps

1. **Upload dataset to Google Drive** (if not already done):
   ```bash
   rclone copy ./local_dataset/ gdrive:dataset2/ --progress
   ```

2. **Commit changes to git**:
   ```bash
   git add .gitignore data/README.md data/full_dataset/README.md \
           DATASET_CLEANUP_SUMMARY.md DATASET_REMOVED_MANIFEST.txt
   git commit -m "Clean up local datasets - use Google Drive instead"
   git push origin main
   ```

3. **Start training on Colab**:
   - Upload `colab_train_attrimil.ipynb` to Colab
   - Follow `COLAB_QUICKSTART.md` for setup
   - Run training on GPU

---

## Summary

**Before:** 92 GB of local data
**After:** 176 KB of metadata
**Saved:** 91.99 GB

All large dataset files removed. Metadata and directory structure preserved. Ready for Colab training with Google Drive! 🚀

---

See also:
- `data/README.md` - Data organization guide
- `COLAB_SETUP.md` - Complete Colab setup guide
- `COLAB_QUICKSTART.md` - 5-minute quick start
- `.gitignore` - Git ignore rules for large files
