"""
Extract training metrics from log file
"""
import re

# Read log file
with open('training_better_split.log', 'r') as f:
    lines = f.readlines()

# Parse metrics
metrics = []
i = 0
while i < len(lines):
    line = lines[i]

    # Look for epoch line
    if line.startswith('Epoch:'):
        epoch_match = re.search(r'Epoch: (\d+), train_loss: ([\d.]+), train_error: ([\d.]+)', line)
        if epoch_match:
            epoch = int(epoch_match.group(1))
            train_loss = float(epoch_match.group(2))
            train_error = float(epoch_match.group(3))

            # Look ahead for Val Set line (skip class accuracy lines)
            j = i + 1
            while j < len(lines) and not lines[j].startswith('Val Set'):
                j += 1

            if j < len(lines):
                val_line = lines[j]
                val_match = re.search(r'val_loss: ([\d.]+), val_error: ([\d.]+), auc: ([\d.]+)', val_line)
                if val_match:
                    val_loss = float(val_match.group(1))
                    val_error = float(val_match.group(2))
                    val_auc = float(val_match.group(3))

                    metrics.append({
                        'epoch': epoch,
                        'train_loss': train_loss,
                        'train_error': train_error,
                        'val_loss': val_loss,
                        'val_error': val_error,
                        'val_auc': val_auc
                    })
    i += 1

# Print tab-separated format for spreadsheet
print("Epoch\tTrain_Loss\tTrain_Error\tVal_Loss\tVal_Error\tVal_AUC")
for m in metrics:
    print(f"{m['epoch']}\t{m['train_loss']}\t{m['train_error']}\t{m['val_loss']}\t{m['val_error']}\t{m['val_auc']}")

print(f"\n✅ Extracted {len(metrics)} epochs")
