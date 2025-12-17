"""
Batch download videos from shared Google Drive to your own Drive in Colab
Works around rate limits by downloading in batches
"""
import os
import time
import gdown

# Configuration
SHARED_FOLDER_ID = "1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN"
OUTPUT_DIR = "/content/drive/MyDrive/dataset2"

# Class mapping
CLASSES = {
    "Adenoma": "1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN",  # Will need to get individual folder IDs
    "Malignant": "1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN",
    "Normal": "1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN"
}

def download_with_retry(url, output_path, max_retries=3, wait_time=60):
    """Download with retry logic for rate limits"""
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            gdown.download_folder(url=url, output=output_path, quiet=False, remaining_ok=True)
            print(f"✓ Downloaded successfully")
            return True
        except Exception as e:
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                if attempt < max_retries - 1:
                    print(f"⚠ Rate limit hit. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"✗ Failed after {max_retries} attempts")
                    return False
            else:
                print(f"✗ Error: {e}")
                return False

def main():
    print("="*60)
    print("Batch Video Download from Shared Drive")
    print("="*60)

    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Download entire folder
    print(f"\nDownloading from shared folder: {SHARED_FOLDER_ID}")
    print(f"Destination: {OUTPUT_DIR}")
    print("\nThis may take a while and might hit rate limits...")
    print("If rate limits are hit, the script will retry after waiting.\n")

    url = f"https://drive.google.com/drive/folders/{SHARED_FOLDER_ID}"
    success = download_with_retry(url, OUTPUT_DIR)

    if success:
        print("\n" + "="*60)
        print("Download Complete!")
        print("="*60)

        # Count files
        for class_name in ["Adenoma", "Malignant", "Normal"]:
            class_dir = os.path.join(OUTPUT_DIR, class_name)
            if os.path.exists(class_dir):
                video_count = len([f for f in os.listdir(class_dir)
                                  if f.endswith(('.avi', '.mp4', '.mov'))])
                print(f"✓ {class_name}: {video_count} videos")
            else:
                print(f"⚠ {class_name}: folder not found")
    else:
        print("\n" + "="*60)
        print("Download Failed - Rate Limit")
        print("="*60)
        print("\nOptions:")
        print("1. Wait 1-2 hours and run again")
        print("2. Use manual upload method instead")
        print("3. Contact the dataset owner for direct access")

if __name__ == "__main__":
    main()
