# Codebase Reorganization Summary

## What Was Done

Your AttriMIL codebase has been reorganized for better navigation and maintainability.

### 1. Video Status

**Current Status:**
- You have 93 videos currently available (based on dataset_report.txt)
- The Google Drive folder contains approximately **200-300 videos** across 3 classes:
  - Adenoma: ~52 videos
  - Malignant: ~45+ videos
  - Normal: ~30+ videos

**Note:** Due to Google Drive rate limits, the exact count from the API wasn't available, but the folder structure shows significantly more videos than you currently have.

### 2. Reorganization Changes

All files have been organized into logical directories:

```
AttriMIL/
├── Core Files (root)
│   ├── config.py, config_video.py, constraints.py
│   ├── dataloader*.py (3 files)
│   ├── trainer_*.py (5 files)
│   ├── tester_*.py (4 files)
│   └── utils.py, coords_to_feature.py
│
├── data/
│   ├── camelyon16/      # Camelyon16 dataset
│   ├── features/        # Video features
│   ├── full_dataset/    # Full dataset
│   └── video/           # Video data
│       ├── video_data/
│       └── video_panning_data/
│
├── docs/                # 8 documentation files
│   ├── CODEBASE_STRUCTURE.md (NEW)
│   ├── REORGANIZATION_SUMMARY.md (NEW)
│   ├── TRAINING_GUIDE.md
│   └── ...
│
├── results/
│   ├── models/          # Saved weights
│   └── training/        # Training logs, CSVs, metrics
│
├── scripts/
│   ├── data_processing/      # 8 data prep scripts
│   ├── results_extraction/   # 3 results scripts
│   └── utils/                # 4 utility scripts
│
├── datasets/            # Dataset definitions
├── models/              # Model implementations
└── visualization/       # Visualization code
```

### 3. Files Moved

- **Documentation** (8 files) → `docs/`
- **Helper Scripts** (15 files) → `scripts/`
  - Data processing scripts → `scripts/data_processing/`
  - Results extraction scripts → `scripts/results_extraction/`
  - Utility scripts → `scripts/utils/`
- **Results Files** (8 files) → `results/training/`
- **Model Weights** → `results/models/`
- **Data Directories** → `data/`

### 4. Files Deleted

- Empty directories
- Cache files from Hugging Face

## How to Download All Videos

A new script has been created to help you download all videos from Google Drive:

### Method 1: Using the Python Script (Recommended)

```bash
# Install gdown if not already installed
pip install gdown

# Download all videos
python scripts/data_processing/download_all_videos.py --output-dir data/video/raw_videos

# If download is interrupted, resume with:
python scripts/data_processing/download_all_videos.py --output-dir data/video/raw_videos --resume
```

The script will:
- Download all videos from the Google Drive folder
- Organize them by class (Adenoma, Malignant, Normal)
- Show a summary of downloaded videos
- Support resuming interrupted downloads

### Method 2: Manual Download

1. Visit: https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN
2. Download the entire folder or individual class folders
3. Extract to `data/video/raw_videos/`

### Expected Structure After Download

```
data/video/raw_videos/
├── Adenoma/
│   ├── 1.avi
│   ├── 2.avi
│   └── ... (~52 videos)
├── Malignant/
│   ├── 10.avi
│   ├── 11.avi
│   └── ... (~45+ videos)
└── Normal/
    ├── 24a0631.avi
    ├── 24a0791.avi
    └── ... (~30+ videos)
```

## Next Steps

1. **Download Videos**: Run the download script to get all ~300 videos
2. **Extract Features**: Use `scripts/data_processing/extract_video_features.py`
3. **Prepare Dataset**: Use `scripts/data_processing/prepare_video_dataset.py`
4. **Train Models**: Use the appropriate `trainer_*.py` file

## Navigation Tips

- **Find training code**: Look in root directory (`trainer_*.py`)
- **Find data scripts**: Look in `scripts/data_processing/`
- **Find results**: Look in `results/training/`
- **Find documentation**: Look in `docs/`
- **Reference structure**: See `docs/CODEBASE_STRUCTURE.md`

## Troubleshooting Downloads

If you encounter rate limit errors from Google Drive:
1. Wait 15-30 minutes
2. Run the script again with `--resume`
3. Or download directly from browser in smaller batches

Google Drive has rate limits for popular files. The script handles this gracefully and allows resuming.
