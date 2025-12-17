#!/bin/bash
# Quick script to push AttriMIL code to GitHub

set -e

echo "=================================================="
echo "Pushing AttriMIL to GitHub"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "config_env.py" ]; then
    echo "❌ Error: Run this from AttriMIL project root"
    exit 1
fi

echo "✓ In correct directory"
echo ""

# Show what will be committed
echo "Files to commit:"
echo "---------------"
git status --short | head -20
echo ""

# Add all Colab and documentation files
echo "Adding files to git..."
git add config_env.py train_colab.py colab_train_attrimil.ipynb \
        COLAB_*.md DATASET_*.md DATASET_*.txt COMMIT_GUIDE.md \
        CODEBASE_STRUCTURE.md VIDEO_DOWNLOAD_STATUS.md \
        .gitignore data/ docs/ scripts/ results/

echo "✓ Files added"
echo ""

# Show what's staged
echo "Staged files:"
git diff --cached --name-only | head -30
echo ""

# Commit
echo "Creating commit..."
git commit -m "Add Google Colab support with Drive integration

Major changes:
- Add environment auto-detection (config_env.py)
- Add Colab training script with automatic Drive mounting
- Add Jupyter notebook for Colab (colab_train_attrimil.ipynb)
- Remove 92GB of local datasets (use Google Drive instead)
- Add comprehensive documentation (COLAB_*.md)
- Update gitignore to prevent large file commits
- Reorganize project structure (docs/, scripts/, results/)

Benefits:
- Train on free Colab GPU
- Stream data from Google Drive (no downloads needed)
- Auto-checkpoint to Drive every 30 min
- Resume training after disconnections
- Edit locally in VS Code/Warp, train in Colab

Setup: See COLAB_QUICKSTART.md for 5-minute guide
Space saved: 92GB local storage freed"

echo "✓ Commit created"
echo ""

# Push
echo "Pushing to GitHub..."
echo "You may need to enter your GitHub credentials"
echo ""

git push origin main

echo ""
echo "=================================================="
echo "✓ Successfully pushed to GitHub!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Verify on GitHub: https://github.com/YOUR_USERNAME/AttriMIL"
echo "2. Upload dataset to Google Drive: MyDrive/dataset2/"
echo "3. Open Colab and run notebook: colab_train_attrimil.ipynb"
echo ""
echo "See COLAB_QUICKSTART.md for complete instructions"
echo "=================================================="
