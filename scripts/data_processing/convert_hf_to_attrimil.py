"""
Convert Hugging Face CAMELYON16 features to AttriMIL format
"""
import pandas as pd
import numpy as np
import h5py
import torch
import os
from tqdm import tqdm
import pyarrow.parquet as pq

print("="*80)
print("Converting Hugging Face CAMELYON16 data to AttriMIL format")
print("="*80)

# Create output directories
os.makedirs('./camelyon16_attrimil/h5_files', exist_ok=True)
os.makedirs('./camelyon16_attrimil/pt_files', exist_ok=True)
os.makedirs('./camelyon16_attrimil/splits', exist_ok=True)

# Load train and test data
print("\nLoading train data...")
train_files = [
    './camelyon16_features/data/Phikon_train-00000-of-00002-8a8b4d843ef2994a.parquet',
    './camelyon16_features/data/Phikon_train-00001-of-00002-d9e9ef91efa8af1d.parquet'
]

train_dfs = []
for f in train_files:
    table = pq.read_table(f)
    train_dfs.append(table.to_pandas())
train_df = pd.concat(train_dfs, ignore_index=True)

print(f"Loading test data...")
test_file = './camelyon16_features/data/Phikon_test-00000-of-00001-f7f5c26c8b3c993c.parquet'
table = pq.read_table(test_file)
test_df = table.to_pandas()

print(f"\nTrain samples: {len(train_df)}")
print(f"Test samples: {len(test_df)}")

# Create CSV with slide info
all_slide_ids = []
all_labels = []

def process_split(df, split_name):
    """Process a data split and create .h5 and .pt files"""
    print(f"\nProcessing {split_name} split...")

    slide_ids = []
    labels = []

    for idx in tqdm(range(len(df)), desc=f"Converting {split_name}"):
        slide_id = f"{split_name}_slide_{idx:04d}"
        features_array = df['features'].iloc[idx]
        label = int(df['label'].iloc[idx])

        # Convert to numpy array if needed
        features_list = []
        coords_list = []

        for patch in features_array:
            if len(patch) >= 3:
                # First 3 values appear to be coordinates
                coords_list.append(patch[:3])
                # Rest are features
                features_list.append(patch[3:])

        features = np.array(features_list, dtype=np.float32)
        coords = np.array(coords_list, dtype=np.float32)

        # Save as .h5 file
        h5_path = f'./camelyon16_attrimil/h5_files/{slide_id}.h5'
        with h5py.File(h5_path, 'w') as f:
            f.create_dataset('features', data=features)
            f.create_dataset('coords', data=coords)
            # Create dummy nearest neighbors (AttriMIL needs this)
            # Use simple indices for now
            n_patches = len(features)
            nearest = np.zeros((n_patches, 3), dtype=np.int64)
            for i in range(n_patches):
                # Simple neighbor assignment: just nearby indices
                neighbors = []
                for j in range(max(0, i-10), min(n_patches, i+10)):
                    if j != i:
                        neighbors.append(j)
                        if len(neighbors) >= 3:
                            break
                while len(neighbors) < 3:
                    neighbors.append(min(i, n_patches-1))
                nearest[i] = neighbors[:3]
            f.create_dataset('nearest', data=nearest)

        # Save as .pt file
        pt_path = f'./camelyon16_attrimil/pt_files/{slide_id}.pt'
        torch.save(torch.from_numpy(features), pt_path)

        slide_ids.append(slide_id)
        labels.append('tumor_tissue' if label == 1 else 'normal_tissue')

    return slide_ids, labels

# Process train and test splits
train_ids, train_labels = process_split(train_df, 'train')
test_ids, test_labels = process_split(test_df, 'test')

# Create master CSV
print("\nCreating dataset CSV...")
all_ids = train_ids + test_ids
all_labels_text = train_labels + test_labels

dataset_df = pd.DataFrame({
    'slide_id': all_ids,
    'label': all_labels_text
})
dataset_df.to_csv('./camelyon16_attrimil/camelyon16_total.csv', index=False)

# Create train/val/test splits (80/10/10 split for train data)
from sklearn.model_selection import train_test_split

train_val_df = dataset_df[:len(train_ids)]
test_df_final = dataset_df[len(train_ids):]

# Split train into train/val
train_final_df, val_df = train_test_split(
    train_val_df, test_size=0.111, random_state=42, stratify=train_val_df['label']
)

print(f"\nFinal splits:")
print(f"  Train: {len(train_final_df)}")
print(f"  Val: {len(val_df)}")
print(f"  Test: {len(test_df_final)}")

# Save split CSV
split_df = pd.DataFrame({
    'train': pd.Series(train_final_df['slide_id'].values),
    'val': pd.Series(val_df['slide_id'].values),
    'test': pd.Series(test_df_final['slide_id'].values)
})
split_df.to_csv('./camelyon16_attrimil/splits/splits_0.csv', index=False)

print("\n" + "="*80)
print("Conversion complete!")
print("="*80)
print(f"\nOutput structure:")
print(f"  camelyon16_attrimil/")
print(f"    ├── h5_files/          ({len(all_ids)} files)")
print(f"    ├── pt_files/          ({len(all_ids)} files)")
print(f"    ├── camelyon16_total.csv")
print(f"    └── splits/")
print(f"        └── splits_0.csv")
print("\nYou can now run training with these paths!")
