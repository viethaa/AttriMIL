# Video AttriMIL Project - Current Status

## Overview
This document summarizes the current status of adapting AttriMIL for video classification using colonoscopy/endoscopy video data.

---

## ✅ Completed Tasks

### 1. Dataset Download (Partial)
- **Status**: ✅ Partially complete
- **Downloaded**: 35 Adenoma videos (38GB)
- **Missing**: Malignant and Normal categories
- **Reason**: Google Drive download failed due to permission/connection issues on file ID `1PaFfLtoReYDdS0YAkFhe884tqx2IYbPg`

### 2. Dataset Preparation
- **Status**: ✅ Complete
- **Location**: `video_data/`
- **Files Created**:
  - `video_dataset.csv` - Full dataset metadata (35 videos)
  - `splits/splits_0.csv` - Train/val/test splits
  - `dataset_report.txt` - Detailed statistics
  - `NEXT_STEPS.md` - Guide for next steps

**Split Distribution:**
- Training: 21 videos (60%)
- Validation: 7 videos (20%)
- Test: 7 videos (20%)

### 3. Feature Extraction Script
- **Status**: ✅ Created
- **File**: `extract_video_features.py`
- **Model**: ResNet50 pretrained on ImageNet
- **Features**: 2048-dimensional per frame
- **Sampling**: Configurable frame sampling rate

---

## ⏳ In Progress

### Extract Features from Videos
**Command to run:**
```bash
python extract_video_features.py \
    --data_root full_dataset \
    --csv_file video_data/video_dataset.csv \
    --output_dir video_features \
    --sample_rate 30 \
    --device auto
```

**Expected Output:**
- `video_features/` directory
- One `.pt` file per video containing frame features
- `extraction_info.csv` with statistics

**Estimated Time:**
- ~1-2 minutes per video on MPS (Apple Silicon GPU)
- Total: ~35-70 minutes for 35 videos

---

## 📋 Pending Tasks

### 1. Complete Dataset Download
**Options:**
- **A. Manual download**: User manually downloads Malignant and Normal folders from Google Drive
- **B. Alternative tool**: Try different download method (wget, curl, rclone, browser download)
- **C. Request access**: Ask dataset owner for direct access or different sharing method
- **D. Proceed with Adenoma only**: Use as proof-of-concept, binary classification against combined others

**Google Drive Folder**: https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN

### 2. Adapt AttriMIL Trainer for Videos
**Changes needed in training code:**

```python
# Key modifications needed:
# 1. Dataloader - load .pt files instead of .h5
# 2. Model input - 2048-dim instead of 768-dim (if using ResNet50)
#    OR keep 768-dim by using different feature extractor
# 3. Temporal constraint - replace spatial with temporal
# 4. Multi-class - 3 classes instead of 2
```

**Specific files to modify:**
- `dataloader_pkl.py` → Create `dataloader_video.py`
  - Load `.pt` files from `video_features/` instead of `.h5` from Camelyon16
  - Handle video IDs instead of slide IDs

- `constraints.py`
  - Replace 2D spatial masking with 1D temporal masking
  - Neighboring frames should have similar attention weights

- `trainer_attrimil_abmil.py` → Create `trainer_video.py`
  - Update configuration:
    ```python
    CONFIG = {
        'csv_path': 'video_data/video_dataset.csv',
        'data_dir': 'video_features/',
        'split_dir': 'video_data/splits/',
        'num_classes': 3,  # Or 1 if binary (Adenoma only)
        'feature_dim': 2048,  # ResNet50 features
        'max_epochs': 150,
        'lr': 2e-4,
    }
    ```
  - Adjust model architecture for different feature dimension
  - Update metrics for multi-class classification

### 3. Run Training
After adapting the trainer:
```bash
python trainer_video.py
```

**Expected Results:**
- Training curves similar to Camelyon16 results
- AUC and accuracy metrics
- Model checkpoints in `save_weights/video_attrimil/`

---

## 📊 Current Dataset Statistics

### Downloaded (Adenoma only)
```
Total videos: 35
Total size: 38GB
Category distribution:
  - Adenoma: 35 videos

File sizes range: 11MB - 4.4GB per video

Sample files:
  - 1.avi (982MB)
  - 2.avi (3.6GB)
  - 3.avi (1.7GB)
  - 24a0763.avi (4.4GB) - largest
  - 24a2782.avi (11MB) - smallest
```

### Expected (Complete Dataset)
```
Total videos: ~100-200 (estimated)
Total size: ~100-150GB (estimated)
Categories:
  - Normal: ? videos
  - Adenoma: 35 videos ✓
  - Malignant: ? videos
```

---

## 🔧 Technical Details

### Hardware
- **Device**: Apple Silicon (MPS available)
- **PyTorch**: 2.9.1
- **GPU Acceleration**: Yes (MPS)

### Model Architecture (Current)
```
Video → Frame Sampling → ResNet50 Feature Extractor → 2048-dim features/frame
   ↓
Multiple frames → "Bag" representation
Each frame → "Instance" in MIL terminology
   ↓
AttriMIL Model:
  - Attention mechanism (same as WSI)
  - Temporal constraint (instead of spatial)
  - Ranking constraint (same as WSI)
   ↓
Video-level classification
```

### Alternative Feature Extractors
If 768-dim features preferred (to match PHIKON):
- **Option 1**: Add linear projection 2048 → 768
- **Option 2**: Use ViT-Base encoder (768-dim native)
- **Option 3**: Use VideoMAE (768-dim, video-specific pretraining)

