"""
Automatically find videos in Google Drive and train
This script searches for videos in all possible locations
"""
import os
import subprocess

print("="*60)
print("Auto-Finding Videos in Google Drive")
print("="*60)

# Possible locations where videos might be
possible_paths = [
    "/content/drive/MyDrive/dataset2",
    "/content/drive/MyDrive/fulldata",
    "/content/drive/Shareddrives",
    "/content/drive/MyDrive/.shortcut-targets-by-id"
]

# Find all .avi files
print("\nSearching for videos...")
result = subprocess.run(
    ['find', '/content/drive', '-name', '*.avi', '-type', 'f'],
    capture_output=True,
    text=True,
    timeout=120
)

video_files = [line for line in result.stdout.split('\n') if line.strip()]

if not video_files:
    print("✗ No videos found!")
    print("\nPlease:")
    print("1. Make sure Drive is mounted")
    print("2. Copy videos to /content/drive/MyDrive/dataset2/")
    print("   with structure: Adenoma/, Malignant/, Normal/")
    exit(1)

print(f"✓ Found {len(video_files)} videos!")
print("\nFirst few videos:")
for v in video_files[:5]:
    print(f"  {v}")

# Detect structure
adenoma_videos = [v for v in video_files if 'Adenoma' in v or 'adenoma' in v]
malignant_videos = [v for v in video_files if 'Malignant' in v or 'malignant' in v]
normal_videos = [v for v in video_files if 'Normal' in v or 'normal' in v]

print(f"\nClass distribution:")
print(f"  Adenoma: {len(adenoma_videos)}")
print(f"  Malignant: {len(malignant_videos)}")
print(f"  Normal: {len(normal_videos)}")

# Find common root path
if video_files:
    sample_path = video_files[0]
    parts = sample_path.split('/')

    # Find where class folders are
    for i, part in enumerate(parts):
        if part in ['Adenoma', 'Malignant', 'Normal']:
            dataset_root = '/'.join(parts[:i])
            print(f"\n✓ Dataset root detected: {dataset_root}")

            # Update config_env.py
            print("\nUpdating configuration...")
            config_content = f'''
import os
from pathlib import Path

def is_colab():
    try:
        import google.colab
        return True
    except ImportError:
        return False

def get_env_config():
    config = {{}}
    config['is_colab'] = is_colab()

    DATASET_ROOT = "{dataset_root}"
    config['dataset_root'] = DATASET_ROOT
    config['csv_path'] = os.path.join(DATASET_ROOT, 'video_data', 'video_dataset.csv')
    config['feature_dir'] = os.path.join(DATASET_ROOT, 'video_features')
    config['split_path'] = os.path.join(DATASET_ROOT, 'video_data', 'splits')
    config['save_dir'] = '/content/drive/MyDrive/AttriMIL/results/models/video_attrimil'
    config['log_dir'] = '/content/drive/MyDrive/AttriMIL/results/logs/video_attrimil'
    config['max_epochs'] = 150
    config['lr'] = 0.0002
    config['early_stopping'] = True

    return config

def print_config(config):
    print("="*60)
    print("AttriMIL Configuration")
    print("="*60)
    print(f"Dataset Root: {{config['dataset_root']}}")
    print(f"CSV Path: {{config['csv_path']}}")
    print(f"Feature Dir: {{config['feature_dir']}}")
    print("="*60)
'''

            with open('config_env.py', 'w') as f:
                f.write(config_content)

            print("✓ Configuration updated!")
            print("\nNow run:")
            print("1. python extract_features_colab.py")
            print("2. python create_dataset_csv_colab.py")
            print("3. python train_colab.py")

            break
else:
    print("\n✗ Could not determine dataset structure")
