# Next Steps for Video AttriMIL

## 1. Install Dependencies

```bash
pip install opencv-python-headless
pip install torch torchvision
pip install timm  # For video transformers
```

## 2. Extract Video Features

You need to extract features from the videos before training.

Options:
- **I3D** (Kinetics-400 pretrained): 1024-dim features
- **SlowFast**: 2048-dim features
- **VideoMAE** (Recommended): 768-dim features (matches PHIKON!)

## 3. Create Feature Extraction Script

See `extract_video_features.py` (to be created)

## 4. Adapt AttriMIL Trainer

Modify trainer to:
- Load video features instead of WSI features
- Replace spatial constraint with temporal constraint
- Adjust for multi-class classification (3 classes)

## 5. Run Training

```bash
python trainer_video.py
```
