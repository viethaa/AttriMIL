# AttriMIL Codebase Structure

This document describes the organized structure of the AttriMIL codebase.

## Root Directory

Core Python files for training, testing, and data loading:

- `config.py` - Main configuration file
- `config_video.py` - Video-specific configuration
- `constraints.py` - Training constraints
- `coords_to_feature.py` - Coordinate to feature conversion
- `utils.py` - Utility functions

### Trainers
- `trainer_attrimil_abmil.py` - AttriMIL/ABMIL trainer
- `trainer_dsmil.py` - DSMIL trainer
- `trainer_mil.py` - MIL trainer
- `trainer_transmil.py` - TransMIL trainer
- `trainer_video.py` - Video trainer

### Testers
- `tester_attrimil_abmil.py` - AttriMIL/ABMIL tester
- `tester_dsmil.py` - DSMIL tester
- `tester_mil.py` - MIL tester
- `tester_transmil.py` - TransMIL tester

### Data Loaders
- `dataloader.py` - Main data loader
- `dataloader_pkl.py` - PKL format data loader
- `dataloader_video.py` - Video data loader

## Directory Structure

```
.
├── data/                           # All data files
│   ├── camelyon16/                # Camelyon16 dataset
│   ├── features/                  # Extracted features
│   ├── full_dataset/              # Full dataset
│   └── video/                     # Video data
│       ├── video_data/            # Raw video files
│       └── video_panning_data/    # Panning video data
│
├── datasets/                       # Dataset definitions
│
├── docs/                           # Documentation
│   ├── DOWNLOAD_STATUS_UPDATE.md
│   ├── QUICK_START.md
│   ├── RESULTS_SUMMARY.md
│   ├── SESSION_SUMMARY.md
│   ├── SUPERVISOR_REPORT.md
│   ├── TRAINING_GUIDE.md
│   ├── VIDEO_DATASET_STATUS.md
│   └── VIDEO_PROJECT_SUMMARY.md
│
├── models/                         # Model definitions
│
├── results/                        # Training results and outputs
│   ├── models/                    # Saved model weights
│   └── training/                  # Training logs and metrics
│       ├── accuracy_table.txt
│       ├── complete_training_results.csv
│       ├── training_results.csv
│       ├── training_summary.csv
│       └── ...
│
├── scripts/                        # Utility scripts
│   ├── data_processing/           # Data preparation scripts
│   │   ├── create_3coords.py
│   │   ├── create_better_splits.py
│   │   ├── create_splits_pkl.py
│   │   ├── convert_hf_to_attrimil.py
│   │   ├── download_camelyon16_features.py
│   │   ├── download_remaining_videos.py
│   │   ├── extract_video_features.py
│   │   └── prepare_video_dataset.py
│   │
│   ├── results_extraction/        # Results processing scripts
│   │   ├── extract_accuracy.py
│   │   ├── extract_metrics.py
│   │   └── extract_training_results.py
│   │
│   └── utils/                     # Miscellaneous utilities
│       ├── check_downloaded_data.py
│       ├── download_missing_videos.sh
│       ├── fix_csv.py
│       └── inspect_features_detail.py
│
└── visualization/                  # Visualization code
```

## Quick Navigation

- **Training a model**: Use `trainer_*.py` files in root directory
- **Testing a model**: Use `tester_*.py` files in root directory
- **Data preparation**: Check `scripts/data_processing/`
- **Results analysis**: Check `scripts/results_extraction/`
- **Documentation**: Check `docs/`
- **Saved models**: Check `results/models/`
- **Training logs**: Check `results/training/`
