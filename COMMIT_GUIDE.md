# Git Commit Guide

## Summary of Changes

### What Happened
1. ✅ **Removed 92GB of local datasets** - Now use Google Drive instead
2. ✅ **Added Colab training support** - Full integration with Google Drive
3. ✅ **Created documentation** - Complete setup guides
4. ✅ **Updated gitignore** - Prevent committing large files

---

## Files to Commit

### 1. Colab Integration Files (NEW)
```bash
git add config_env.py                    # Environment detection
git add train_colab.py                   # Colab training script
git add colab_train_attrimil.ipynb      # Jupyter notebook
```

### 2. Documentation (NEW)
```bash
git add COLAB_SETUP.md                   # Complete setup guide
git add COLAB_QUICKSTART.md              # 5-minute quick start
git add COLAB_CHECKLIST.md               # Setup checklist
git add COLAB_REFACTOR_SUMMARY.md        # What changed
git add CODEBASE_STRUCTURE.md            # Project structure
git add VIDEO_DOWNLOAD_STATUS.md         # Video download info
git add DATASET_CLEANUP_SUMMARY.md       # Cleanup summary
git add DATASET_REMOVED_MANIFEST.txt     # Removal log
git add COMMIT_GUIDE.md                  # This file
```

### 3. Data Organization (NEW/MODIFIED)
```bash
git add data/README.md                   # Data organization guide
git add data/full_dataset/README.md      # Empty dataset explanation
git add data/camelyon16/README.md        # Camelyon16 info (if exists)
git add data/video/                      # Metadata files (CSV only)
git add data/features/                   # Feature metadata
```

### 4. Updated Files (MODIFIED)
```bash
git add .gitignore                       # Added dataset ignore rules
```

### 5. Scripts Organization (NEW)
```bash
git add scripts/data_processing/         # Data scripts
git add scripts/results_extraction/      # Results scripts
git add scripts/utils/                   # Utility scripts
```

### 6. Documentation Folder (NEW)
```bash
git add docs/                            # Documentation from reorganization
```

### 7. Results Folder Structure (NEW - empty folders)
```bash
git add results/models/.gitkeep          # Keep directory structure
git add results/logs/.gitkeep            # Keep directory structure
```

---

## Commit Commands

### Option 1: All at Once
```bash
# Add all new and modified files
git add config_env.py train_colab.py colab_train_attrimil.ipynb \
        COLAB_*.md CODEBASE_STRUCTURE.md VIDEO_DOWNLOAD_STATUS.md \
        DATASET_*.md DATASET_*.txt COMMIT_GUIDE.md \
        .gitignore data/ docs/ scripts/ results/

# Commit
git commit -m "Add Google Colab support and clean up local datasets

Major changes:
- Add environment auto-detection (config_env.py)
- Add Colab training script with Drive integration
- Add comprehensive documentation and guides
- Remove 92GB of local datasets (use Google Drive instead)
- Update gitignore to prevent large file commits
- Reorganize project structure

Benefits:
- Train on free Colab GPU
- Stream data from Google Drive (no downloads)
- Auto-checkpoint to Drive every 30 min
- Resume training after disconnections
- Edit locally, train in Colab via GitHub sync

See COLAB_QUICKSTART.md for 5-minute setup guide."

# Push
git push origin main
```

### Option 2: Step by Step

**Step 1: Colab files**
```bash
git add config_env.py train_colab.py colab_train_attrimil.ipynb
git commit -m "Add Google Colab training support

- config_env.py: Auto-detect Colab vs local environment
- train_colab.py: Colab training script with Drive mounting
- colab_train_attrimil.ipynb: Jupyter notebook for Colab"
```

**Step 2: Documentation**
```bash
git add COLAB_*.md CODEBASE_STRUCTURE.md VIDEO_DOWNLOAD_STATUS.md
git commit -m "Add comprehensive Colab documentation

- COLAB_SETUP.md: Complete setup guide
- COLAB_QUICKSTART.md: 5-minute quick start
- COLAB_CHECKLIST.md: Step-by-step checklist
- COLAB_REFACTOR_SUMMARY.md: Summary of changes
- CODEBASE_STRUCTURE.md: Project organization
- VIDEO_DOWNLOAD_STATUS.md: Video download info"
```

