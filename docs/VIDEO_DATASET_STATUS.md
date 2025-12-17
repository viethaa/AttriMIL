# Video Dataset Status Report

## Download Status

### ✅ Successfully Downloaded
- **Adenoma Category**: 35 video files (38GB total)
- **Location**: `/Users/vietha/Documents/GitHub/AttriMIL/full_dataset/Adenoma/`
- **File Format**: .avi files
- **File Sizes**: Range from 11MB to 4.4GB per video

### ❌ Missing Categories
- **Malignant**: Not downloaded (connection/permission issues)
- **Normal**: Not downloaded (connection/permission issues)

### Download Issue
The Google Drive download using `gdown` failed partway through due to:
```
Please check connections and permissions.
```

This appears to be either:
1. Google Drive rate limiting
2. File-specific permission restrictions
3. Network connection issues

## Dataset Structure

### Current Structure
```
full_dataset/
└── Adenoma/
    ├── 1.avi (982MB)
    ├── 2.avi (3.6GB)
    ├── 3.avi (1.7GB)
    ├── 4.avi (2.2GB)
    ├── 5.avi (2.0GB)
    ├── 21b8981.avi (1.4GB)
    ├── 24a0125.avi (3.8GB)
    ├── 24a0140.avi (396MB)
    ├── 24a0141.avi (980MB)
    ├── 24a0350.avi (550MB)
    ├── 24a0633.avi (3.1GB)
    ├── 24a0705.avi (472MB)
    ├── 24a0763.avi (4.4GB)
    ├── 24a0986.avi (250MB)
    ├── 24a0987.avi (912MB)
    ├── 24a1140.avi (418MB)
    ├── 24a1522.avi (560MB)
    ├── 24a1676.avi (306MB)
    ├── 24a1680.avi (1.1GB)
    ├── 24a1814.avi (479MB)
    ├── 24a2096.avi (1.1GB)
    ├── 24a2232.avi (537MB)
    ├── 24a2386.avi (45MB)
    ├── 24a2782.avi (11MB)
    ├── 24a2784.avi (17MB)
    ├── 24a2900.avi (19MB)
    ├── 24a3261.avi (89MB)
    ├── 24a4121.avi (305MB)
    ├── 24a4127.avi (570MB)
    ├── 24a4415.avi (641MB)
    ├── 24a4554.avi (550MB)
    ├── 24a5614.avi (1.0GB)
    ├── 24a5759.avi (725MB)
    ├── 24a5913.avi (387MB)
    └── 24a6155.avi (2.7GB)
```

### Expected Complete Structure
```
full_dataset/
├── Adenoma/     ✅ Downloaded (35 files, 38GB)
├── Malignant/   ❌ Missing
└── Normal/      ❌ Missing
```

## Next Steps

### 1. Complete Dataset Download
**Options:**
- **Option A**: Retry download with different tool or method
- **Option B**: Ask user to manually download Malignant/Normal folders
- **Option C**: Proceed with Adenoma-only for initial testing

### 2. Install Required Dependencies
Need to install video processing libraries:
```bash
pip install opencv-python-headless
pip install torch torchvision
# For feature extraction, choose one:
pip install pytorchvideo  # For I3D, SlowFast, X3D
# OR
pip install timm  # For VideoMAE, TimeSformer
```

### 3. Video Analysis
Before feature extraction, need to analyze:
- Frame dimensions (width x height)
- Frame rate (FPS)
- Total frames per video
- Duration
- Color space (RGB/BGR)

### 4. Feature Extraction Pipeline

#### Approach 1: I3D Features (Kinetics-400 pretrained)
- Input: 16-frame clips @ 224x224
- Output: 1024-dim features per clip
- Aggregate clips → bag representation

#### Approach 2: SlowFast Features
- Input: 32 frames (slow) + 8 frames (fast) @ 224x224
- Output: 2048-dim features
- More accurate but slower

#### Approach 3: VideoMAE (Recommended for MIL)
- Input: 16-frame clips @ 224x224
- Output: 768-dim features (matches PHIKON dimension!)
- Self-supervised pretraining on videos
- Better for fine-grained features

### 5. Data Splits
Create pkl files similar to Camelyon16 structure:
```
video_splits/
├── splits_0.csv
└── splits_0_bool.csv
```

Columns:
- `video_id`: filename without extension
- `label`: 0 (Normal), 1 (Adenoma), 2 (Malignant)
- `train`: boolean
- `val`: boolean
- `test`: boolean

### 6. Adapt AttriMIL for Videos

**Key Modifications:**
```python
# Video is the "bag", frames/clips are "instances"
class VideoAttriMIL(nn.Module):
    def __init__(self, feature_dim=768, num_classes=3):
        # Same architecture as image AttriMIL
        # But interpret:
        # - Bag = entire video
        # - Instances = frame/clip features
        # - Spatial constraint → Temporal constraint
```

**Temporal Constraint:**
- Replace 2D spatial masking with 1D temporal masking
- Neighboring frames should have similar attention
- Use temporal consistency loss

### 7. Training Configuration

```python
# Video-specific config
VIDEO_CONFIG = {
    'csv_path': 'video_data/video_total.csv',
    'data_dir': 'video_features/',  # Extracted features
    'split_dir': 'video_splits/',
    'num_classes': 3,  # Normal, Adenoma, Malignant
    'feature_dim': 768,  # If using VideoMAE
    'max_epochs': 150,
    'lr': 2e-4,
    'batch_size': 1,  # One video at a time
}
```

## Estimated Storage Requirements

### Current
- **Downloaded Videos**: 38GB (Adenoma only)

### Full Dataset (estimated)
- **All Videos**: ~100-150GB (assuming similar sizes for other categories)

### Extracted Features (estimated)
- **Per video**: ~1-10MB (depending on video length and sampling rate)
- **Total features**: ~500MB-2GB

## Timeline

1. **Complete download**: TBD (depends on approach chosen)
2. **Install dependencies**: 5-10 minutes
3. **Analyze video properties**: 10-15 minutes
4. **Extract features**: 2-4 hours (GPU) or 8-12 hours (CPU)
5. **Create splits**: 15 minutes
6. **Adapt trainer**: 1-2 hours
7. **Run training**: 2-4 hours for 150 epochs

**Total Estimated Time**: 1-2 days

## Recommendations

1. **Priority**: Complete dataset download
   - Try manual download of Malignant/Normal folders
   - Or use alternative download method (wget, curl, rclone)

2. **For Testing**: Can proceed with Adenoma-only
   - Treat as binary classification (Adenoma vs. combined Normal+Malignant)
   - Or use for proof-of-concept

3. **Feature Extraction**: Recommend VideoMAE
   - 768-dim matches PHIKON (Camelyon16 features)
   - Can reuse exact same AttriMIL architecture
   - Good balance of accuracy and speed

4. **Hardware**: Feature extraction should use GPU if available
   - Check: `python -c "import torch; print(torch.cuda.is_available())"`
   - If no GPU: use CPU but expect slower extraction
