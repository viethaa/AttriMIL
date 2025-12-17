"""
Trainer for AttriMIL on video polyp classification dataset (3-class: Normal, Adenoma, Malignant)
"""
from dataloader_video import Video_MIL_Dataset

import os
import torch
from torch import nn
import torch.optim as optim
import torch.nn.functional as F

import pandas as pd
import numpy as np

from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.metrics import auc as calc_auc

from models.AttriMIL import AttriMIL
from utils import *

from constraints import spatial_constraint, rank_constraint
import queue
import config_video as config

device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))


class Accuracy_Logger(object):
    """Accuracy logger"""
    def __init__(self, n_classes):
        super().__init__()
        self.n_classes = n_classes
        self.initialize()

    def initialize(self):
        self.data = [{"count": 0, "correct": 0} for i in range(self.n_classes)]

    def log(self, Y_hat, Y):
        Y_hat = int(Y_hat)
        Y = int(Y)
        self.data[Y]["count"] += 1
        self.data[Y]["correct"] += (Y_hat == Y)

    def log_batch(self, Y_hat, Y):
        Y_hat = np.array(Y_hat).astype(int)
        Y = np.array(Y).astype(int)
        for label_class in np.unique(Y):
            cls_mask = Y == label_class
            self.data[label_class]["count"] += cls_mask.sum()
            self.data[label_class]["correct"] += (Y_hat[cls_mask] == Y[cls_mask]).sum()

    def get_summary(self, c):
        count = self.data[c]["count"]
        correct = self.data[c]["correct"]

        if count == 0:
            acc = None
        else:
            acc = float(correct) / count

        return acc, correct, count

def summary(model, loader, n_classes):
    acc_logger = Accuracy_Logger(n_classes=n_classes)
    model.eval()
    test_loss = 0.
    test_error = 0.

    all_probs = np.zeros((len(loader), n_classes))
    all_labels = np.zeros(len(loader))

    slide_ids = [bag['video_id'] for bag in loader.dataset.video_data]
    patient_results = {}

    for batch_idx, (data, label, coords, nearest) in enumerate(loader):
        data, label = data.to(device), label.to(device)
        slide_id = slide_ids[batch_idx]
        with torch.inference_mode():
            logits, Y_prob, Y_hat, attribute_score, results_dict = model(data)
        Y_hat = torch.topk(logits.view(1, -1), 1, dim = 1)[1]
        acc_logger.log(Y_hat, label)

        probs = Y_prob.cpu().numpy()
        all_probs[batch_idx] = probs
        all_labels[batch_idx] = label.item()

        patient_results.update({slide_id: {'slide_id': np.array(slide_id), 'prob': probs, 'label': label.item()}})
        error = calculate_error(Y_hat, label)
        test_error += error

    test_error /= len(loader)

    if n_classes == 2:
        auc = roc_auc_score(all_labels, all_probs[:, 1])
        aucs = []
    else:
        aucs = []
        binary_labels = label_binarize(all_labels, classes=[i for i in range(n_classes)])
        for class_idx in range(n_classes):
            if class_idx in all_labels:
                fpr, tpr, _ = roc_curve(binary_labels[:, class_idx], all_probs[:, class_idx])
                aucs.append(calc_auc(fpr, tpr))
            else:
                aucs.append(float('nan'))

        auc = np.nanmean(np.array(aucs))

    return patient_results, test_error, auc, acc_logger


