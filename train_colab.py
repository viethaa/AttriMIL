"""
Colab-ready training script for AttriMIL on video dataset
Automatically handles Google Drive mounting and environment configuration
"""
import os
import sys
import torch
import torch.optim as optim
import torch.nn.functional as F
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Import configuration
from config_env import get_env_config, print_config, is_colab

# Mount Google Drive if in Colab
if is_colab():
    print("Detected Google Colab environment")
    print("Mounting Google Drive...")
    from google.colab import drive
    drive.mount('/content/drive')
    print("✓ Google Drive mounted successfully")
else:
    print("Running in local environment")

# Get environment-specific config
config = get_env_config()
print_config(config)

# Import project modules
from dataloader_video import Video_MIL_Dataset
from models.AttriMIL import AttriMIL
from constraints import spatial_constraint, rank_constraint
from utils import *

# Set device
device = torch.device(
    "cuda" if torch.cuda.is_available() else
    ("mps" if torch.backends.mps.is_available() else "cpu")
)
print(f"\nUsing device: {device}")


class ColabCheckpointManager:
    """
    Manages checkpoints with periodic saves to Google Drive
    Prevents data loss during Colab disconnections
    """
    def __init__(self, save_dir, interval_minutes=30):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.interval_minutes = interval_minutes
        self.last_save_time = datetime.now()

    def should_save(self):
        """Check if enough time has passed for periodic save"""
        elapsed = (datetime.now() - self.last_save_time).total_seconds() / 60
        return elapsed >= self.interval_minutes

    def save_checkpoint(self, model, optimizer, epoch, metrics, name='checkpoint'):
        """Save model checkpoint to Drive"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        }

        # Save checkpoint
        checkpoint_path = self.save_dir / f'{name}_epoch_{epoch}.pt'
        torch.save(checkpoint, checkpoint_path)

        # Update latest checkpoint symlink
        latest_path = self.save_dir / f'{name}_latest.pt'
        torch.save(checkpoint, latest_path)

        self.last_save_time = datetime.now()
        print(f"✓ Checkpoint saved: {checkpoint_path}")

        return checkpoint_path

    def load_latest_checkpoint(self, model, optimizer=None):
        """Load the latest checkpoint if it exists"""
        latest_path = self.save_dir / 'checkpoint_latest.pt'

        if latest_path.exists():
            print(f"Loading checkpoint: {latest_path}")
            checkpoint = torch.load(latest_path, map_location=device)

            model.load_state_dict(checkpoint['model_state_dict'])
            if optimizer is not None:
                optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

            print(f"✓ Resumed from epoch {checkpoint['epoch']}")
            return checkpoint['epoch'], checkpoint['metrics']
        else:
            print("No existing checkpoint found, starting from scratch")
            return 0, {}


def train_epoch(model, loader, optimizer, epoch, config, checkpoint_mgr=None):
    """Train for one epoch"""
    model.train()
    train_loss = 0.
    train_error = 0.

    for batch_idx, (data, label, coords, nearest) in enumerate(loader):
        data, label = data.to(device), label.to(device)

        optimizer.zero_grad()

        # Forward pass
        logits, Y_prob, Y_hat, attribute_score, results_dict = model(data)

        # Classification loss
        loss = F.cross_entropy(logits, label)

        # Add spatial constraint loss
        if config['spatial_loss_weight'] > 0:
            spatial_loss = spatial_constraint(attribute_score, coords, nearest)
            loss += config['spatial_loss_weight'] * spatial_loss

        # Add ranking constraint loss
        if config['ranking_loss_weight'] > 0:
            ranking_loss = rank_constraint(attribute_score, label)
            loss += config['ranking_loss_weight'] * ranking_loss

        # Backward pass
        loss.backward()
        optimizer.step()

        # Track metrics
        train_loss += loss.item()
        error = calculate_error(Y_hat, label)
        train_error += error

        # Print progress
        if batch_idx % config['print_freq'] == 0:
            print(f'Epoch: {epoch}, Batch: {batch_idx}/{len(loader)}, '
                  f'Loss: {loss.item():.4f}, Error: {error:.4f}')

        # Periodic checkpoint save (Colab-specific)
        if checkpoint_mgr and checkpoint_mgr.should_save():
            metrics = {'train_loss': train_loss / (batch_idx + 1)}
            checkpoint_mgr.save_checkpoint(
                model, optimizer, epoch, metrics, name='periodic'
            )

    # Calculate average metrics
    train_loss /= len(loader)
    train_error /= len(loader)

    return train_loss, train_error


def validate(model, loader, config):
    """Validate model"""
    model.eval()
    val_loss = 0.
    val_error = 0.

    all_probs = []
    all_labels = []

    with torch.no_grad():
        for batch_idx, (data, label, coords, nearest) in enumerate(loader):
            data, label = data.to(device), label.to(device)

            logits, Y_prob, Y_hat, attribute_score, results_dict = model(data)

            loss = F.cross_entropy(logits, label)

            val_loss += loss.item()
            val_error += calculate_error(Y_hat, label)

            all_probs.append(Y_prob.cpu().numpy())
            all_labels.append(label.cpu().numpy())

    val_loss /= len(loader)
    val_error /= len(loader)

    return val_loss, val_error, np.concatenate(all_probs), np.concatenate(all_labels)


def main():
    """Main training function"""
    print("\n" + "="*60)
    print("Starting AttriMIL Training")
    print("="*60 + "\n")

    # Verify dataset paths exist
    print("Verifying dataset paths...")
    if not os.path.exists(config['csv_path']):
        raise FileNotFoundError(f"CSV file not found: {config['csv_path']}")
    if not os.path.exists(config['feature_dir']):
        raise FileNotFoundError(f"Feature directory not found: {config['feature_dir']}")
    print("✓ Dataset paths verified\n")

    # Initialize checkpoint manager for Colab
    checkpoint_mgr = None
    if config.get('use_drive_checkpoints', False):
        checkpoint_mgr = ColabCheckpointManager(
            config['save_dir'],
            interval_minutes=config.get('checkpoint_interval_minutes', 30)
        )

    # Load datasets (lazy loading - features loaded on-demand)
    print("Loading dataset metadata...")
    train_dataset = Video_MIL_Dataset(
        csv_path=config['csv_path'],
        feature_dir=config['feature_dir'],
        shuffle=True,
        seed=config['seed'],
        label_dict=config['label_dict']
    )

    val_dataset = Video_MIL_Dataset(
        csv_path=config['csv_path'],
        feature_dir=config['feature_dir'],
        shuffle=False,
        label_dict=config['label_dict']
    )

    # Create dataloaders (batch_size=1 for MIL)
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=1,
        shuffle=True,
        num_workers=0  # Set to 0 for Colab stability
    )

    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=0
    )

    print(f"✓ Loaded {len(train_dataset)} training videos")
    print(f"✓ Loaded {len(val_dataset)} validation videos\n")

    # Initialize model
    print("Initializing model...")
    model = AttriMIL(
        feature_dim=config['feature_dim'],
        n_classes=config['n_classes']
    ).to(device)

    optimizer = optim.Adam(
        model.parameters(),
        lr=config['learning_rate'],
        weight_decay=config['weight_decay']
    )

    print(f"✓ Model initialized with {count_parameters(model):,} parameters\n")

    # Try to resume from checkpoint
    start_epoch = 0
    best_val_loss = float('inf')
    if checkpoint_mgr:
        start_epoch, metrics = checkpoint_mgr.load_latest_checkpoint(model, optimizer)
        best_val_loss = metrics.get('best_val_loss', float('inf'))

    # Training loop
    print("Starting training loop...")
    print("="*60 + "\n")

    patience_counter = 0

    for epoch in range(start_epoch, config['max_epoch']):
        print(f"\n{'='*60}")
        print(f"Epoch {epoch + 1}/{config['max_epoch']}")
        print(f"{'='*60}")

        # Train
        train_loss, train_error = train_epoch(
            model, train_loader, optimizer, epoch, config, checkpoint_mgr
        )

        print(f"\nTrain - Loss: {train_loss:.4f}, Error: {train_error:.4f}")

        # Validate
        val_loss, val_error, val_probs, val_labels = validate(
            model, val_loader, config
        )

        print(f"Val   - Loss: {val_loss:.4f}, Error: {val_error:.4f}")

        # Save checkpoint if improved
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0

            if checkpoint_mgr:
                checkpoint_mgr.save_checkpoint(
                    model, optimizer, epoch,
                    {'train_loss': train_loss, 'val_loss': val_loss,
                     'best_val_loss': best_val_loss},
                    name='best'
                )
            print("✓ New best validation loss!")
        else:
            patience_counter += 1

        # Early stopping
        if (config['early_stopping'] and
            epoch >= config['min_epochs_before_early_stop'] and
            patience_counter >= config['early_stopping_patience']):
            print(f"\nEarly stopping triggered after {epoch + 1} epochs")
            break

        # Regular checkpoint save
        if (epoch + 1) % config['save_checkpoint_freq'] == 0:
            if checkpoint_mgr:
                checkpoint_mgr.save_checkpoint(
                    model, optimizer, epoch,
                    {'train_loss': train_loss, 'val_loss': val_loss},
                    name=f'epoch_{epoch+1}'
                )

    print("\n" + "="*60)
    print("Training completed!")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Models saved to: {config['save_dir']}")
    print("="*60 + "\n")


def count_parameters(model):
    """Count trainable parameters"""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def calculate_error(Y_hat, Y):
    """Calculate classification error"""
    error = 1. - Y_hat.float().eq(Y.float()).float().mean().item()
    return error


if __name__ == "__main__":
    main()
