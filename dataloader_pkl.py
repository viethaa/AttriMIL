"""
Dataloader for .pkl feature files (adapted from original dataloader.py)
"""
from __future__ import print_function, division
import os
import torch
import numpy as np
import pandas as pd
import pickle
from torch.utils.data import Dataset

class Generic_MIL_Dataset(Dataset):
    def __init__(self,
                 csv_path='dataset.csv',
                 data_dir=None,
                 shuffle=False,
                 seed=7,
                 print_info=True,
                 label_dict={},
                 patient_strat=False,
                 ignore=[]):
        """
        Args:
            csv_path (string): Path to the csv file with annotations.
            data_dir (string): Directory with all the feature .pkl files.
            shuffle (bool): Whether to shuffle the dataset
            seed (int): random seed for shuffling the data
            print_info (bool): Whether to print dataset info
            label_dict (dict): Dictionary mapping label names to integers
            patient_strat (bool): Whether to use patient-level stratification
            ignore (list): List of samples to ignore
        """
        self.data_dir = data_dir
        self.label_dict = label_dict

        # Read CSV
        slide_data = pd.read_csv(csv_path)

        # Remove ignored samples
        if len(ignore) > 0:
            slide_data = slide_data[~slide_data['patient'].isin(ignore)]

        # Map labels if label_dict provided
        if len(label_dict) > 0:
            slide_data['label'] = slide_data['class'].map(label_dict)

        # Get unique patients (bags)
        patients = slide_data['patient'].unique()

        if shuffle:
            np.random.seed(seed)
            np.random.shuffle(patients)

        # Determine number of classes
        if len(label_dict) > 0:
            self.num_classes = len(label_dict)
        else:
            self.num_classes = slide_data['label'].nunique()

        # Create bag-level dataset
        self.slide_data = []
        self.slide_cls_ids = [[] for _ in range(self.num_classes)]

        for bag_idx, patient_id in enumerate(patients):
            patient_data = slide_data[slide_data['patient'] == patient_id]
            label = patient_data['label'].iloc[0]
            instance_indices = patient_data['idx'].tolist()

            self.slide_data.append({
                'slide_id': patient_id,
                'label': label,
                'instance_indices': instance_indices
            })

            self.slide_cls_ids[label].append(bag_idx)

        if print_info:
            self.summarize()

    def summarize(self):
        print("Dataset Summary:")
        print(f"Total bags (patients): {len(self.slide_data)}")
        for i in range(self.num_classes):
            print(f"Class {i}: {len(self.slide_cls_ids[i])} bags")

    def __len__(self):
        return len(self.slide_data)

    def __getitem__(self, idx):
        bag = self.slide_data[idx]
        slide_id = bag['slide_id']
        label = bag['label']
        instance_indices = bag['instance_indices']

        # Load all instances for this bag
        features_list = []
        for inst_idx in instance_indices:
            pkl_path = os.path.join(self.data_dir, f'image_{inst_idx}.pkl')
            with open(pkl_path, 'rb') as f:
                feat = pickle.load(f)
                if isinstance(feat, torch.Tensor):
                    feat = feat.numpy()
                features_list.append(feat)

        # Stack into tensor [N, feature_dim]
        features = torch.from_numpy(np.stack(features_list)).float()

        # Create dummy coords (not used for video data but needed for compatibility)
        coords = np.zeros((len(features_list), 2))

        # Create dummy nearest neighbors (not used but needed for compatibility)
        nearest = np.zeros((len(features_list), 3), dtype=np.int64)
        for i in range(len(features_list)):
            neighbors = []
            for j in range(max(0, i-5), min(len(features_list), i+5)):
                if j != i:
                    neighbors.append(j)
                    if len(neighbors) >= 3:
                        break
            while len(neighbors) < 3:
                neighbors.append(min(i, len(features_list)-1))
            nearest[i] = neighbors[:3]

        label = torch.tensor(label).long()

        return features, label, coords, nearest

    def return_splits(self, from_id=False, csv_path=None):
        """
        Return train/val/test splits
        """
        if from_id:
            raise NotImplementedError()
        else:
            assert csv_path is not None
            all_splits = pd.read_csv(csv_path)
            train_split = self.get_split_from_df(all_splits, 'train')
            val_split = self.get_split_from_df(all_splits, 'val')
            test_split = self.get_split_from_df(all_splits, 'test')

        return train_split, val_split, test_split

    def get_split_from_df(self, all_splits, split_key='train'):
        """
        Get a specific split from DataFrame
        """
        split_patients = all_splits[split_key].dropna().unique()

        # Filter slide_data for patients in this split
        split_data = [bag for bag in self.slide_data if bag['slide_id'] in split_patients]

        # Create new dataset
        split_dataset = Generic_Split(split_data, self.data_dir, self.num_classes)
        return split_dataset


class Generic_Split(Dataset):
    def __init__(self, slide_data, data_dir, num_classes):
        self.slide_data = slide_data
        self.data_dir = data_dir
        self.num_classes = num_classes

        # Create class indices
        self.slide_cls_ids = [[] for _ in range(num_classes)]
        for i, bag in enumerate(slide_data):
            self.slide_cls_ids[bag['label']].append(i)

    def __len__(self):
        return len(self.slide_data)

    def __getitem__(self, idx):
        bag = self.slide_data[idx]
        slide_id = bag['slide_id']
        label = bag['label']
        instance_indices = bag['instance_indices']

        # Load all instances for this bag
        features_list = []
        for inst_idx in instance_indices:
            pkl_path = os.path.join(self.data_dir, f'image_{inst_idx}.pkl')
            with open(pkl_path, 'rb') as f:
                feat = pickle.load(f)
                if isinstance(feat, torch.Tensor):
                    feat = feat.numpy()
                features_list.append(feat)

        # Stack into tensor [N, feature_dim]
        features = torch.from_numpy(np.stack(features_list)).float()

        # Create dummy coords
        coords = np.zeros((len(features_list), 2))

        # Create dummy nearest neighbors
        nearest = np.zeros((len(features_list), 3), dtype=np.int64)
        for i in range(len(features_list)):
            neighbors = []
            for j in range(max(0, i-5), min(len(features_list), i+5)):
                if j != i:
                    neighbors.append(j)
                    if len(neighbors) >= 3:
                        break
            while len(neighbors) < 3:
                neighbors.append(min(i, len(features_list)-1))
            nearest[i] = neighbors[:3]

        label = torch.tensor(label).long()

        return features, label, coords, nearest


# Keep the same signature as original for compatibility
Generic_WSI_Classification_Dataset = Generic_MIL_Dataset
