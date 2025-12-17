"""
Create dataset CSV file from extracted features
Maps video names to labels and creates train/val/test splits
"""
import os
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import numpy as np

# Configuration
DATASET_ROOT = "/content/drive/MyDrive/dataset2"
FEATURE_DIR = f"{DATASET_ROOT}/video_features"
OUTPUT_DIR = f"{DATASET_ROOT}/video_data"
CSV_PATH = f"{OUTPUT_DIR}/video_dataset.csv"
SPLIT_DIR = f"{OUTPUT_DIR}/splits"

# Class mapping
CLASSES = {
    "Normal": 0,
    "Adenoma": 1,
    "Malignant": 2
}

# Split ratios
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

def collect_videos():
    """Collect all videos from class folders"""
    print("Collecting videos from class folders...")

    data = []
    for class_name, label in CLASSES.items():
        class_dir = os.path.join(DATASET_ROOT, class_name)

        if not os.path.exists(class_dir):
            print(f"⚠ Warning: {class_dir} not found, skipping...")
            continue

        # Get all video files
        video_files = [f for f in os.listdir(class_dir)
                      if f.endswith(('.avi', '.mp4', '.mov'))]

        print(f"  {class_name}: {len(video_files)} videos")

        for video_file in video_files:
            # Check if corresponding feature file exists
            feature_filename = os.path.splitext(video_file)[0] + '.pt'
            feature_path = os.path.join(FEATURE_DIR, feature_filename)

            if os.path.exists(feature_path):
                data.append({
                    'video_name': video_file,
                    'label': label,
                    'class_name': class_name
                })
            else:
                print(f"  ⚠ No features for {video_file}, skipping...")

    return data

def create_splits(data):
    """Create train/val/test splits"""
    print("\nCreating train/val/test splits...")

    df = pd.DataFrame(data)

    # Separate by class for stratified split
    train_data = []
    val_data = []
    test_data = []

    for label in df['label'].unique():
        class_df = df[df['label'] == label]
        n = len(class_df)

        # Split into train, val, test
        train_df, temp_df = train_test_split(
            class_df, test_size=(VAL_RATIO + TEST_RATIO),
            random_state=42
        )
        val_df, test_df = train_test_split(
            temp_df, test_size=TEST_RATIO/(VAL_RATIO + TEST_RATIO),
            random_state=42
        )

        train_data.append(train_df)
        val_data.append(val_df)
        test_data.append(test_df)

    # Combine all classes
    train_df = pd.concat(train_data, ignore_index=True)
    val_df = pd.concat(val_data, ignore_index=True)
    test_df = pd.concat(test_data, ignore_index=True)

    # Add split column
    train_df['split'] = 'train'
    val_df['split'] = 'val'
    test_df['split'] = 'test'

    # Combine into final dataset
    final_df = pd.concat([train_df, val_df, test_df], ignore_index=True)

    # Print split statistics
    print(f"\n  Total videos: {len(final_df)}")
    print(f"  Train: {len(train_df)} ({len(train_df)/len(final_df)*100:.1f}%)")
    print(f"  Val: {len(val_df)} ({len(val_df)/len(final_df)*100:.1f}%)")
    print(f"  Test: {len(test_df)} ({len(test_df)/len(final_df)*100:.1f}%)")

    print("\n  Per-class distribution:")
    for label, class_name in enumerate(['Normal', 'Adenoma', 'Malignant']):
        class_df = final_df[final_df['label'] == label]
        train_count = len(class_df[class_df['split'] == 'train'])
        val_count = len(class_df[class_df['split'] == 'val'])
        test_count = len(class_df[class_df['split'] == 'test'])
        print(f"    {class_name}: train={train_count}, val={val_count}, test={test_count}")

    return final_df

def save_csv(df):
    """Save dataset CSV"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(SPLIT_DIR, exist_ok=True)

    # Save main CSV
    df_to_save = df[['video_name', 'label', 'split']]
    df_to_save.to_csv(CSV_PATH, index=False)
    print(f"\n✓ Saved main CSV: {CSV_PATH}")

    # Also save split-specific CSVs for compatibility
    for split in ['train', 'val', 'test']:
        split_df = df[df['split'] == split][['video_name', 'label']]
        split_path = os.path.join(SPLIT_DIR, f'split_{split}.csv')
        split_df.to_csv(split_path, index=False)
        print(f"✓ Saved {split} split: {split_path}")

    # Print first few rows
    print("\nFirst 10 rows of dataset:")
    print(df_to_save.head(10).to_string(index=False))

def main():
    print("="*60)
    print("Create Dataset CSV for AttriMIL")
    print("="*60)

    # Check if features exist
    if not os.path.exists(FEATURE_DIR):
        print(f"\n✗ Error: Feature directory not found: {FEATURE_DIR}")
        print("Please run extract_features_colab.py first!")
        return

    feature_count = len([f for f in os.listdir(FEATURE_DIR) if f.endswith('.pt')])
    print(f"\nFound {feature_count} feature files in {FEATURE_DIR}")

    if feature_count == 0:
        print("\n✗ Error: No feature files found!")
        print("Please run extract_features_colab.py first!")
        return

    # Collect videos
    data = collect_videos()

    if not data:
        print("\n✗ Error: No videos found!")
        return

    # Create splits
    df = create_splits(data)

    # Save CSV
    save_csv(df)

    print("\n" + "="*60)
    print("Dataset CSV Created Successfully!")
    print("="*60)
    print(f"✓ CSV file: {CSV_PATH}")
    print(f"✓ Total videos: {len(df)}")
    print("\n✓ Ready for training!")
    print("Next step: Run train_colab.py")

if __name__ == "__main__":
    main()
