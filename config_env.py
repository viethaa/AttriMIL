"""
Environment-aware configuration for AttriMIL
Automatically detects environment (local Mac, Colab, etc.) and sets paths accordingly
"""
import os
from pathlib import Path


def is_colab():
    """Detect if running in Google Colab"""
    try:
        import google.colab
        return True
    except ImportError:
        return False


def get_env_config():
    """
    Get environment-specific configuration

    Returns:
        dict: Configuration dictionary with all paths and settings
    """
    config = {}

    # Detect environment
    config['is_colab'] = is_colab()
    config['device_type'] = 'colab' if config['is_colab'] else 'local'

    # ========================
    # DATASET PATHS
    # ========================
    if config['is_colab']:
        # Google Colab with Drive mounted
        # Dataset is in /content/drive/MyDrive/dataset2
        DRIVE_ROOT = Path('/content/drive/MyDrive')
        DATASET_ROOT = DRIVE_ROOT / 'dataset2'
        PROJECT_ROOT = DRIVE_ROOT / 'AttriMIL'  # GitHub repo synced to Drive

        config['dataset_root'] = str(DATASET_ROOT)
        config['csv_path'] = str(DATASET_ROOT / 'video_data' / 'video_dataset.csv')
        config['feature_dir'] = str(DATASET_ROOT / 'video_features')
        config['split_path'] = str(DATASET_ROOT / 'video_data' / 'splits')

        # Save outputs to Drive (persists across Colab sessions)
        config['save_dir'] = str(PROJECT_ROOT / 'results' / 'models' / 'video_attrimil')
        config['log_dir'] = str(PROJECT_ROOT / 'results' / 'logs' / 'video_attrimil')

    else:
        # Local Mac environment
        # Use relative paths or environment variable
        PROJECT_ROOT = Path(os.environ.get('ATTRIMIL_ROOT', os.getcwd()))

        config['dataset_root'] = str(PROJECT_ROOT / 'data' / 'full_dataset')
        config['csv_path'] = str(PROJECT_ROOT / 'data' / 'video' / 'video_data' / 'video_dataset.csv')
        config['feature_dir'] = str(PROJECT_ROOT / 'data' / 'features' / 'video_features')
        config['split_path'] = str(PROJECT_ROOT / 'data' / 'video' / 'video_data' / 'splits')

        # Save locally
        config['save_dir'] = str(PROJECT_ROOT / 'results' / 'models' / 'video_attrimil')
        config['log_dir'] = str(PROJECT_ROOT / 'results' / 'logs' / 'video_attrimil')

    # Create directories if they don't exist
    os.makedirs(config['save_dir'], exist_ok=True)
    os.makedirs(config['log_dir'], exist_ok=True)

    # ========================
    # DATASET SETTINGS
    # ========================
    config['label_dict'] = {'Normal': 0, 'Adenoma': 1, 'Malignant': 2}
    config['n_classes'] = 3
    config['seed'] = 1

    # ========================
    # MODEL SETTINGS
    # ========================
    config['feature_dim'] = 2048  # ResNet50 features

    # ========================
    # TRAINING SETTINGS
    # ========================
    config['max_epoch'] = 150
    config['learning_rate'] = 2e-4
    config['momentum'] = 0.9
    config['weight_decay'] = 1e-5

    # Early stopping
    config['early_stopping'] = True
    config['early_stopping_patience'] = 20
    config['min_epochs_before_early_stop'] = 50

    # ========================
    # LOSS WEIGHTS
    # ========================
    config['spatial_loss_weight'] = 1.0
    config['ranking_loss_weight'] = 5.0

    # ========================
    # LOGGING SETTINGS
    # ========================
    config['writer_flag'] = True
    config['save_checkpoint_freq'] = 10
    config['print_freq'] = 20

    # ========================
    # CROSS-VALIDATION
    # ========================
    config['num_folds'] = 1
    config['run_specific_fold'] = None

    # ========================
    # COLAB-SPECIFIC SETTINGS
    # ========================
    if config['is_colab']:
        config['use_drive_checkpoints'] = True
        config['checkpoint_interval_minutes'] = 30  # Save every 30 min
        config['auto_disconnect_hours'] = 11  # Warn before 12h disconnect

    return config


def print_config(config):
    """Print configuration summary"""
    print("="*60)
    print("AttriMIL Configuration")
    print("="*60)
    print(f"Environment: {config['device_type']}")
    print(f"Running in Colab: {config['is_colab']}")
    print()
    print("Dataset Paths:")
    print(f"  Dataset Root: {config['dataset_root']}")
    print(f"  CSV Path: {config['csv_path']}")
    print(f"  Feature Dir: {config['feature_dir']}")
    print(f"  Split Path: {config['split_path']}")
    print()
    print("Output Paths:")
    print(f"  Save Dir: {config['save_dir']}")
    print(f"  Log Dir: {config['log_dir']}")
    print()
    print("Training Settings:")
    print(f"  Max Epochs: {config['max_epoch']}")
    print(f"  Learning Rate: {config['learning_rate']}")
    print(f"  Early Stopping: {config['early_stopping']}")
    print("="*60)


# Create a default config instance
DEFAULT_CONFIG = get_env_config()


if __name__ == "__main__":
    # Test configuration
    config = get_env_config()
    print_config(config)
