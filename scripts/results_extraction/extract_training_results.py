"""
Extract training results from TensorBoard logs and format for Google Sheets
"""
import os
from tensorboard.backend.event_processing import event_accumulator
import pandas as pd
import glob

# Find tensorboard log directory
log_dir = './save_weights/camelyon16_attrimil_phikon/0/'

# Find event file
event_files = glob.glob(os.path.join(log_dir, 'events.out.tfevents.*'))

if not event_files:
    print("No tensorboard event files found!")
    exit(1)

print(f"Reading from: {event_files[0]}")

# Load tensorboard data
ea = event_accumulator.EventAccumulator(event_files[0])
ea.Reload()

# Get available tags
print("\nAvailable scalar tags:")
for tag in ea.Tags()['scalars']:
    print(f"  - {tag}")

# Extract data
data = {
    'Epoch': [],
    'Train_Loss': [],
    'Train_Loss_Bag': [],
    'Val_Loss': [],
    'Val_AUC': [],
    'Train_Class0_Acc': [],
    'Train_Class1_Acc': [],
}

# Get all scalar data
for tag in ea.Tags()['scalars']:
    events = ea.Scalars(tag)

    for event in events:
        epoch = event.step
        value = event.value

        # Add epoch if not already there
        if epoch not in data['Epoch']:
            data['Epoch'].append(epoch)
            # Initialize all metrics for this epoch
            data['Train_Loss'].append(None)
            data['Train_Loss_Bag'].append(None)
            data['Val_Loss'].append(None)
            data['Val_AUC'].append(None)
            data['Train_Class0_Acc'].append(None)
            data['Train_Class1_Acc'].append(None)

        # Find index for this epoch
        idx = data['Epoch'].index(epoch)

        # Map tag to column
        if tag == 'train/loss':
            data['Train_Loss'][idx] = value
        elif tag == 'train/loss_bag':
            data['Train_Loss_Bag'][idx] = value
        elif tag == 'val/loss':
            data['Val_Loss'][idx] = value
        elif tag == 'val/auc':
            data['Val_AUC'][idx] = value
        elif tag == 'train/class_0_acc':
            data['Train_Class0_Acc'][idx] = value
        elif tag == 'train/class_1_acc':
            data['Train_Class1_Acc'][idx] = value

# Create DataFrame
df = pd.DataFrame(data)
df = df.sort_values('Epoch')

# Fill in missing values with forward fill
df = df.fillna(method='ffill')

print(f"\n\nExtracted {len(df)} epochs of data")
print("\nFirst few rows:")
print(df.head(10))
print("\nLast few rows:")
print(df.tail(10))

# Save as CSV (easy to import to Google Sheets)
output_file = 'training_results.csv'
df.to_csv(output_file, index=False)
print(f"\n✅ Saved to: {output_file}")
print("\nYou can now:")
print("1. Open this CSV in Google Sheets")
print("2. Or copy the output below and paste directly into Sheets\n")

print("="*80)
print("COPY THIS INTO GOOGLE SHEETS:")
print("="*80)
# Print tab-separated for easy paste into sheets
for col in df.columns:
    print(col, end='\t')
print()

for _, row in df.iterrows():
    for col in df.columns:
        val = row[col]
        if pd.isna(val):
            print('', end='\t')
        else:
            print(f"{val:.6f}", end='\t')
    print()
