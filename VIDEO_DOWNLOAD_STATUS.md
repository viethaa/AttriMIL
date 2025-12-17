# Video Download Status

## Current Count

**You have 94 out of 149 videos from Google Drive (~63%)**

Breakdown by class:
- **Adenoma**: 36 / 50 videos (72%)
- **Malignant**: 25 / 50 videos (50%)
- **Normal**: 33 / 49 videos (67%)

**Missing**: 55 videos total
- 14 Adenoma videos
- 25 Malignant videos
- 16 Normal videos

## Why Browser Download Failed

Google Drive tries to **zip large folders** before downloading, which:
1. Takes a long time for ~100+ GB of video files
2. Often times out or fails
3. Hits quota/rate limits during the zipping process

This is a known issue with large Google Drive folders.

## Solution: Individual File Downloads

I've created a script that downloads files **one-by-one** instead of as a folder. This:
- ✓ Avoids the zipping problem
- ✓ Can resume if interrupted
- ✓ Skips files you already have
- ✓ Works around rate limits better

## How to Download Missing Videos

Run this command:

```bash
python scripts/data_processing/download_individual_videos.py
```

The script will:
1. Skip the 94 videos you already have
2. Download the 55 missing videos one-by-one
3. Stop if it hits a rate limit
4. Show progress as it goes

### If It Hits Rate Limit

The script just hit a rate limit after downloading 1 file (you now have 94 videos). To continue:

1. **Wait 30-60 minutes** for rate limit to reset
2. **Run the same command again**:
   ```bash
   python scripts/data_processing/download_individual_videos.py
   ```
3. It will automatically skip files you already have and continue

### Download Specific Class Only

To download only missing videos from one class:

```bash
# Download only Malignant videos (25 missing)
python scripts/data_processing/download_individual_videos.py --class Malignant

# Download only Adenoma videos (14 missing)
python scripts/data_processing/download_individual_videos.py --class Adenoma

# Download only Normal videos (16 missing)
python scripts/data_processing/download_individual_videos.py --class Normal
```

## Expected Timeline

Due to Google Drive rate limits, you'll likely need to run the script **multiple times**:

- Each run might download **5-20 videos** before hitting rate limit
- Wait **30-60 minutes** between runs
- Total time: **4-8 hours** spread across a day (with waiting periods)

**Tip**: Run it a few times throughout the day when you think of it. The script picks up where it left off.

## Alternative: Download Over Multiple Days

Since the rate limit is per IP address per time period:

```bash
# Run today - download ~10-20 videos
python scripts/data_processing/download_individual_videos.py

# Run tomorrow - download ~10-20 more
python scripts/data_processing/download_individual_videos.py

# Run day after - download remaining
python scripts/data_processing/download_individual_videos.py
```

## Current Video Locations

Your videos are in:
- `data/full_dataset/Adenoma/` - 36 videos
- `data/full_dataset/Malignant/` - 25 videos
- `data/full_dataset/Normal/` - 33 videos

## Check Your Progress

Anytime you want to check how many videos you have:

```bash
# Count all videos
find data/full_dataset -name "*.avi" | wc -l

# Count by class
find data/full_dataset/Adenoma -name "*.avi" | wc -l
find data/full_dataset/Malignant -name "*.avi" | wc -l
find data/full_dataset/Normal -name "*.avi" | wc -l
```

## Summary

- ✅ **Codebase reorganized** - Clean folder structure
- ✅ **Individual download script created** - Works around folder zipping issue
- ✅ **94/149 videos downloaded** - 63% complete
- ⏳ **55 videos remaining** - Run script periodically to download them

**Next step**: Run the download script a few times throughout the day (waiting 30-60 min between runs) to get the remaining 55 videos.
