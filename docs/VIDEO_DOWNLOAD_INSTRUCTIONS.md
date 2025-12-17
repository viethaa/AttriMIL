# Video Download Instructions

## Current Status

**Videos Downloaded:** 0 / ~300
**Issue:** Google Drive rate limiting (too many people have accessed these files recently)

## What Happened

The download from Google Drive failed due to rate limiting. This is a common issue with popular shared folders on Google Drive. The error message was:

> "Too many users have viewed or downloaded this file recently. Please try accessing the file again later."

## How to Download the Videos

### Option 1: Retry Script (Recommended)

Wait **30 minutes** for the rate limit to reset, then run:

```bash
./scripts/data_processing/retry_download_videos.sh
```

This script will:
- Clean up empty directories from the failed attempt
- Retry the download with resume capability
- Show a summary of downloaded videos
- Tell you if you need to retry again

### Option 2: Manual Download from Browser

Sometimes downloading through the browser bypasses rate limits:

1. Open the Google Drive folder in your browser:
   https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN

2. You'll see three folders:
   - Adenoma (~52 videos)
   - Malignant (~45+ videos)
   - Normal (~30+ videos)

3. Download each folder:
   - Click on a folder (e.g., "Adenoma")
   - Right-click → Download
   - Repeat for all three folders

4. Extract the downloaded files to:
   ```
   data/video/raw_videos/Adenoma/
   data/video/raw_videos/Malignant/
   data/video/raw_videos/Normal/
   ```

### Option 3: Download with Python Script

The Python script I created earlier can also be used:

```bash
# Wait 30 minutes, then run:
python scripts/data_processing/download_all_videos.py --output-dir data/video/raw_videos --resume
```

## Expected Result

After successful download, you should have approximately **200-300 videos** organized like this:

```
data/video/raw_videos/
├── Adenoma/
│   ├── 1.avi
│   ├── 2.avi
│   ├── 24a0125.avi
│   └── ... (~52 total)
├── Malignant/
│   ├── 10.avi
│   ├── 11.avi
│   ├── 24a0271.avi
│   └── ... (~45+ total)
└── Normal/
    ├── 24a0631.avi
    ├── 24a0791.avi
    ├── 24a1536.avi
    └── ... (~30+ total)
```

## Verify Downloaded Videos

After downloading, check the count:

```bash
# Count all videos
find data/video/raw_videos -name "*.avi" | wc -l

# Count by class
find data/video/raw_videos/Adenoma -name "*.avi" | wc -l
find data/video/raw_videos/Malignant -name "*.avi" | wc -l
find data/video/raw_videos/Normal -name "*.avi" | wc -l
```

You should see around **200-300 total videos**.

## Troubleshooting

### Still Getting Rate Limit Errors?

- **Wait longer**: Sometimes it takes 1-2 hours for rate limits to fully reset
- **Try browser download**: Manual browser downloads often work when API downloads fail
- **Download in batches**: Download one class folder at a time
- **Use different network**: Try from a different IP address (different WiFi, mobile hotspot, etc.)

### Videos in "dataset2" Folder?

If videos download to `data/video/raw_videos/dataset2/`, move them:

```bash
mv data/video/raw_videos/dataset2/Adenoma data/video/raw_videos/
mv data/video/raw_videos/dataset2/Malignant data/video/raw_videos/
mv data/video/raw_videos/dataset2/Normal data/video/raw_videos/
rmdir data/video/raw_videos/dataset2
```

## Next Steps After Download

Once you have all videos downloaded:

1. **Extract features**:
   ```bash
   python scripts/data_processing/extract_video_features.py
   ```

2. **Prepare dataset**:
   ```bash
   python scripts/data_processing/prepare_video_dataset.py
   ```

3. **Train model**:
   ```bash
   python trainer_video.py
   ```

## Summary

**Right now:**
- ❌ 0 videos downloaded (rate limited)

**Next step:**
- ⏱️ Wait 30 minutes
- ▶️ Run: `./scripts/data_processing/retry_download_videos.sh`
- ✓ Verify ~200-300 videos downloaded
