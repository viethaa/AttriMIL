"""
Check the structure of downloaded CAMELYON16 features
"""
import pandas as pd
import pyarrow.parquet as pq

print("Checking downloaded CAMELYON16 features...")
print("="*80)

# Check train data
train_file = './camelyon16_features/data/Phikon_train-00000-of-00002-8a8b4d843ef2994a.parquet'
print(f"\nReading: {train_file}")

# Read parquet file
table = pq.read_table(train_file)
df = table.to_pandas()

print(f"\nDataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst row sample:")
print(df.head(1))

print(f"\nFeature shape for first sample: {df['features'].iloc[0].shape if hasattr(df['features'].iloc[0], 'shape') else 'N/A'}")
print(f"Label: {df['label'].iloc[0]}")

print("\n" + "="*80)
print("Summary:")
print(f"- Total samples in this file: {len(df)}")
print(f"- Features column type: {type(df['features'].iloc[0])}")
print(f"- Label distribution: {df['label'].value_counts().to_dict()}")
