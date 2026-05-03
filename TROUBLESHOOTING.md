# 🔧 Troubleshooting Guide

## Error: "No module named 'pkg_resources'" or "Failed to build pandas"

This means your virtual environment is missing essential build tools.

### Solution (Run these commands in order):

```bash
# 1. Make sure you're in the virtual environment
source venv/Scripts/activate

# 2. Upgrade pip, setuptools, and wheel
python -m pip install --upgrade pip setuptools wheel

# 3. Now install requirements
pip install -r requirements.txt
```

### If that doesn't work, recreate the virtual environment:

```bash
# 1. Deactivate current venv
deactivate

# 2. Delete the old venv folder
rm -rf venv

# 3. Create a fresh virtual environment
python -m venv venv

# 4. Activate it
source venv/Scripts/activate

# 5. Upgrade pip, setuptools, and wheel FIRST
python -m pip install --upgrade pip setuptools wheel

# 6. Install requirements
pip install -r requirements.txt
```

---

## Complete Step-by-Step Fix

Copy and paste these commands one by one:

```bash
# Navigate to project (use quotes for spaces!)
cd "D:/FCDS/Syllabus/Spring 25-26/Data computation/Hotel-Booking"

# Remove old venv if it exists
rm -rf venv

# Create fresh virtual environment
python -m venv venv

# Activate it
source venv/Scripts/activate

# Upgrade pip and build tools
python -m pip install --upgrade pip setuptools wheel

# Install all requirements
pip install -r requirements.txt

# Verify installations
pip list
```

---

## Alternative: Install Packages Individually

If requirements.txt still fails, install packages one by one:

```bash
# Core packages first
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install scikit-learn==1.3.0
pip install joblib==1.3.2

# Streamlit
pip install streamlit==1.28.0

# Visualization
pip install matplotlib==3.7.2
pip install seaborn==0.12.2

# Additional
pip install Pillow==10.0.0
```

---

## Check Your Python Version

```bash
python --version
```

**Required:** Python 3.8 or higher

If you have an older version:
1. Download Python 3.9+ from [python.org](https://www.python.org/downloads/)
2. Install it
3. Use `python3` instead of `python` in commands

---

## Still Having Issues?

### Option 1: Use Conda Instead

```bash
# Create conda environment
conda create -n hotel-booking python=3.9

# Activate it
conda activate hotel-booking

# Install packages
conda install pandas numpy scikit-learn matplotlib seaborn
pip install streamlit joblib
```

### Option 2: Use System Python (Not Recommended)

```bash
# Install globally (skip venv)
pip install pandas numpy scikit-learn streamlit joblib matplotlib seaborn Pillow

# Run directly
python train_and_save_model.py
streamlit run app.py
```

---

## Verify Everything Works

After installation, test:

```bash
# Test Python imports
python -c "import pandas; import numpy; import sklearn; import streamlit; import joblib; print('All imports successful!')"

# If no errors, you're good to go!
```

---

## Quick Reference: Common Commands

```bash
# Check if venv is active (should show venv path)
which python

# List installed packages
pip list

# Check specific package
pip show pandas

# Reinstall a package
pip uninstall pandas
pip install pandas==2.0.3

# Clear pip cache
pip cache purge
```

---

## Next Steps After Fixing

Once packages are installed successfully:

```bash
# 1. Train the model
python train_and_save_model.py

# 2. Run the app
streamlit run app.py
```

---

**Still stuck? The issue might be:**
- Outdated Python version (need 3.8+)
- Corrupted pip cache
- Windows permissions issues
- Antivirus blocking installations

Try running your terminal as Administrator if nothing else works.