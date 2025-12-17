# Video Dataset Download - Status Update

**Date**: December 13, 2025
**Issue**: Google Drive Download Quota Limit

---

## Current Download Status

### ✅ Successfully Downloaded

| Category | Videos | Total Size | Status |
|----------|--------|------------|--------|
| Adenoma | 35 | 38GB | ✅ Complete |
| Malignant | 1 | 1.0GB | ⚠️ Partial (quota blocked) |
| Normal | 0 | 0GB | ❌ Blocked |

**Total**: 36 videos, ~39GB

---

## What Happened

### Google Drive Quota Limitation

When attempting to download the Malignant and Normal folders, Google Drive blocked further downloads with this message:

```
Too many users have viewed or downloaded this file recently. Please
try accessing the file again later. If the file you are trying to
access is particularly large or is shared with many people, it may
take up to 24 hours to be able to view or download the file.
```

**This is a common Google Drive limitation for:**
- Popular/frequently accessed files
- Large files
- Files shared with many people
- Multiple consecutive downloads from the same IP

### What Downloaded

**Malignant folder:**
- ✅ 10.avi (1.0GB) - Successfully downloaded
- ❌ 11.avi, 12.avi, 13.avi, ... (40+ files) - Blocked

**Normal folder:**
- ❌ All files blocked (didn't even start)

**Adenoma folder:**
- ✅ All 35 files downloaded earlier (38GB total)

---

## Options to Proceed

### Option 1: Manual Browser Download (Recommended)

**Steps:**
1. Open the Google Drive links in your browser:
   - Malignant: https://drive.google.com/drive/folders/1A5zcNdl5klKXx_u7MRv2SrjqY_p_pLsf
   - Normal: https://drive.google.com/drive/folders/18yl_eoj2Kd0EnuWJVhbFtRfyqfFAg8fT

2. Select all files → Right-click → Download
   (Or use "Download all" from folder menu)

3. Place downloaded files in:
   ```
   full_dataset/Malignant/  (malignant videos)
   full_dataset/Normal/     (normal videos)
   ```

4. Re-run preparation:
   ```bash
   python prepare_video_dataset.py
   python extract_video_features.py
   ```

**Pros:**
- Bypasses gdown quota limits
- Usually works better for large downloads
- Can download in batches

**Cons:**
- Manual process
- May need to unzip/organize files

---

### Option 2: Wait and Retry (24 hours)

**Steps:**
1. Wait 24 hours for Google Drive quota to reset
2. Re-run download script:
   ```bash
   gdown --folder https://drive.google.com/drive/folders/1A5zcNdl5klKXx_u7MRv2SrjqY_p_pLsf \
         -O full_dataset/Malignant --remaining-ok

   gdown --folder https://drive.google.com/drive/folders/18yl_eoj2Kd0EnuWJVhbFtRfyqfFAg8fT \
         -O full_dataset/Normal --remaining-ok
   ```

**Pros:**
- Automated
- No manual work

**Cons:**
- Must wait 24 hours
- May still hit quotas if popular dataset

---

### Option 3: Proceed with Adenoma-Only (Fastest)

**Steps:**
1. Use existing 35 Adenoma videos for proof-of-concept
2. Run feature extraction:
   ```bash
   python extract_video_features.py
   ```
3. Create binary classification trainer (Adenoma vs. not-Adenoma)
4. Train and validate the pipeline

**Pros:**
- Can start immediately
- Tests the full pipeline
- 35 videos is reasonable for initial testing

**Cons:**
- Only 1 class (no multi-class classification)
- Can't evaluate full model performance
- Will need to retrain with full dataset later

**Recommendation**: Do this first while waiting for full dataset

---

### Option 4: Alternative Download Methods

**A. Using rclone (Google Drive integration):**
```bash
# Install rclone
brew install rclone

# Configure Google Drive
rclone config

# Download folders
rclone copy "gdrive:folder_name" full_dataset/Malignant/
```

**B. Using wget with cookies:**
1. Login to Google Drive in browser
2. Export cookies
3. Use wget with cookie file

**C. Contact Dataset Owner:**
- Request alternative sharing method
- Ask for direct download link
- Request increased quota

---

##My Recommendation

**Best Approach: Combination**

1. **Immediate (Today):**
   - ✅ Proceed with Adenoma-only dataset (35 videos)
   - ✅ Run feature extraction
   - ✅ Create and test video dataloader
   - ✅ Adapt trainer for video features
   - ✅ Run initial training

2. **Short-term (This Week):**
   - Manual browser download of Malignant + Normal folders
   - OR wait 24h and retry automated download
   - Re-run preparation with full dataset
   - Train 3-class model

3. **Why this approach:**
   - Don't wait idly - validate pipeline works
   - Get initial results with Adenoma
   - Complete dataset download in parallel
   - Minimal time wasted

---

## Commands to Proceed Now

```bash
# 1. Check current dataset
ls -lh full_dataset/*/
# Output: Adenoma (35 files), Malignant (1 file), Normal (0 files)

# 2. Update dataset preparation (with current files)
python prepare_video_dataset.py

# 3. Extract features (will take ~1-2 hours)
python extract_video_features.py \
    --data_root full_dataset \
    --csv_file video_data/video_dataset.csv \
    --output_dir video_features \
    --sample_rate 30

# 4. Continue with dataloader and trainer creation
```

---

## Expected Results with Adenoma-Only

**Dataset Split:**
- Train: ~21 Adenoma videos
- Val: ~7 Adenoma videos
- Test: ~7 Adenoma videos

**Classification Task:**
- Binary: Is this an Adenoma video? (Yes/No)
- Can still test:
  - Feature extraction pipeline
  - Dataloader
  - AttriMIL model
  - Training loop
  - Attention mechanism
  - Temporal constraints

**Metrics:**
- Training loss, accuracy
- Validation AUC, accuracy
- Model convergence
- Attention visualizations

---

## When Full Dataset Available

**Re-run these steps:**

```bash
# 1. Prepare full dataset
python prepare_video_dataset.py
# Will create new splits with all 3 categories

# 2. Extract features from new videos
python extract_video_features.py
# Will only process new Malignant + Normal videos

# 3. Update trainer config
# Change num_classes: 1 → 3

# 4. Re-train with 3-class classification
python trainer_video.py
```

---

## File Locations

```
Current State:
full_dataset/
├── Adenoma/     [35 files, 38GB] ✅
├── Malignant/   [1 file, 1GB] ⚠️ (only 10.avi)
└── Normal/      [0 files] ❌

Target State:
full_dataset/
├── Adenoma/     [~35 files] ✅
├── Malignant/   [~40 files] ⏳
└── Normal/      [~50 files] ⏳
```

---

## Next Steps

### Immediate Actions (Choose One):

**A. Proceed with Adenoma (Recommended):**
```bash
python prepare_video_dataset.py
python extract_video_features.py
```

**B. Manual Download First:**
1. Download Malignant + Normal from browser
2. Place in respective folders
3. Run prepare + extract

**C. Wait 24h:**
- Come back tomorrow
- Retry automated download

---

## Technical Notes

### Why Quota Limits Exist

Google Drive implements quotas to:
- Prevent abuse
- Manage bandwidth
- Ensure fair usage
- Protect against bots

### Typical Limits

- ~15-50 files per folder per day (varies)
- ~750 MB - 10GB per day per IP (varies)
- Shared files have lower limits
- Can reset after 24 hours

### Best Practices

- Download in smaller batches
- Use delays between downloads
- Authenticate with Google account (higher limits)
- Use alternative methods for large datasets
- Contact owner for direct access

---

## Summary

- **Downloaded**: 36/~125 videos (29%)
- **Blocked By**: Google Drive quota limits
- **Workaround**: Manual download or wait 24h
- **Current Capability**: Can proceed with Adenoma-only
- **Recommendation**: Start with Adenoma while downloading full dataset

---

**Status**: Ready to proceed with feature extraction on available videos
**Blocker**: Google Drive quota (for complete dataset)
**Action**: Your choice of Option 1, 2, or 3 above

---

*Generated: 2025-12-13*
*Last Updated: After encountering Google Drive quota*
