"""
Extract accuracy metrics from training log for spreadsheet
"""
import re

# Read log file
with open('training_better_split.log', 'r') as f:
    lines = f.readlines()

# Parse accuracy metrics
metrics = []
i = 0
while i < len(lines):
    line = lines[i]

    # Look for epoch line
    if line.startswith('Epoch:'):
        epoch_match = re.search(r'Epoch: (\d+), train_loss: [\d.]+, train_error: ([\d.]+)', line)
        if epoch_match:
            epoch = int(epoch_match.group(1))
            train_error = float(epoch_match.group(2))
            train_acc_overall = 1 - train_error

            # Extract train class accuracies (next 3 lines)
            train_class_acc = {}
            for j in range(1, 4):
                if i+j < len(lines):
                    class_match = re.search(r'Class (\d+): acc ([\d.]+)', lines[i+j])
                    if class_match:
                        cls = int(class_match.group(1))
                        acc = float(class_match.group(2))
                        train_class_acc[cls] = acc

            # Find Val Set line
            j = i + 1
            while j < len(lines) and not lines[j].startswith('Val Set'):
                j += 1

            if j < len(lines):
                val_line = lines[j]
                val_match = re.search(r'val_error: ([\d.]+)', val_line)
                if val_match:
                    val_error = float(val_match.group(1))
                    val_acc_overall = 1 - val_error

                    # Extract val class accuracies (next 3 lines after Val Set)
                    val_class_acc = {}
                    for k in range(1, 4):
                        if j+k < len(lines):
                            class_match = re.search(r'Class (\d+): acc ([\d.]+)', lines[j+k])
                            if class_match:
                                cls = int(class_match.group(1))
                                acc = float(class_match.group(2))
                                val_class_acc[cls] = acc

                    metrics.append({
                        'epoch': epoch,
                        'train_acc_overall': train_acc_overall,
                        'train_acc_c0': train_class_acc.get(0, 0),
                        'train_acc_c1': train_class_acc.get(1, 0),
                        'train_acc_c2': train_class_acc.get(2, 0),
                        'val_acc_overall': val_acc_overall,
                        'val_acc_c0': val_class_acc.get(0, 0),
                        'val_acc_c1': val_class_acc.get(1, 0),
                        'val_acc_c2': val_class_acc.get(2, 0)
                    })
    i += 1

# Print tab-separated format for spreadsheet
print("Epoch\tTrain_Acc\tTrain_C0\tTrain_C1\tTrain_C2\tVal_Acc\tVal_C0\tVal_C1\tVal_C2")
for m in metrics:
    print(f"{m['epoch']}\t{m['train_acc_overall']:.4f}\t{m['train_acc_c0']:.4f}\t{m['train_acc_c1']:.4f}\t{m['train_acc_c2']:.4f}\t{m['val_acc_overall']:.4f}\t{m['val_acc_c0']:.4f}\t{m['val_acc_c1']:.4f}\t{m['val_acc_c2']:.4f}")

print(f"\n✅ Extracted {len(metrics)} epochs")
