"""
Detailed inspection of feature structure
"""
import pandas as pd
import pyarrow.parquet as pq
import numpy as np

train_file = './camelyon16_features/data/Phikon_train-00000-of-00002-8a8b4d843ef2994a.parquet'
table = pq.read_table(train_file)
df = table.to_pandas()

print("Detailed Feature Inspection")
print("="*80)

# Get first sample
first_sample_features = df['features'].iloc[0]
print(f"Type: {type(first_sample_features)}")
print(f"Shape: {first_sample_features.shape}")
print(f"Dtype: {first_sample_features.dtype}")

# Check if it's nested
if len(first_sample_features.shape) > 1:
    print(f"\nThis appears to be patch-level features!")
    print(f"Number of patches: {first_sample_features.shape[0]}")
    print(f"Feature dimension per patch: {first_sample_features.shape[1]}")
else:
    print(f"\nThis appears to be slide-level aggregated features")
    print(f"Feature vector length: {first_sample_features.shape[0]}")

print(f"\nFirst few values: {first_sample_features[:10]}")

# Check a few more samples
print(f"\n\nChecking multiple samples:")
for i in range(min(5, len(df))):
    feat_shape = df['features'].iloc[i].shape
    label = df['label'].iloc[i]
    print(f"Sample {i}: shape={feat_shape}, label={label}")