**Step 3: Dataset cleanup**
```bash
git add .gitignore DATASET_*.md DATASET_*.txt data/
git commit -m "Clean up local datasets - use Google Drive instead

- Remove 92GB of local video and feature files
- Keep metadata CSV files (splits, dataset info)
- Add data/ README files explaining organization
- Update .gitignore to prevent large file commits
- Create cleanup manifest and summary

Space saved: 91.99 GB
Data location: Google Drive /MyDrive/dataset2/"
```

**Step 4: Project reorganization**
```bash
git add docs/ scripts/ results/
git commit -m "Reorganize project structure

- docs/: Documentation and guides
- scripts/: Organized utility scripts by purpose
- results/: Model checkpoints and logs directory"
```

**Step 5: Push all**
```bash
git push origin main
```

---

## Verification

### Before Pushing

**Check what will be committed:**
```bash
git status
```

**Check file sizes:**
```bash
# Should see only small files
git ls-files --others | xargs du -sh
```

**Verify no large files:**
```bash
# Should return empty
git status | grep -E "\.(avi|pt|pkl|parquet|h5)"
```

**Test locally:**
```bash
# Should detect local environment
python -c "from config_env import get_env_config, print_config; print_config(get_env_config())"
```

### After Pushing

**Verify on GitHub:**
1. Go to your repo on GitHub
2. Check files appear correctly
3. Verify `data/` folders are empty (only README)
4. Check `.gitignore` includes dataset patterns

---

## What NOT to Commit

These should be gitignored automatically:

❌ `*.avi` - Video files
❌ `*.pt` - Feature/checkpoint files
❌ `*.pkl` - Pickle files
❌ `*.parquet` - Parquet data files
❌ `data/full_dataset/*/` - Dataset directories
❌ `results/models/*.pt` - Model checkpoints
❌ Large binary files (>100MB)

If git tries to commit these, check your `.gitignore`!

---

## Troubleshooting

### "File too large" error

If you get an error about large files:

```bash
# Remove from staging
git reset HEAD path/to/large/file

# Add to .gitignore
echo "path/to/large/file" >> .gitignore

# Recommit
git add .gitignore
git commit --amend
```

### Accidentally committed large files

```bash
# Remove from history (BEFORE pushing)
git rm --cached path/to/large/file
git commit --amend

# If already pushed, use BFG Repo Cleaner
# See: https://rtyley.github.io/bfg-repo-cleaner/
```

### Want to undo everything

```bash
# Reset to last commit (keeps changes as uncommitted)
git reset HEAD~1

# Or discard all changes (CAREFUL!)
git reset --hard HEAD
```

---

## Next Steps After Commit

1. **Verify on GitHub:**
   - Check files uploaded correctly
   - No large files in repo

2. **Upload dataset to Google Drive:**
   ```bash
   rclone copy ./local_data/ gdrive:dataset2/ --progress
   ```

3. **Clone to Drive:**
   ```python
   # In Colab
   !cd /content/drive/MyDrive && \
    git clone https://github.com/YOUR_USERNAME/AttriMIL.git
   ```

4. **Start training:**
   - Follow `COLAB_QUICKSTART.md`
   - Upload notebook to Colab
   - Run training!

---

## Summary

**Ready to commit:**
- ✅ 6 new Colab files
- ✅ 9 documentation files
- ✅ Updated .gitignore
- ✅ Reorganized data/ folder (metadata only)
- ✅ Reorganized scripts/ and docs/
- ✅ Total: ~20-30 files, all small (<1MB each)

**Not committing:**
- ❌ Video files (92GB removed)
- ❌ Feature files
- ❌ Model checkpoints
- ❌ Large binary files

**Next:** Push to GitHub and set up Colab! 🚀
