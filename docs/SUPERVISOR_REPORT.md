# Training Report: AttriMIL on Video Panning Classification

**Date**: December 6, 2025
**Model**: AttriMIL (Attention-based Multiple Instance Learning)
**Dataset**: Video Panning Classification (Adenoma subtypes)

---

## Executive Summary

Successfully trained AttriMIL on a 75-patient video classification dataset, achieving **88.67% test AUC** and **98% validation AUC**. Results demonstrate the model can learn meaningful patterns for 3-class Adenoma classification, though overfitting remains a challenge due to the small dataset size.

---

## Current Results

### Dataset
- **Total**: 75 patients (25 per class)
- **Features**: 4,565 pre-extracted 512-dim video features (.pkl files)
- **Split**: 45 train / 15 val / 15 test patients
- **Classes**: 3-class Adenoma classification (types 0, 1, 2)

### Performance Metrics

| Metric | Validation (Best) | Test (Final) |
|--------|-------------------|--------------|
| **AUC** | **98.00%** | **88.67%** |
| **Accuracy** | 86.67% | 73.33% |
| **Best Epoch** | 19 | - |

### Per-Class Test Accuracy
- **Class 0** (Adenoma type 1): 80% (4/5 correct)
- **Class 1** (Malignant): 80% (4/5 correct)
- **Class 2** (Normal): 60% (3/5 correct)

---

## Key Observations

### ✅ Strengths
1. **High validation AUC (98%)** indicates the model learned discriminative features
2. **Balanced per-class performance** (60-80%) shows no severe class bias
3. **Stable validation performance** from epoch 12-70 suggests convergence
4. **Reproducible results** with proper train/val/test split

### ⚠️ Limitations
1. **Severe overfitting**:
   - Training accuracy: 100% (epoch 16+)
   - Test accuracy: 73.33%
   - Gap indicates poor generalization

2. **Small dataset size**:
   - Only 75 patients total
   - Test set (15 patients) has limited statistical power
   - Model has 1M+ parameters, ideal for thousands of samples

3. **Validation-test gap**:
   - Validation AUC: 98%
   - Test AUC: 88.67%
   - 9.3% drop suggests possible data split issues or small test set variance

---

## Root Causes Analysis

| Issue | Cause | Impact |
|-------|-------|--------|
| Overfitting | 1M parameters vs 45 training bags | Train acc → 100%, test → 73% |
| Dataset size | Only 75 patients available | High variance, unreliable metrics |
| No regularization | Dropout disabled, minimal weight decay | Model memorizes training data |
| Class 2 underperformance | Possible: harder to classify or data imbalance | 60% vs 80% for other classes |

---

## Action Plan for Improvement

### 🎯 Priority 1: Access Full Dataset (IMMEDIATE)
**Current blocker**: Need access to `/mnt/disk4/video-panninng-classification/`

**Required actions**:
1. Mount disk4 on aiotlab server (needs sudo password)
2. Verify full dataset size (supervisor mentioned "full data on disk 4")
3. Download and prepare complete dataset

**Expected impact**:
- More training data → less overfitting
- Larger test set → more reliable metrics
- Better statistical power

**Timeline**: 1-2 days (pending disk access)

---

### 🔧 Priority 2: Add Regularization (QUICK WIN)

**Immediate improvements** (can do with current 75-patient dataset):

1. **Dropout regularization** (1 hour)
   - Add dropout=0.5 to model layers
   - Expected: 5-10% improvement in test accuracy

2. **Stronger weight decay** (30 min)
   - Increase from 1e-4 to 1e-3
   - Expected: reduce overfitting

3. **Data augmentation** (2 hours)
   - Feature-level noise injection
   - Random feature dropout during training
   - Expected: better generalization

4. **Early stopping on test AUC** (30 min)
   - Currently stops on validation loss
   - Switch to validation AUC monitoring
   - Expected: prevent overfitting to validation set

**Timeline**: 1 day of experimentation

---

### 📊 Priority 3: Cross-Validation (RECOMMENDED)

**Current limitation**: Single train/val/test split may not be representative

**Proposed approach**:
- 5-fold cross-validation
- Each fold: 60 train / 15 test
- Report mean ± std across folds

**Expected benefits**:
- More robust performance estimates
- Confidence intervals for metrics
- Better understanding of model stability

**Timeline**: 2 days (5x longer training)

---

### 🚀 Priority 4: Model Architecture Exploration

**Current**: AttriMIL with 1M parameters (potentially too large)

**Alternatives to test**:
1. **Smaller AttriMIL**: Reduce hidden dimensions (512→256)
2. **ABMIL baseline**: Standard attention-based MIL (simpler)
3. **TransMIL**: Transformer-based MIL (state-of-art)
4. **Feature ensemble**: Train multiple models, ensemble predictions

**Timeline**: 1 week for comprehensive comparison

---

## Recommended Next Steps (Prioritized)

### Week 1: Data & Quick Improvements
1. ✅ **Day 1-2**: Get disk4 access, download full dataset
2. 🔧 **Day 3**: Add regularization (dropout + weight decay)
3. 📊 **Day 4-5**: Re-train with improvements, compare results

### Week 2: Robust Evaluation
4. 📊 **Day 6-10**: 5-fold cross-validation on full dataset
5. 📈 **Day 11-12**: Analyze results, write detailed report

### Week 3+: Advanced Exploration (if needed)
6. 🚀 **Optional**: Model architecture comparison
7. 🎯 **Optional**: Hyperparameter tuning (learning rate, loss weights)

---

## Expected Outcomes

### With current 75-patient dataset + regularization:
- **Test AUC**: 88% → 90-92% (optimistic)
- **Overfitting**: Reduced but still present
- **Confidence**: Low (small dataset)

### With full dataset (assuming 200+ patients):
- **Test AUC**: 92-95% (realistic target)
- **Overfitting**: Significantly reduced
- **Confidence**: High (proper statistical power)
- **Publication-ready**: Yes

---

## Questions for Supervisor

1. **Disk4 access**: Can you provide sudo password or mount `/mnt/disk4/` for us?
   - Expected path: `/mnt/disk4/video-panninng-classification/datasets/`
   - Need to verify actual size of full dataset

2. **Timeline expectations**:
   - Is 2-3 weeks acceptable for comprehensive experiments?
   - Or prioritize quick results with current 75-patient dataset?

3. **Performance targets**:
   - What AUC/accuracy is considered "good enough" for this task?
   - Are we aiming for publication or internal use?

4. **Resource availability**:
   - Can we use GPU server for longer training runs?
   - Any computational budget constraints?

---

## Conclusion

The current results (**88.67% test AUC, 98% validation AUC**) demonstrate that AttriMIL successfully learns from video features for Adenoma classification. However, the **small dataset (75 patients)** and resulting **severe overfitting** limit the model's practical utility.

**Critical next step**: Access the full dataset on disk4 to:
- ✅ Train on larger sample size
- ✅ Reduce overfitting through more data
- ✅ Obtain statistically reliable test results
- ✅ Achieve publication-quality performance

**Quick wins** (while waiting for disk4 access):
- Add dropout regularization
- Implement cross-validation
- Optimize hyperparameters

**Bottom line**: We have a working baseline. With the full dataset and proper regularization, we can realistically achieve 92-95% test AUC.

---

**Prepared by**: [Your name]
**Contact**: [Your email]
**Next update**: After disk4 access secured
