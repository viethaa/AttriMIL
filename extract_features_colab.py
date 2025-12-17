"""
Extract features from videos in Google Drive for AttriMIL training
Processes videos from class folders and saves features as .pt files
"""
import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.io import read_video
import cv2
from pathlib import Path
from tqdm import tqdm
import numpy as np

# Configuration
DATASET_ROOT = "/content/drive/MyDrive/dataset2"
FEATURE_DIR = f"{DATASET_ROOT}/video_features"
CLASSES = ["Normal", "Adenoma", "Malignant"]  # 0, 1, 2

# Feature extraction settings
FRAMES_PER_VIDEO = 50  # Number of frames to sample per video
FEATURE_DIM = 2048  # ResNet50 output dimension

def setup_feature_extractor():
    """Load pre-trained ResNet50 as feature extractor"""
    print("Loading ResNet50 feature extractor...")
    model = models.resnet50(pretrained=True)
    # Remove final classification layer
    model = torch.nn.Sequential(*list(model.children())[:-1])
    model.eval()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    print(f"✓ Feature extractor loaded on {device}")
    return model, device

def get_transform():
    """Image preprocessing transform"""
    return transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])

def extract_frames(video_path, num_frames=50):
    """Extract uniformly sampled frames from video"""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        cap.release()
        return None

    # Sample frame indices uniformly
    if total_frames < num_frames:
        frame_indices = list(range(total_frames))
    else:
        frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)

    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

    cap.release()
    return frames if frames else None

def extract_features_from_video(video_path, model, device, transform):
    """Extract features from a single video"""
    # Extract frames
    frames = extract_frames(video_path, num_frames=FRAMES_PER_VIDEO)
    if frames is None or len(frames) == 0:
        return None

    # Process frames through CNN
    features = []
    with torch.no_grad():
        for frame in frames:
            # Preprocess frame
            frame_tensor = transform(frame).unsqueeze(0).to(device)
            # Extract features
            feat = model(frame_tensor)
            feat = feat.squeeze().cpu()
            features.append(feat)

    # Stack into tensor [num_frames, feature_dim]
    features = torch.stack(features)
    return features

def main():
    print("="*60)
    print("Video Feature Extraction for AttriMIL")
    print("="*60)

    # Create output directory
    os.makedirs(FEATURE_DIR, exist_ok=True)
    print(f"\nFeatures will be saved to: {FEATURE_DIR}")

    # Setup feature extractor
    model, device = setup_feature_extractor()
    transform = get_transform()

    # Process each class
    total_videos = 0
    failed_videos = []

    for class_idx, class_name in enumerate(CLASSES):
        class_dir = os.path.join(DATASET_ROOT, class_name)

        if not os.path.exists(class_dir):
            print(f"\n⚠ Warning: Directory not found: {class_dir}")
            continue

        # Get all video files
        video_files = [f for f in os.listdir(class_dir)
                      if f.endswith(('.avi', '.mp4', '.mov'))]

        print(f"\n{'='*60}")
        print(f"Processing {class_name} (label={class_idx})")
        print(f"Found {len(video_files)} videos")
        print(f"{'='*60}")

        # Process each video
        for video_file in tqdm(video_files, desc=f"{class_name}"):
            video_path = os.path.join(class_dir, video_file)

            # Output feature file name
            feature_filename = os.path.splitext(video_file)[0] + '.pt'
            feature_path = os.path.join(FEATURE_DIR, feature_filename)

            # Skip if already processed
            if os.path.exists(feature_path):
                continue

            try:
                # Extract features
                features = extract_features_from_video(video_path, model, device, transform)

                if features is not None:
                    # Save features
                    torch.save(features, feature_path)
                    total_videos += 1
                else:
                    failed_videos.append(video_file)

            except Exception as e:
                print(f"\n✗ Error processing {video_file}: {e}")
                failed_videos.append(video_file)

    # Summary
    print("\n" + "="*60)
    print("Feature Extraction Complete!")
    print("="*60)
    print(f"✓ Successfully processed: {total_videos} videos")
    print(f"✓ Features saved to: {FEATURE_DIR}")

    if failed_videos:
        print(f"\n⚠ Failed videos ({len(failed_videos)}):")
        for vid in failed_videos[:10]:  # Show first 10
            print(f"  - {vid}")
        if len(failed_videos) > 10:
            print(f"  ... and {len(failed_videos)-10} more")

    print("\n✓ Ready for CSV creation!")
    print("Next step: Run create_dataset_csv_colab.py")

if __name__ == "__main__":
    main()