---

## 📁 Project Structure

```
AttriMIL/
├── full_dataset/
│   ├── Adenoma/              ✓ 35 videos (38GB)
│   ├── Malignant/            ✗ Missing
│   └── Normal/               ✗ Missing
│
├── video_data/               ✓ Created
│   ├── video_dataset.csv
│   ├── dataset_report.txt
│   ├── NEXT_STEPS.md
│   └── splits/
│       └── splits_0.csv
│
├── video_features/           ⏳ To be created
│   ├── 1.pt
│   ├── 2.pt
│   ├── ...
│   └── extraction_info.csv
│
├── Scripts:
│   ├── prepare_video_dataset.py      ✓ Created & ran
│   ├── extract_video_features.py     ✓ Created
│   ├── dataloader_video.py           ⏳ To be created
│   └── trainer_video.py              ⏳ To be created
│
└── Documentation:
    ├── VIDEO_DATASET_STATUS.md       ✓ Created
    ├── VIDEO_PROJECT_SUMMARY.md      ✓ This file
    └── TRAINING_GUIDE.md             (From previous work)
```

---

## 🚀 Recommended Next Steps

### Immediate (Today)
1. **Run feature extraction**:
   ```bash
   python extract_video_features.py
   ```
   - This will take ~1 hour
   - Creates `video_features/` directory with .pt files

2. **Create video dataloader**:
   - Copy `dataloader_pkl.py` → `dataloader_video.py`
   - Modify to load .pt files
   - Test with one video

### Short-term (This Week)
3. **Adapt trainer**:
   - Copy `trainer_attrimil_abmil.py` → `trainer_video.py`
   - Update configuration for video features
   - Modify temporal constraint
   - Adjust for 2048-dim features

4. **Run initial training**:
   - Train on Adenoma-only (binary: is_adenoma vs not)
   - Validate the pipeline works
   - Check convergence and metrics

### Medium-term
5. **Complete dataset**:
   - Obtain Malignant and Normal videos
   - Re-run preparation and extraction
   - Train full 3-class model

6. **Optimize**:
   - Try different feature extractors (VideoMAE, etc.)
   - Tune hyperparameters
   - Compare with baseline methods

---

## 💡 Design Decisions

### Why ResNet50 for Feature Extraction?
- ✅ Proven on medical images
- ✅ Pretrained on ImageNet (good general features)
- ✅ Fast inference
- ✅ 2048-dim features (good representation power)
- ⚠️ Not video-specific (no temporal modeling in features)

**Alternative**: VideoMAE
- ✅ Video-specific pretraining
- ✅ 768-dim (matches PHIKON)
- ✅ Self-supervised (good for medical domain)
- ⚠️ Slower inference
- ⚠️ Requires more GPU memory

### Why Frame Sampling at 1 FPS?
- ✅ Reduces redundancy (videos at 30 fps have very similar adjacent frames)
- ✅ Manageable bag sizes for MIL
- ✅ Faster feature extraction
- ⚠️ May miss brief abnormalities
- **Adjustable**: Can change `--sample_rate` parameter

### Why 2048-dim Features?
- ✅ ResNet50 native output
- ✅ Rich representation
- ⚠️ Different from PHIKON's 768-dim
- **Solution**: AttriMIL can handle any dimension, just update `feature_dim` config

---

## 🎯 Success Metrics

### Minimum Viable (Adenoma-only)
- [ ] Feature extraction completes successfully
- [ ] Training converges (loss decreases)
- [ ] Validation AUC > 0.7
- [ ] Can classify Adenoma videos

### Target (Full Dataset)
- [ ] All 3 categories downloaded and processed
- [ ] Balanced train/val/test splits across all classes
- [ ] Validation AUC > 0.85
- [ ] Per-class accuracy > 80%
- [ ] Comparable to published baselines on this dataset

---

## 📝 Notes

### Known Limitations
1. **Incomplete dataset**: Only Adenoma videos available
2. **Frame-level features**: Not using temporal models (I3D, SlowFast, etc.)
3. **No video-specific augmentations**: Using image-pretrained models

### Future Improvements
1. **Temporal modeling**: Use video transformers (VideoMAE, TimeSformer)
2. **Data augmentation**: Video-specific augmentations (temporal cropping, speed variation)
3. **Multi-scale features**: Extract features at different temporal resolutions
4. **Attention visualization**: Visualize which frames the model attends to

---

## 🐛 Troubleshooting

### If feature extraction fails:
```bash
# Check video can be read:
python -c "import cv2; cap = cv2.VideoCapture('full_dataset/Adenoma/1.avi'); print(cap.isOpened())"

# Try with smaller sample:
python extract_video_features.py --max_frames 10

# Use CPU if GPU fails:
python extract_video_features.py --device cpu
```

### If dataset download needed:
```bash
# Try individual file download:
gdown FILE_ID -O output_filename.avi

# Or use browser download and place in correct folders
```

---

## 📚 References

- **AttriMIL Paper**: (Original paper on histopathology WSI)
- **Camelyon16 Dataset**: Breast cancer metastases detection
- **Video MIL**: Videos as bags, frames as instances
- **Medical Video Analysis**: Colonoscopy polyp detection literature

---

*Last Updated: 2025-12-13*
*Status: Feature extraction ready, awaiting execution*
