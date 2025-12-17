# AttriMIL Training Results - Video Panning Classification

## Dataset Information
- **Task**: 3-class video panning classification (Adenoma subtypes)
- **Total Patients**: 75 (25 per class)
- **Total Images**: 4,565 video frames
- **Features**: 512-dim pre-extracted features (.pkl files)
- **Classes**:
  - Class 0: Adenoma type 1
  - Class 1: Adenoma type 2 (Malignant)
  - Class 2: Adenoma type 3 (Normal)

## Data Split
- **Training**: 45 patients (15 per class, 2,860 images)
- **Validation**: 15 patients (5 per class, 914 images)
- **Test**: 15 patients (5 per class, 791 images)

## Model Configuration
- **Architecture**: AttriMIL (Attention-based MIL)
- **Parameters**: 1,053,193 trainable parameters
- **Optimizer**: Adam (lr=2e-4, weight_decay=1e-4)
- **Loss**: Cross-entropy + Spatial constraint + Ranking constraint
  - Spatial loss weight: 1.0
  - Ranking loss weight: 5.0
- **Training**: 200 max epochs, early stopping (patience=50)

## Final Results

### Test Set Performance
- **Test AUC**: **88.67%**
- **Test Accuracy**: **73.33%** (11/15 correct)
- **Test Error**: 26.67%

### Per-Class Results (Test Set)
| Class | Accuracy | Correct/Total |
|-------|----------|---------------|
| Class 0 (Adenoma type 1) | 80% | 4/5 |
| Class 1 (Malignant) | 80% | 4/5 |
| Class 2 (Normal) | 60% | 3/5 |

### Best Validation Performance (Epoch 20)
- **Val AUC**: **98.00%**
- **Val Loss**: 0.3397
- **Val Error**: 13.33% (2/15 wrong)
- **Val Accuracy**: 86.67%

### Training Performance (Best Epoch)
- **Train Loss**: 0.0209
- **Train Error**: 0% (perfect fit on training data)
- **Train Accuracy**: 100%

## Key Observations

1. **Strong Validation Performance**: 98% AUC on validation set indicates the model learned meaningful patterns

2. **Test Performance**: 88.67% AUC is good for a small dataset (75 patients total)

3. **Overfitting Present**: 100% train accuracy vs 73% test accuracy shows overfitting, but this is expected with:
   - Small dataset (only 75 patients)
   - 1M+ parameters
   - Limited regularization

4. **Class Balance**: Relatively balanced per-class performance (60-80% accuracy)

5. **Reliability**: Results are now more reliable with 15 test patients vs previous 6

## Comparison to Previous Run

| Metric | Previous (6 test) | Current (15 test) | Improvement |
|--------|-------------------|-------------------|-------------|
| Test AUC | 79.17% | **88.67%** | +9.5% |
| Test Accuracy | 66.67% | **73.33%** | +6.7% |
| Class 0 Acc | 0% | **80%** | +80% |
| Statistical Reliability | Low (n=6) | **Higher (n=15)** | ✓ |

## Saved Model
- **Location**: `./results_video/s_0_checkpoint.pt`
- **Best Epoch**: 20
- **Criterion**: Lowest validation loss

## Training Log
- **Full log**: `training_better_split.log`
- **Total epochs trained**: 71 (stopped early)
- **Training time**: ~15 minutes

---

**Generated**: 2025-12-06
**Model**: AttriMIL
**Dataset**: Video Panning Classification (75 patients)
