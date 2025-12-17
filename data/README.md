# Data Directory

**⚠️ This directory no longer contains local datasets!**

## What Happened

All large dataset files (~92GB) have been removed from local storage to:
- Free up disk space on your Mac
- Use Google Drive for data storage instead
- Train exclusively on Google Colab with GPU

## Where Is The Data Now?

### For Colab Training (Recommended):
Data is stored in **Google Drive**:
```
/content/drive/MyDrive/dataset2/
├── video_data/
│   ├── video_dataset.csv
│   └── splits/
└── video_features/
    └── *.pt files
```

The training script (`train_colab.py`) automatically accesses data from Drive when running in Colab.

## Directory Structure

This folder maintains directory structure for reference and metadata files:

```
data/
├── README.md                    # This file
├── camelyon16/                  # Camelyon16 metadata
│   ├── README.md
│   ├── camelyon16_total.csv    # Metadata (kept)
│   └── splits/
│       └── splits_0.csv        # Split info (kept)
│
├── features/                    # Feature extraction info
│   └── video_features/
│       └── extraction_info.csv # Extraction metadata (kept)
│
├── full_dataset/                # Video dataset (EMPTY - use Drive)
│   ├── README.md
│   ├── Adenoma/                # Empty (videos in Drive)
│   ├── Malignant/              # Empty (videos in Drive)
│   └── Normal/                 # Empty (videos in Drive)
│
└── video/                       # Video metadata
    ├── video_data/
    │   ├── video_dataset.csv   # Metadata (kept)
    │   ├── dataset_report.txt  # Report (kept)
    │   └── splits/
    │       └── splits_0.csv    # Split info (kept)
    └── video_panning_data/
        ├── dataset.csv         # Metadata (kept)
        └── splits*.csv         # Split info (kept)
```

## What Was Removed

- **Video files**: All `.avi` files (~87GB)
- **Feature files**: All `.pt`, `.pkl`, `.h5` files (~5GB)
- **Parquet files**: Camelyon16 parquet data (~1.1GB)

Total space freed: **~92GB**

See `DATASET_REMOVED_MANIFEST.txt` for detailed removal log.

## What Was Kept

✅ **CSV metadata files** - Dataset info, splits, reports
✅ **README files** - Documentation
✅ **Directory structure** - Empty folders for reference
✅ **.gitignore** - Updated to ignore large files

## How to Use Data

### For Colab Training (Primary Method):

1. **Ensure data is in Google Drive:**
   ```
   MyDrive/dataset2/
   ```

2. **Run training on Colab:**
   ```python
   # In Colab notebook
   !python train_colab.py
   ```

   The script automatically detects Colab and uses Drive paths.

### For Local Testing (Optional):

If you need local data for testing:

**Option 1: Download from Drive**
```bash
# Using rclone
rclone copy gdrive:dataset2/ ./data/full_dataset/ --progress

# Or manually from Drive web interface
```

**Option 2: Download specific files**
```bash
# Use the download script for individual videos
python scripts/data_processing/download_individual_videos.py \
  --output-dir data/full_dataset \
  --class Adenoma  # Download only specific class
```

## Environment Detection

The project automatically detects whether you're running locally or in Colab:

```python
from config_env import get_env_config

config = get_env_config()

# In Colab: config['dataset_root'] = '/content/drive/MyDrive/dataset2'
# Locally:  config['dataset_root'] = './data/full_dataset'
```

## gitignore

Large files are now ignored by git:
- `*.avi`, `*.mp4` - Video files
- `*.pt`, `*.h5`, `*.pkl` - Feature files
- `*.parquet` - Data files
- Dataset directories

This ensures you never accidentally commit large files to GitHub.

## Recovery

If you need the original data:

1. **From Google Drive**: Download from `MyDrive/dataset2/`
2. **From original source**: Re-download using scripts in `scripts/data_processing/`
3. **From backup**: If you have local backups

## Summary

✅ **Local storage freed**: 92GB
✅ **Data location**: Google Drive (`MyDrive/dataset2/`)
✅ **Training**: Use Google Colab with `train_colab.py`
✅ **Metadata preserved**: CSV files kept for reference
✅ **Git-safe**: Large files ignored automatically

---

**For complete Colab setup instructions, see:**
- `COLAB_QUICKSTART.md` - 5-minute setup
- `COLAB_SETUP.md` - Full documentation
- `COLAB_CHECKLIST.md` - Step-by-step checklist
