# 🚀 GitHub Push & Streamlit Cloud Deployment Guide

## Step 1: Verify .gitignore

Your `.gitignore` already excludes large files. Let's verify:

```bash
cat .gitignore
```

Should include:
- `*.csv` (dataset)
- `model_artifacts/` (trained models)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)

✅ This is already set up correctly!

---

## Step 2: Push to GitHub

### Initialize Git (if not already done):
```bash
git init
git add .
git commit -m "Add hotel booking prediction app"
```

### Connect to GitHub:
```bash
# Replace YOUR_USERNAME and YOUR_REPO with your actual GitHub username and repo name
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Or if repo already exists:
```bash
git add .
git commit -m "Add Streamlit deployment files"
git push
```

---

## Step 3: Handle the Dataset

Since `hotel_bookings.csv` is excluded by `.gitignore`, you have 3 options:

### Option A: Upload to Google Drive (Recommended)
1. Upload `hotel_bookings.csv` to Google Drive
2. Get shareable link
3. Update `train_and_save_model.py` to download from URL

### Option B: Use Streamlit Secrets
1. In Streamlit Cloud, go to app settings
2. Add dataset path in secrets
3. Upload dataset through Streamlit interface

### Option C: Use GitHub Release
1. Create a GitHub release
2. Attach `hotel_bookings.csv` as release asset
3. Download in code from release URL

**For now, we'll use Option A (Google Drive) - easiest!**

---

## Step 4: Modify Code to Download Dataset

I'll create a version that downloads the dataset automatically:

### Create `download_data.py`:
```python
import os
import requests
import pandas as pd

def download_dataset(url, filepath='hotel_bookings.csv'):
    """Download dataset from URL if not exists"""
    if os.path.exists(filepath):
        print(f"✓ Dataset already exists: {filepath}")
        return filepath
    
    print(f"Downloading dataset from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Dataset downloaded: {filepath}")
        return filepath
    except Exception as e:
        print(f"✗ Error downloading dataset: {e}")
        raise

# Google Drive direct download link format:
# https://drive.google.com/uc?export=download&id=FILE_ID
DATASET_URL = "YOUR_GOOGLE_DRIVE_LINK_HERE"

if __name__ == "__main__":
    download_dataset(DATASET_URL)
```

---

## Step 5: Deploy to Streamlit Cloud

### 1. Go to Streamlit Cloud:
https://share.streamlit.io/

### 2. Sign in with GitHub

### 3. Click "New app"

### 4. Configure:
- **Repository:** YOUR_USERNAME/YOUR_REPO
- **Branch:** main
- **Main file path:** app.py

### 5. Advanced Settings (Optional):
- **Python version:** 3.9 or 3.10 (not 3.11+ due to pandas compatibility)
- **Secrets:** Add dataset URL if using secrets

### 6. Click "Deploy"!

---

## Step 6: First Deployment Will Fail (Expected!)

**Why?** Because the model doesn't exist yet.

### Fix:
1. In Streamlit Cloud logs, you'll see: "Model files not found"
2. This is expected - we need to train the model first
3. Two options:

#### Option A: Train on Streamlit Cloud
- SSH into Streamlit Cloud (not available)
- Use Streamlit's file uploader to upload pre-trained model

#### Option B: Modify app.py to train on first run
- Add auto-training logic
- Model trains automatically on first deployment

**Let's use Option B - I'll modify the code!**

---

## Step 7: Auto-Training on First Run

I'll update `app.py` to automatically train the model if it doesn't exist.

This way:
1. Push code to GitHub
2. Deploy to Streamlit Cloud
3. App automatically trains model on first run
4. Subsequent runs use the cached model

---

## 🎯 Quick Commands Summary

```bash
# 1. Check what will be pushed
git status

# 2. Add all files (respects .gitignore)
git add .

# 3. Commit
git commit -m "Add hotel booking prediction app with Streamlit"

# 4. Push to GitHub
git push origin main

# 5. Go to Streamlit Cloud and deploy!
```

---

## 📋 Checklist Before Pushing

- [ ] `.gitignore` excludes `*.csv` and `model_artifacts/`
- [ ] `requirements.txt` has all dependencies
- [ ] `app.py` is the main file
- [ ] `README.md` has instructions
- [ ] Dataset is uploaded to Google Drive (or will be handled separately)

---

## 🆘 Troubleshooting

### "File too large" error:
- Check `.gitignore` includes `*.csv`
- Run: `git rm --cached hotel_bookings.csv`
- Commit and push again

### "Module not found" on Streamlit Cloud:
- Check `requirements.txt` has all packages
- Verify Python version compatibility

### "Model not found" error:
- Expected on first run
- Will be fixed with auto-training code

---

## 🎉 After Deployment

Once deployed, you'll get a URL like:
```
https://YOUR_USERNAME-hotel-booking.streamlit.app
```

Share this URL with anyone to use your app! 🚀

---

## 📝 Next Steps After Pushing

1. I'll modify `app.py` to auto-train on first run
2. You push the updated code
3. Streamlit Cloud will automatically redeploy
4. App will train model and work perfectly!

Ready to push? Let me know when you've pushed to GitHub!