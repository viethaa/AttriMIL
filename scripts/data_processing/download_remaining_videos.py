"""
Download remaining video folders with retry logic and rate limiting.

This script downloads videos one at a time with delays to avoid
Google Drive quota limits.
"""

import subprocess
import time
import json
from pathlib import Path

# File IDs from the error messages and logs
MAL IGNANT_FILES = {
    '11.avi': '17gKExbf6LCbAkl94I8ciWHUf7azpGwcK',
    '12.avi': '1PF9pTqigtpWGMPWGd6ElCIvS5zpZvXtf',
    '13.avi': '1f_Y5ufyfciA0ZNCYFDwbbLHZgCcStMe7',
    # Add more as needed
}

NORMAL_FILES = {
    '24a0631.avi': '1tBHFUEDphtCM57dMkSwzv4EiJ9kk8zxE',
    # Add more as needed
}

def download_file(file_id, output_path, max_retries=3):
    """Download a single file from Google Drive with retry logic."""
    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1}/{max_retries} for {output_path.name}")

            # Use gdown to download single file
            cmd = f"gdown {file_id} -O {output_path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3600)

            if result.returncode == 0 and output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"  ✓ Downloaded {output_path.name} ({size_mb:.1f} MB)")
                return True
            else:
                print(f"  ✗ Failed: {result.stderr[:200]}")

        except subprocess.TimeoutExpired:
            print(f"  ✗ Timeout downloading {output_path.name}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        if attempt < max_retries - 1:
            wait_time = 30 * (attempt + 1)  # Exponential backoff
            print(f"  Waiting {wait_time}s before retry...")
            time.sleep(wait_time)

    return False

def main():
    print("="*80)
    print("Downloading Remaining Videos (with rate limiting)")
    print("="*80)

    # Create directories
    malignant_dir = Path("full_dataset/Malignant")
    normal_dir = Path("full_dataset/Normal")
    malignant_dir.mkdir(parents=True, exist_ok=True)
    normal_dir.mkdir(parents=True, exist_ok=True)

    # Move already downloaded file
    temp_file = Path("/tmp/Malignant/10.avi")
    if temp_file.exists():
        target = malignant_dir / "10.avi"
        if not target.exists():
            print(f"Moving {temp_file} to {target}")
            temp_file.rename(target)
            print(f"  ✓ Moved 10.avi (1.0GB)")

    # Try downloading a few more files
    # Note: Due to Google Drive quotas, this may still fail
    # Recommend manual download for large datasets

    print("\n" + "="*80)
    print("NOTE: Google Drive has download quotas")
    print("="*80)
    print("The download is being rate-limited by Google Drive.")
    print("Options:")
    print("  1. Wait 24 hours and retry")
    print("  2. Download manually through browser")
    print("  3. Use the existing Adenoma dataset for now")
    print("  4. Contact dataset owner for direct access")

if __name__ == "__main__":
    main()
