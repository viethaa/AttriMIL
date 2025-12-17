# Video AttriMIL - Quick Start Guide

## Current Status: Ready for Feature Extraction

---

## What's Been Done ✅

1. **Downloaded 35 Adenoma videos** (38GB) from Google Drive
2. **Created train/val/test splits**: 21/7/7 videos
3. **Prepared dataset metadata**: `video_data/video_dataset.csv`
4. **Created feature extraction script**: `extract_video_features.py`

---

## What's Missing ⚠️

- **Malignant videos**: Not downloaded (Google Drive permission/connection issue)
- **Normal videos**: Not downloaded (Google Drive permission/connection issue)

The download failed on file ID `1PaFfLtoReYDdS0YAkFhe884tqx2IYbPg` with:
```
Please check connections and permissions.
```

**Options to fix:**
1. Manually download from: https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN
2. Continue with Adenoma-only for now (proof-of-concept)

---

## Next Steps (In Order)

### Step 1: Extract Features (Ready Now!)

```bash
# This will take ~1 hour for 35 videos
python extract_video_features.py \
    --data_root full_dataset \
    --csv_file video_data/video_dataset.csv \
    --output_dir video_features \
    --sample_rate 30 \
    --device auto
```

**What this does:**
- Samples 1 frame per second from each video
- Extracts 2048-dim ResNet50 features per frame
- Saves features as `.pt` files in `video_features/`
- Creates `video_features/extraction_info.csv` with stats

**Expected output:**
- 35 `.pt` files (one per video)
- Each file contains tensor of shape `(num_frames, 2048)`
- Smaller videos: ~200-500 frames
- Larger videos: ~1000-3000 frames

---

### Step 2: Create Video Dataloader

Copy and modify the dataloader:

```bash
cp dataloader_pkl.py dataloader_video.py
```

**Key changes needed:**
1. Load `.pt` files instead of `.h5` files
2. Handle video IDs instead of slide IDs
3. Read from `video_features/` directory

**Example code:**
```python
# In dataloader_video.py
def load_video_features(video_id, features_dir):
    feature_path = Path(features_dir) / f"{video_id}.pt"
    features = torch.load(feature_path)
    return features  # Shape: (num_frames, 2048)
```

---

### Step 3: Adapt AttriMIL Trainer

Copy and modify the trainer:

```bash
cp trainer_attrimil_abmil.py trainer_video.py
```

**Key changes:**

```python
# Update configuration
CONFIG = {
    'csv_path': 'video_data/video_dataset.csv',
    'data_dir': 'video_features/',
    'split_dir': 'video_data/splits/',
    'num_classes': 1,  # Binary for now (Adenoma only)
    'feature_dim': 2048,  # ResNet50 features
    'max_epochs': 150,
    'lr': 2e-4,
}

# Update model initialization
model = AttriMIL(
    feature_dim=2048,  # Changed from 768
    num_classes=1,  # Binary classification
)
```

**Temporal constraint modification:**
```python
# In constraints.py or trainer
# Replace 2D spatial constraint with 1D temporal constraint
# Instead of: neighboring patches in 2D grid
# Now: neighboring frames in temporal sequence
```

---

### Step 4: Run Training

```bash
python trainer_video.py
```

**Monitor:**
- Training loss should decrease
- Validation AUC should increase
- Expect ~100 epochs to converge (similar to Camelyon16 results)

---

## Detailed Documentation

- **`VIDEO_PROJECT_SUMMARY.md`**: Complete project overview with technical details
- **`VIDEO_DATASET_STATUS.md`**: Dataset download status and structure
- **`video_data/NEXT_STEPS.md`**: Step-by-step guide for next tasks
- **`video_data/dataset_report.txt`**: Dataset statistics

---

## Troubleshooting

### Feature extraction fails?
```bash
# Test with one video first:
python extract_video_features.py --max_frames 10

# Try CPU if GPU fails:
python extract_video_features.py --device cpu
```

### Out of memory during training?
```python
# In trainer_video.py, reduce batch size or max frames:
CONFIG = {
    ...
    'max_frames_per_video': 500,  # Limit frames
    'sample_frames': True,  # Subsample if needed
}
```

### Need full dataset?
- Download Malignant and Normal folders manually
- Place in `full_dataset/Malignant/` and `full_dataset/Normal/`
- Re-run: `python prepare_video_dataset.py`
- Re-run: `python extract_video_features.py`
- Update `num_classes=3` in trainer config

---

## Expected Timeline

| Task | Time |
|------|------|
| Feature extraction (35 videos) | ~1 hour |
| Create video dataloader | ~30 min |
| Adapt trainer | ~1-2 hours |
| Initial training (150 epochs) | ~2-3 hours |
| **Total** | **~5-7 hours** |

---

## Hardware Requirements

- **Storage**: ~40GB for videos + ~1GB for features
- **RAM**: 8GB minimum (16GB recommended)
- **GPU**: Optional but recommended (MPS/CUDA)
  - Feature extraction: 10x faster with GPU
  - Training: 5x faster with GPU

---

## Quick Commands Cheat Sheet

```bash
# 1. Extract features (RUN THIS FIRST!)
python extract_video_features.py

# 2. Check extraction results
ls -lh video_features/
head video_features/extraction_info.csv

# 3. Test dataloader (after creating dataloader_video.py)
python -c "from dataloader_video import VideoDataset; ds = VideoDataset('video_data/video_dataset.csv'); print(len(ds))"

# 4. Train model (after creating trainer_video.py)
python trainer_video.py

# 5. Monitor training
tail -f save_weights/video_attrimil/training.log
```

---

## Current File Structure

```
AttriMIL/
├── full_dataset/
│   └── Adenoma/              # ✅ 35 videos (38GB)
│
├── video_data/               # ✅ Created
│   ├── video_dataset.csv     # Dataset metadata
│   └── splits/
│       └── splits_0.csv      # Train/val/test splits
│
├── video_features/           # ⏳ Will be created
│   └── *.pt                  # After running extract_video_features.py
│
├── extract_video_features.py # ✅ Ready to run
├── prepare_video_dataset.py  # ✅ Already ran
│
├── dataloader_video.py       # ⏳ To be created (from dataloader_pkl.py)
└── trainer_video.py          # ⏳ To be created (from trainer_attrimil_abmil.py)
```

---

## Success Criteria

### Minimum (Adenoma-only)
- [ ] Feature extraction completes without errors
- [ ] Training loss decreases consistently
- [ ] Validation AUC > 0.70
- [ ] Model can distinguish Adenoma videos

### Ideal (Full dataset when available)
- [ ] 3-class classification (Normal/Adenoma/Malignant)
- [ ] Validation AUC > 0.85
- [ ] Balanced performance across all classes

---

**Ready to proceed?**

Run: `python extract_video_features.py`

This will create the features needed for training. Then proceed with Steps 2-4.

---

*Generated: 2025-12-13*
*Version: v1.0*