def train(datasets, cur, args):
    """
        train for a single fold
    """
    print('\nTraining Fold {}!'.format(cur))
    writer_dir = os.path.join(args.results_dir, str(cur))
    if not os.path.isdir(writer_dir):
        os.makedirs(writer_dir, exist_ok=True)

    if args.log_data:
        from tensorboardX import SummaryWriter
        writer = SummaryWriter(writer_dir, flush_secs=15)
    else:
        writer = None

    print('\nInit train/val/test splits...', end=' ')
    train_split, val_split, test_split = datasets
    print('Done!')
    print("Training on {} samples".format(len(train_split)))
    print("Validating on {} samples".format(len(val_split)))
    print("Testing on {} samples".format(len(test_split)))

    print('\nInit loss function...', end=' ')
    loss_fn = nn.CrossEntropyLoss()
    print('Done!')

    print('\nInit Model...', end=' ')
    model = AttriMIL(dim=args.feature_dim, n_classes=args.n_classes)
    model.to(device)
    print('Done!')
    print_network(model)

    print('\nInit optimizer ...', end=' ')
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()),
                          lr=args.lr, weight_decay=args.reg)
    print('Done!')

    print('\nInit Loaders...', end=' ')
    train_loader = get_split_loader(train_split, training=True, weighted = args.weighted_sample)
    val_loader = get_split_loader(val_split)
    test_loader = get_split_loader(test_split)
    print('Done!')

    print('\n')
    mini_loss = 10000
    retain = 0

    for epoch in range(args.max_epochs):
        train_loop(epoch, model, train_loader, optimizer, args.n_classes, writer, loss_fn)
        val_loss = validate(cur, epoch, model, val_loader, args.n_classes, writer, loss_fn, args.results_dir)

        # Early stopping logic
        if val_loss < mini_loss:
            print("loss decrease from:{} to {}".format(mini_loss, val_loss))
            torch.save(model.state_dict(), os.path.join(args.results_dir, "s_{}_checkpoint.pt".format(cur)))
            mini_loss = val_loss
            retain = 0
        else:
            retain += 1
            print("Retain of early stopping: {} / {}".format(retain, args.early_stopping_patience))

        if retain > args.early_stopping_patience and epoch > 50:
            print("Early stopping")
            break

    if args.log_data:
        writer.close()

    print('\nTesting on hold-out test set...')
    model.load_state_dict(torch.load(os.path.join(args.results_dir, "s_{}_checkpoint.pt".format(cur))))
    results, test_error, test_auc, acc_logger = summary(model, test_loader, args.n_classes)

    print('Test error: {:.4f}, Test AUC: {:.4f}'.format(test_error, test_auc))

    for i in range(args.n_classes):
        acc, correct, count = acc_logger.get_summary(i)
        print('Class {}: acc {:.4f}, correct {}/{}'.format(i, acc, correct, count))

    return results, test_auc, 1-test_error, acc_logger


def train_loop(epoch, model, loader, optimizer, n_classes, writer=None, loss_fn=None):
    device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
    model.train()
    acc_logger = Accuracy_Logger(n_classes=n_classes)
    train_loss = 0.
    train_error = 0.

    print('\n')

    # Initialize ranking constraint queues
    label_positive_list = []
    label_negative_list = []
    for i in range(n_classes):
        label_positive_list.append(queue.Queue(maxsize=4))
        label_negative_list.append(queue.Queue(maxsize=4))

    for batch_idx, (data, label, coords, nearest) in enumerate(loader):
        data, label = data.to(device), label.to(device)
        coords = coords.float().to(device) if isinstance(coords, torch.Tensor) else torch.from_numpy(coords).float().to(device)
        nearest = nearest.long().to(device) if isinstance(nearest, torch.Tensor) else torch.from_numpy(nearest).long().to(device)

        logits, Y_prob, Y_hat, attribute_score, results_dict = model(data)

        acc_logger.log(Y_hat, label)
        loss_bag = loss_fn(logits, label)

        loss_spa = spatial_constraint(attribute_score, n_classes, nearest, ks=3)
        loss_rank, label_positive_list, label_negative_list = rank_constraint(
            data, label, model, attribute_score, n_classes, label_positive_list, label_negative_list
        )

        loss = loss_bag + config.spatial_loss_weight * loss_spa + config.ranking_loss_weight * loss_rank

        train_loss += loss.item()
        error = calculate_error(Y_hat, label)
        train_error += error

        # backward pass
        loss.backward()
        # step
        optimizer.step()
        optimizer.zero_grad()

    # calculate loss and error for epoch
    train_loss /= len(loader)
    train_error /= len(loader)

    print('Epoch: {}, train_loss: {:.4f}, train_error: {:.4f}'.format(epoch, train_loss, train_error))
    for i in range(n_classes):
        acc, correct, count = acc_logger.get_summary(i)
        print('Class {}: acc {:.4f}, correct {}/{}'.format(i, acc if acc is not None else 0, correct, count))
        if writer:
            writer.add_scalar('train/class_{}_acc'.format(i), acc, epoch)

    if writer:
        writer.add_scalar('train/loss', train_loss, epoch)
        writer.add_scalar('train/error', train_error, epoch)


