"""
Video dataloader for AttriMIL
Loads video features from .pt files where each video is a bag and each frame is an instance
"""
from __future__ import print_function, division
import os
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset


class Video_MIL_Dataset(Dataset):
    def __init__(self,
                 csv_path='video_data/video_dataset.csv',
                 feature_dir='video_features',
                 shuffle=False,
                 seed=7,
                 print_info=True,
                 label_dict=None,
                 ignore=[]):
        """
        Args:
            csv_path (string): Path to the csv file with video metadata.
            feature_dir (string): Directory with all the feature .pt files.
            shuffle (bool): Whether to shuffle the dataset
            seed (int): random seed for shuffling the data
            print_info (bool): Whether to print dataset info
            label_dict (dict): Optional dictionary mapping category names to labels
            ignore (list): List of video_ids to ignore
        """
        self.feature_dir = feature_dir
        self.label_dict = label_dict

        # Read CSV
        video_data = pd.read_csv(csv_path)

        # Remove ignored samples
        if len(ignore) > 0:
            video_data = video_data[~video_data['video_id'].isin(ignore)]

        # Map labels if label_dict provided
        if label_dict is not None and len(label_dict) > 0:
            video_data['label'] = video_data['category'].map(label_dict)

        # Get unique video IDs
        video_ids = video_data['video_id'].unique()

        if shuffle:
            np.random.seed(seed)
            np.random.shuffle(video_ids)

        # Determine number of classes
        self.num_classes = video_data['label'].nunique()

        # Create video-level dataset (each video is a bag)
        self.video_data = []
        self.video_cls_ids = [[] for _ in range(self.num_classes)]

        for bag_idx, video_id in enumerate(video_ids):
            video_row = video_data[video_data['video_id'] == video_id].iloc[0]
            label = int(video_row['label'])
            category = video_row['category']

            self.video_data.append({
                'video_id': video_id,
                'label': label,
                'category': category
            })

            self.video_cls_ids[label].append(bag_idx)

        if print_info:
            self.summarize()

    def summarize(self):
        print("Video Dataset Summary:")
        print(f"Total videos (bags): {len(self.video_data)}")
        for i in range(self.num_classes):
            print(f"Class {i}: {len(self.video_cls_ids[i])} videos")

    def __len__(self):
        return len(self.video_data)

    def __getitem__(self, idx):
        bag = self.video_data[idx]
        video_id = bag['video_id']
        label = bag['label']

        # Load video features from .pt file
        feature_path = os.path.join(self.feature_dir, f'{video_id}.pt')

        if not os.path.exists(feature_path):
            raise FileNotFoundError(f"Feature file not found: {feature_path}")

        features = torch.load(feature_path)  # [N, feature_dim] where N is number of frames

        # Ensure features are float tensor
        if not isinstance(features, torch.Tensor):
            features = torch.from_numpy(features).float()
        else:
            features = features.float()

        # Create temporal coordinates (frame indices as 1D coords)
        # Convert to 2D for compatibility with spatial constraint code
        num_frames = features.shape[0]
        coords = np.zeros((num_frames, 2))
        coords[:, 0] = np.arange(num_frames)  # Frame index in x-coordinate
        # y-coordinate stays 0 (1D temporal data)

        # Create temporal nearest neighbors (consecutive frames)
        # For each frame, its nearest neighbors are the temporally adjacent frames
        nearest = np.zeros((num_frames, 3), dtype=np.int64)
        for i in range(num_frames):
            neighbors = []

            # Add previous frame
            if i > 0:
                neighbors.append(i - 1)

            # Add next frame
            if i < num_frames - 1:
                neighbors.append(i + 1)

            # Add second previous/next frame if needed
            if len(neighbors) < 3 and i > 1:
                neighbors.insert(0, i - 2)
            if len(neighbors) < 3 and i < num_frames - 2:
                neighbors.append(i + 2)

            # If still not enough (edge cases for very short videos), repeat closest
            while len(neighbors) < 3:
                if i > 0:
                    neighbors.insert(0, max(0, i - len(neighbors) - 1))
                elif i < num_frames - 1:
                    neighbors.append(min(num_frames - 1, i + len(neighbors) + 1))
                else:
                    # Video has only 1 frame - use itself
                    neighbors.append(i)

            nearest[i] = neighbors[:3]

        label = torch.tensor(label).long()

        return features, label, coords, nearest

    def return_splits(self, from_id=False, csv_path=None):
        """
        Return train/val/test splits based on split CSV
        """
        if from_id:
            raise NotImplementedError("from_id not implemented for video dataset")
        else:
            assert csv_path is not None, "Must provide csv_path for splits"
            all_splits = pd.read_csv(csv_path)
            train_split = self.get_split_from_df(all_splits, 'train')
            val_split = self.get_split_from_df(all_splits, 'val')
            test_split = self.get_split_from_df(all_splits, 'test')

        return train_split, val_split, test_split

    def get_split_from_df(self, all_splits, split_key='train'):
        """
        Get a specific split from DataFrame
        Args:
            all_splits: DataFrame with columns [video_id, label, train, val, test]
            split_key: 'train', 'val', or 'test'
        """
        # Get video_ids where split_key column is True
        split_video_ids = all_splits[all_splits[split_key] == True]['video_id'].values

        # Filter video_data for videos in this split
        split_data = [bag for bag in self.video_data if bag['video_id'] in split_video_ids]

        # Create new dataset
        split_dataset = Video_Split(split_data, self.feature_dir, self.num_classes)
        return split_dataset


class Video_Split(Dataset):
    def __init__(self, video_data, feature_dir, num_classes):
        self.video_data = video_data
        self.feature_dir = feature_dir
        self.num_classes = num_classes

        # Create class indices
        self.video_cls_ids = [[] for _ in range(num_classes)]
        for i, bag in enumerate(video_data):
            self.video_cls_ids[bag['label']].append(i)

    def __len__(self):
        return len(self.video_data)

    def __getitem__(self, idx):
        bag = self.video_data[idx]
        video_id = bag['video_id']
        label = bag['label']

        # Load video features from .pt file
        feature_path = os.path.join(self.feature_dir, f'{video_id}.pt')

        if not os.path.exists(feature_path):
            raise FileNotFoundError(f"Feature file not found: {feature_path}")

        features = torch.load(feature_path)

        # Ensure features are float tensor
        if not isinstance(features, torch.Tensor):
            features = torch.from_numpy(features).float()
        else:
            features = features.float()

        # Create temporal coordinates
        num_frames = features.shape[0]
        coords = np.zeros((num_frames, 2))
        coords[:, 0] = np.arange(num_frames)

        # Create temporal nearest neighbors
        nearest = np.zeros((num_frames, 3), dtype=np.int64)
        for i in range(num_frames):
            neighbors = []

            if i > 0:
                neighbors.append(i - 1)
            if i < num_frames - 1:
                neighbors.append(i + 1)
            if len(neighbors) < 3 and i > 1:
                neighbors.insert(0, i - 2)
            if len(neighbors) < 3 and i < num_frames - 2:
                neighbors.append(i + 2)

            while len(neighbors) < 3:
                if i > 0:
                    neighbors.insert(0, max(0, i - len(neighbors) - 1))
                elif i < num_frames - 1:
                    neighbors.append(min(num_frames - 1, i + len(neighbors) + 1))
                else:
                    neighbors.append(i)

            nearest[i] = neighbors[:3]

        label = torch.tensor(label).long()

        return features, label, coords, nearest
