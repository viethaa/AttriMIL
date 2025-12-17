"""
Extract features from videos for AttriMIL training.

This script extracts frame-level features using a pretrained vision model.
Each video becomes a "bag" and frames become "instances" in MIL terminology.
"""

import os
import sys
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import argparse

class VideoFeatureExtractor:
    """Extract features from video frames using pretrained CNN."""

    def __init__(self, model_name='resnet50', device='auto', feature_dim=2048):
        """
        Initialize feature extractor.

        Args:
            model_name: Name of the model to use ('resnet50', etc.)
            device: Device to use ('cuda', 'mps', 'cpu', or 'auto')
            feature_dim: Dimension of extracted features
        """
        self.model_name = model_name
        self.feature_dim = feature_dim

        # Setup device
        if device == 'auto':
            if torch.cuda.is_available():
                self.device = torch.device('cuda')
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                self.device = torch.device('mps')
            else:
                self.device = torch.device('cpu')
        else:
            self.device = torch.device(device)

        print(f"Using device: {self.device}")

        # Load model
        self.model = self._load_model()
        self.model = self.model.to(self.device)
        self.model.eval()

        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def _load_model(self):
        """Load pretrained model and remove classification head."""
        if self.model_name == 'resnet50':
            # Load pretrained ResNet50
            model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)

            # Remove the final classification layer
            # ResNet50: conv layers + avgpool + fc
            # We want features before fc layer (2048-dim)
            model = nn.Sequential(*list(model.children())[:-1])

        else:
            raise ValueError(f"Model {self.model_name} not supported yet")

        return model

    def extract_from_frame(self, frame):
        """Extract features from a single frame."""
        # Preprocess frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_tensor = self.transform(frame_rgb).unsqueeze(0).to(self.device)

        # Extract features
        with torch.no_grad():
            features = self.model(frame_tensor)
            features = features.squeeze()  # Remove batch and spatial dims

        return features.cpu().numpy()

    def extract_from_video(self, video_path, sample_rate=30, max_frames=None):
        """
        Extract features from video by sampling frames.

        Args:
            video_path: Path to video file
            sample_rate: Sample every Nth frame (e.g., 30 = 1 frame per second @ 30fps)
            max_frames: Maximum number of frames to process (None = all)

        Returns:
            numpy array of shape (num_frames, feature_dim)
        """
        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        features_list = []
        frame_count = 0
        sampled_count = 0

        pbar = tqdm(total=total_frames//sample_rate,
                   desc=f"Processing {Path(video_path).name}",
                   leave=False)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Sample frames
            if frame_count % sample_rate == 0:
                try:
                    features = self.extract_from_frame(frame)
                    features_list.append(features)
                    sampled_count += 1
                    pbar.update(1)

                    if max_frames and sampled_count >= max_frames:
                        break

                except Exception as e:
                    print(f"Error processing frame {frame_count}: {e}")

            frame_count += 1

        cap.release()
        pbar.close()

        if len(features_list) == 0:
            raise ValueError(f"No features extracted from {video_path}")

        features_array = np.stack(features_list, axis=0)

        print(f"  Extracted {len(features_list)} frames from {frame_count} total "
              f"({fps:.1f} fps, {frame_count/fps:.1f}s duration)")

        return features_array

def main():
    parser = argparse.ArgumentParser(description='Extract features from videos')
    parser.add_argument('--data_root', type=str, default='full_dataset',
                       help='Root directory containing video folders')
    parser.add_argument('--csv_file', type=str, default='video_data/video_dataset.csv',
                       help='CSV file with video metadata')
    parser.add_argument('--output_dir', type=str, default='video_features',
                       help='Output directory for features')
    parser.add_argument('--sample_rate', type=int, default=30,
                       help='Sample every Nth frame (default: 30 = 1 fps @ 30fps video)')
    parser.add_argument('--max_frames', type=int, default=None,
                       help='Maximum frames per video (default: None = all)')
    parser.add_argument('--model', type=str, default='resnet50',
                       help='Model to use for feature extraction')
    parser.add_argument('--device', type=str, default='auto',
                       help='Device to use (auto/cuda/mps/cpu)')

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Load dataset info
    df = pd.read_csv(args.csv_file)
    print(f"\nLoaded {len(df)} videos from {args.csv_file}")

    # Initialize feature extractor
    print("\nInitializing feature extractor...")
    extractor = VideoFeatureExtractor(
        model_name=args.model,
        device=args.device
    )

    # Process each video
    print(f"\nExtracting features (sampling every {args.sample_rate} frames)...")
    print("="*80)

    features_info = []
    errors = []

    for idx, row in df.iterrows():
        video_id = row['video_id']
        video_path = Path(args.data_root) / row['file_path']

        print(f"\n[{idx+1}/{len(df)}] Processing: {video_id}")

        if not video_path.exists():
            print(f"  WARNING: Video not found: {video_path}")
            errors.append(video_id)
            continue

        try:
            # Extract features
            features = extractor.extract_from_video(
                video_path,
                sample_rate=args.sample_rate,
                max_frames=args.max_frames
            )

            # Save features as .pt file (PyTorch format)
            output_path = output_dir / f"{video_id}.pt"
            torch.save(torch.from_numpy(features), output_path)

            # Record info
            features_info.append({
                'video_id': video_id,
                'num_frames': features.shape[0],
                'feature_dim': features.shape[1],
                'feature_file': str(output_path),
                'status': 'success'
            })

            print(f"  ✓ Saved {features.shape[0]} frame features to {output_path}")

        except Exception as e:
            print(f"  ✗ ERROR: {str(e)}")
            errors.append(video_id)
            features_info.append({
                'video_id': video_id,
                'status': 'failed',
                'error': str(e)
            })

    # Save extraction info
    info_df = pd.DataFrame(features_info)
    info_path = output_dir / 'extraction_info.csv'
    info_df.to_csv(info_path, index=False)

    print("\n" + "="*80)
    print("EXTRACTION SUMMARY")
    print("="*80)
    print(f"Total videos: {len(df)}")
    print(f"Successfully processed: {len([x for x in features_info if x.get('status') == 'success'])}")
    print(f"Failed: {len(errors)}")

    if errors:
        print(f"\nFailed videos: {', '.join(errors)}")

    print(f"\nFeatures saved in: {output_dir}/")
    print(f"Extraction info saved in: {info_path}")

    # Print statistics
    successful = info_df[info_df['status'] == 'success']
    if len(successful) > 0:
        print(f"\nFeature statistics:")
        print(f"  Average frames per video: {successful['num_frames'].mean():.1f}")
        print(f"  Min frames: {successful['num_frames'].min()}")
        print(f"  Max frames: {successful['num_frames'].max()}")
        print(f"  Feature dimension: {successful['feature_dim'].iloc[0]}")

    print("\n✅ Feature extraction complete!")
    print(f"\nNext step: Adapt trainer for video features")
    print(f"  - Update dataloader to load .pt files instead of .h5 files")
    print(f"  - Adjust AttriMIL model for {successful['feature_dim'].iloc[0] if len(successful) > 0 else 2048}-dim features")
    print(f"  - Run training with: python trainer_video.py")

if __name__ == "__main__":
    main()
