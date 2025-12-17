"""
Download CAMELYON16 pre-extracted features from Hugging Face
"""
from huggingface_hub import snapshot_download

print("Downloading CAMELYON16 features from Hugging Face...")
print("This may take a while depending on your internet connection...")

snapshot_download(
    repo_id='owkin/camelyon16-features',
    repo_type='dataset',
    local_dir='./camelyon16_features'
)

print("\n" + "="*80)
print("Download complete!")
print("Features saved to: ./camelyon16_features")
print("="*80)