def validate(cur, epoch, model, loader, n_classes, writer=None, loss_fn=None, results_dir=None):
    device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
    model.eval()
    acc_logger = Accuracy_Logger(n_classes=n_classes)
    val_loss = 0.
    val_error = 0.

    prob = np.zeros((len(loader), n_classes))
    labels = np.zeros(len(loader))

    with torch.inference_mode():
        for batch_idx, (data, label, coords, nearest) in enumerate(loader):
            data, label = data.to(device), label.to(device)

            logits, Y_prob, Y_hat, attribute_score, results_dict = model(data)

            acc_logger.log(Y_hat, label)

            loss_bag = loss_fn(logits, label)

            val_loss += loss_bag.item()

            prob[batch_idx] = Y_prob.cpu().numpy()
            labels[batch_idx] = label.item()

            error = calculate_error(Y_hat, label)
            val_error += error

    val_error /= len(loader)
    val_loss /= len(loader)

    if n_classes == 2:
        auc = roc_auc_score(labels, prob[:, 1])

    else:
        aucs = []
        binary_labels = label_binarize(labels, classes=[i for i in range(n_classes)])
        for class_idx in range(n_classes):
            if class_idx in labels:
                fpr, tpr, _ = roc_curve(binary_labels[:, class_idx], prob[:, class_idx])
                aucs.append(calc_auc(fpr, tpr))
            else:
                aucs.append(float('nan'))

        auc = np.nanmean(np.array(aucs))

    if writer:
        writer.add_scalar('val/loss', val_loss, epoch)
        writer.add_scalar('val/auc', auc, epoch)
        writer.add_scalar('val/error', val_error, epoch)

    print('\nVal Set, val_loss: {:.4f}, val_error: {:.4f}, auc: {:.4f}'.format(val_loss, val_error, auc))
    for i in range(n_classes):
        acc, correct, count = acc_logger.get_summary(i)
        print('Class {}: acc {:.4f}, correct {}/{}'.format(i, acc if acc is not None else 0, correct, count))

        if writer:
            writer.add_scalar('val/class_{}_acc'.format(i), acc, epoch)

    return val_loss


def seed_torch(seed=7):
    import random
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if device.type == 'cuda':
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

def save_splits(split_datasets, column_keys, filename):
    """Save train/val/test splits to CSV"""
    import pandas as pd
    splits_dict = {}
    for i, key in enumerate(column_keys):
        slide_ids = [bag['slide_id'] for bag in split_datasets[i].slide_data]
        splits_dict[key] = slide_ids

    # Pad to same length
    max_len = max([len(v) for v in splits_dict.values()])
    for key in splits_dict:
        splits_dict[key] = splits_dict[key] + [None] * (max_len - len(splits_dict[key]))

    df = pd.DataFrame(splits_dict)
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    # Create save directory
    os.makedirs(config.save_dir, exist_ok=True)

    # Set random seeds
    seed_torch(config.seed)

    # Create dataset
    print("Loading video dataset...")
    print(f"CSV path: {config.csv_path}")
    print(f"Feature dir: {config.data_dir}")
    dataset = Video_MIL_Dataset(
        csv_path=config.csv_path,
        feature_dir=config.data_dir,
        shuffle=False,
        seed=config.seed,
        print_info=True,
        label_dict=None,  # Labels already in CSV as integers (0, 1, 2)
        ignore=[]
    )

    # Get splits
    splits_csv = os.path.join(config.split_path, 'splits_0.csv')
    print(f"Splits CSV: {splits_csv}")
    train_dataset, val_dataset, test_dataset = dataset.return_splits(
        from_id=False,
        csv_path=splits_csv
    )

    datasets = (train_dataset, val_dataset, test_dataset)

    # Create args object for compatibility with existing code
    class Args:
        pass

    args = Args()
    args.results_dir = config.save_dir
    args.log_data = config.writer_flag
    args.drop_out = 0.25
    args.n_classes = config.n_classes
    args.feature_dim = config.feature_dim
    args.model_size = 'small'
    args.model_type = 'attrimil'
    args.lr = config.learning_rate
    args.reg = config.weight_decay
    args.max_epochs = config.max_epoch
    args.weighted_sample = False
    args.early_stopping_patience = config.early_stopping_patience

    print(f"\nTraining Configuration:")
    print(f"  Device: {device}")
    print(f"  Feature dim: {args.feature_dim}")
    print(f"  Num classes: {args.n_classes}")
    print(f"  Max epochs: {args.max_epochs}")
    print(f"  Learning rate: {args.lr}")
    print(f"  Weight decay: {args.reg}")
    print(f"  Spatial loss weight: {config.spatial_loss_weight}")
    print(f"  Ranking loss weight: {config.ranking_loss_weight}")

    # Training
    results, test_auc, test_acc, acc_logger = train(datasets, 0, args)

    print("\n" + "="*80)
    print("FINAL TEST RESULTS")
    print("="*80)
    print(f"Test AUC: {test_auc:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"\nPer-class results:")
    for i in range(config.n_classes):
        acc, correct, count = acc_logger.get_summary(i)
        class_names = ['Normal', 'Adenoma', 'Malignant']
        print(f'  Class {i} ({class_names[i]}): acc {acc:.4f}, correct {correct}/{count}')
    print("="*80)
