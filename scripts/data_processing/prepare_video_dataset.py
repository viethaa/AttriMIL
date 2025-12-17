"""
Prepare video dataset for AttriMIL training.

This script:
1. Scans the video folders
2. Creates a CSV file with video metadata
3. Creates train/val/test splits
4. Prepares for feature extraction
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
DATA_ROOT = Path("full_dataset")
OUTPUT_DIR = Path("video_data")
OUTPUT_DIR.mkdir(exist_ok=True)

# Label mapping
LABEL_DICT = {
    'Normal': 0,
    'Adenoma': 1,
    'Malignant': 2
}

def scan_videos(data_root):
    """Scan video folders and create metadata."""
    videos = []

    for category in ['Normal', 'Adenoma', 'Malignant']:
        category_path = data_root / category

        if not category_path.exists():
            print(f"Warning: {category} folder not found, skipping...")
            continue

        # Find all .avi files
        video_files = list(category_path.glob("*.avi"))
        print(f"Found {len(video_files)} videos in {category}/")

        for video_file in video_files:
            video_id = video_file.stem  # filename without extension
            label = LABEL_DICT[category]
            file_size_mb = video_file.stat().st_size / (1024 * 1024)

            videos.append({
                'video_id': video_id,
                'category': category,
                'label': label,
                'file_path': str(video_file.relative_to(data_root)),
                'file_size_mb': f"{file_size_mb:.1f}"
            })

    return pd.DataFrame(videos)

def create_splits(df, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2, seed=42):
    """Create train/val/test splits stratified by label."""
    np.random.seed(seed)

    # Initialize split columns
    df['train'] = False
    df['val'] = False
    df['test'] = False

    # Split by category to maintain balance
    for category in df['category'].unique():
        category_indices = df[df['category'] == category].index.tolist()
        n = len(category_indices)

        # Shuffle
        np.random.shuffle(category_indices)

        # Calculate split sizes
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)

        # Assign splits
        train_idx = category_indices[:n_train]
        val_idx = category_indices[n_train:n_train + n_val]
        test_idx = category_indices[n_train + n_val:]

        df.loc[train_idx, 'train'] = True
        df.loc[val_idx, 'val'] = True
        df.loc[test_idx, 'test'] = True

    return df

def print_split_summary(df):
    """Print summary of the splits."""
    print("\n" + "="*80)
    print("DATASET SPLIT SUMMARY")
    print("="*80)

    for split in ['train', 'val', 'test']:
        split_df = df[df[split]]
        print(f"\n{split.upper()} SET ({len(split_df)} videos):")
        print(split_df.groupby('category').size().to_string())

    print("\n" + "="*80)
    print("OVERALL DISTRIBUTION")
    print("="*80)
    print(df.groupby('category').size().to_string())
    print(f"\nTotal videos: {len(df)}")
    print(f"Total size: {df['file_size_mb'].astype(float).sum():.1f} MB")

def main():
    print("Scanning video dataset...")
    df = scan_videos(DATA_ROOT)

    if len(df) == 0:
        print("Error: No videos found!")
        return

    print(f"\nFound {len(df)} total videos")

    # Create splits
    print("\nCreating train/val/test splits...")
    df = create_splits(df)

    # Save full dataset info
    csv_path = OUTPUT_DIR / "video_dataset.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved dataset info to: {csv_path}")

    # Save splits
    splits_dir = OUTPUT_DIR / "splits"
    splits_dir.mkdir(exist_ok=True)

    # Save in AttriMIL format (compatible with existing code)
    split_df = df[['video_id', 'label', 'train', 'val', 'test']].copy()
    split_df.to_csv(splits_dir / "splits_0.csv", index=False)
    print(f"Saved splits to: {splits_dir / 'splits_0.csv'}")

    # Print summary
    print_split_summary(df)

    # Save a detailed report
    report_path = OUTPUT_DIR / "dataset_report.txt"
    with open(report_path, 'w') as f:
        f.write("VIDEO DATASET REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total videos: {len(df)}\n")
        f.write(f"Total size: {df['file_size_mb'].astype(float).sum():.1f} MB\n\n")

        f.write("Distribution by category:\n")
        f.write(df.groupby('category').size().to_string())
        f.write("\n\n")

        f.write("Split distribution:\n")
        for split in ['train', 'val', 'test']:
            split_df = df[df[split]]
            f.write(f"\n{split.upper()} SET ({len(split_df)} videos):\n")
            f.write(split_df.groupby('category').size().to_string())
            f.write("\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("FILES LIST:\n")
        f.write("=" * 80 + "\n")
        for idx, row in df.iterrows():
            f.write(f"{row['video_id']}: {row['category']} ({row['file_size_mb']} MB)\n")

    print(f"\nSaved detailed report to: {report_path}")

    # Create info for next steps
    next_steps_path = OUTPUT_DIR / "NEXT_STEPS.md"
    with open(next_steps_path, 'w') as f:
        f.write("# Next Steps for Video AttriMIL\n\n")
        f.write("## 1. Install Dependencies\n\n")
        f.write("```bash\n")
        f.write("pip install opencv-python-headless\n")
        f.write("pip install torch torchvision\n")
        f.write("pip install timm  # For video transformers\n")
        f.write("```\n\n")

        f.write("## 2. Extract Video Features\n\n")
        f.write("You need to extract features from the videos before training.\n\n")
        f.write("Options:\n")
        f.write("- **I3D** (Kinetics-400 pretrained): 1024-dim features\n")
        f.write("- **SlowFast**: 2048-dim features\n")
        f.write("- **VideoMAE** (Recommended): 768-dim features (matches PHIKON!)\n\n")

        f.write("## 3. Create Feature Extraction Script\n\n")
        f.write("See `extract_video_features.py` (to be created)\n\n")

        f.write("## 4. Adapt AttriMIL Trainer\n\n")
        f.write("Modify trainer to:\n")
        f.write("- Load video features instead of WSI features\n")
        f.write("- Replace spatial constraint with temporal constraint\n")
        f.write("- Adjust for multi-class classification (3 classes)\n\n")

        f.write("## 5. Run Training\n\n")
        f.write("```bash\n")
        f.write("python trainer_video.py\n")
        f.write("```\n")

    print(f"Saved next steps guide to: {next_steps_path}")

    print("\n✅ Dataset preparation complete!")
    print(f"\nDataset info saved in: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
