"""
Create better train/val/test splits with larger test set
45 train / 15 val / 15 test (15 patients per class in each split)
"""
import pickle
import pandas as pd
import numpy as np

# Load metadata
df = pickle.load(open('./video_panning_data/Image.pkl', 'rb'))

# Get unique patients per label
np.random.seed(42)  # For reproducibility

train_patients = []
val_patients = []
test_patients = []

# Stratified split: 15 train, 5 val, 5 test per class
for label in [0, 1, 2]:
    patients = df[df['label'] == label]['patient'].unique()
    np.random.shuffle(patients)

    train_patients.extend(patients[:15])
    val_patients.extend(patients[15:20])
    test_patients.extend(patients[20:25])

print("Better Split Summary:")
print(f"Train: {len(train_patients)} patients (15 per class)")
print(f"Val: {len(val_patients)} patients (5 per class)")
print(f"Test: {len(test_patients)} patients (5 per class)")

# Create splits CSV
max_len = max(len(train_patients), len(val_patients), len(test_patients))
splits_df = pd.DataFrame({
    'train': train_patients + [None] * (max_len - len(train_patients)),
    'val': val_patients + [None] * (max_len - len(val_patients)),
    'test': test_patients + [None] * (max_len - len(test_patients))
})

splits_df.to_csv('./video_panning_data/splits_better.csv', index=False)
print(f"\n✅ Saved better splits to: ./video_panning_data/splits_better.csv")

# Print label distribution per split
print("\nLabel distribution per split:")
for split_name, patient_list in [('Train', train_patients), ('Val', val_patients), ('Test', test_patients)]:
    split_df = df[df['patient'].isin(patient_list)]
    label_counts = split_df['label'].value_counts().sort_index()
    print(f"\n{split_name}:")
    for label, count in label_counts.items():
        n_patients = len(split_df[split_df['label'] == label]['patient'].unique())
        print(f"  Label {label}: {count} images from {n_patients} patients")
