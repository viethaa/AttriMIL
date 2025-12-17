#!/bin/bash
# Retry video downloads from Google Drive
# Run this script after waiting 30 minutes for rate limits to reset

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/data/video/raw_videos"

echo "=================================================="
echo "Retrying Video Download from Google Drive"
echo "=================================================="
echo ""
echo "Output directory: $OUTPUT_DIR"
echo ""

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Clean up empty subdirectories from previous failed attempt (but not the main directory)
echo "Cleaning up empty directories..."
find "$OUTPUT_DIR" -mindepth 1 -type d -empty -delete 2>/dev/null || true

# Retry download with resume option
echo ""
echo "Starting download (this may take a while)..."
echo ""

cd "$OUTPUT_DIR"
gdown --folder "https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN" --remaining-ok

cd "$PROJECT_ROOT"

# Count downloaded files
echo ""
echo "=================================================="
echo "Download Summary"
echo "=================================================="

for class in Adenoma Malignant Normal; do
    if [ -d "$OUTPUT_DIR/$class" ]; then
        count=$(find "$OUTPUT_DIR/$class" -name "*.avi" -o -name "*.mp4" | wc -l | tr -d ' ')
        echo "$class: $count videos"
    elif [ -d "$OUTPUT_DIR/dataset2/$class" ]; then
        count=$(find "$OUTPUT_DIR/dataset2/$class" -name "*.avi" -o -name "*.mp4" | wc -l | tr -d ' ')
        echo "$class: $count videos (in dataset2/)"
    else
        echo "$class: Directory not found"
    fi
done

total=$(find "$OUTPUT_DIR" -name "*.avi" -o -name "*.mp4" | wc -l | tr -d ' ')
echo "=================================================="
echo "TOTAL: $total videos"
echo "=================================================="

if [ "$total" -lt 100 ]; then
    echo ""
    echo "⚠️  Warning: Only $total videos downloaded (expected ~200-300)"
    echo ""
    echo "If download failed again due to rate limits:"
    echo "1. Wait another 30 minutes and run this script again"
    echo "2. Or download manually from browser:"
    echo "   https://drive.google.com/drive/folders/1ciU4kWHoJOC7exF7x1n4JfAXub_A8UmN"
else
    echo ""
    echo "✓ Download appears successful!"
fi
