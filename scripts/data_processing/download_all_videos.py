#!/usr/bin/env python3
"""
Download all videos from Google Drive folder.

This script downloads videos from the Google Drive folder containing
colonoscopy videos organized by class (Adenoma, Malignant, Normal).

Google Drive folder: https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN

Usage:
    python download_all_videos.py --output-dir data/video/raw_videos
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


GOOGLE_DRIVE_FOLDER_ID = "1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN"
GOOGLE_DRIVE_URL = f"https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}"


def check_gdown_installed():
    """Check if gdown is installed."""
    try:
        subprocess.run(["gdown", "--version"],
                      capture_output=True,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_gdown():
    """Install gdown using pip."""
    print("Installing gdown...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "gdown"],
                  check=True)
    print("gdown installed successfully!")


def download_videos(output_dir, resume=True):
    """
    Download videos from Google Drive folder.

    Args:
        output_dir: Directory to save downloaded videos
        resume: Whether to resume interrupted downloads
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Downloading videos to: {output_path.absolute()}")
    print(f"Source: {GOOGLE_DRIVE_URL}")
    print("\nThis may take a while depending on your internet connection...")
    print("The folder contains approximately 200-300 videos organized by class.\n")

    # Change to output directory
    original_dir = os.getcwd()
    os.chdir(output_path)

    try:
        # Build gdown command
        cmd = ["gdown", "--folder", GOOGLE_DRIVE_URL]

        if resume:
            cmd.append("--remaining-ok")

        # Run download
        result = subprocess.run(cmd, check=False)

        if result.returncode != 0:
            print("\n⚠️  Download completed with some errors.")
            print("This is common with large folders due to rate limiting.")
            print("\nYou can:")
            print("1. Wait a few minutes and run the script again with --resume")
            print("2. Download files manually from the browser:")
            print(f"   {GOOGLE_DRIVE_URL}")
        else:
            print("\n✓ All videos downloaded successfully!")

    finally:
        os.chdir(original_dir)

    # Count downloaded files
    count_files(output_path)


def count_files(directory):
    """Count video files in directory by class."""
    directory = Path(directory)

    classes = ["Adenoma", "Malignant", "Normal"]
    total = 0

    print("\nDownload Summary:")
    print("=" * 50)

    for class_name in classes:
        class_dir = directory / class_name
        if class_dir.exists():
            files = list(class_dir.glob("*.avi")) + list(class_dir.glob("*.mp4"))
            count = len(files)
            total += count
            print(f"{class_name:12s}: {count:3d} videos")
        else:
            print(f"{class_name:12s}: Directory not found")

    print("=" * 50)
    print(f"{'TOTAL':12s}: {total:3d} videos")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Download all videos from Google Drive folder"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/video/raw_videos",
        help="Output directory for downloaded videos (default: data/video/raw_videos)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="Resume interrupted downloads (default: True)"
    )
    parser.add_argument(
        "--no-resume",
        action="store_false",
        dest="resume",
        help="Don't resume, download everything again"
    )

    args = parser.parse_args()

    # Check if gdown is installed
    if not check_gdown_installed():
        print("gdown is not installed.")
        response = input("Install gdown now? [y/N]: ").strip().lower()
        if response == 'y':
            install_gdown()
        else:
            print("Please install gdown: pip install gdown")
            return 1

    # Download videos
    try:
        download_videos(args.output_dir, args.resume)
        return 0
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        print("Run the script again with --resume to continue.")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
