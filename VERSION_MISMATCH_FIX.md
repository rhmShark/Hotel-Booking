# 🔧 Fix: StringDtype Error (Pandas Version Mismatch)

## The Error

```
❌ Error loading model: StringDtype.__init__() takes from 1 to 2 positional arguments but 3 were given
```

## What This Means

This error occurs when:
1. **Model was trained** with pandas version X (e.g., 2.0.3)
2. **App is loading** with pandas version Y (e.g., 2.1.0 or 1.5.3)
3. Pandas changed how it handles string data types between versions
4. The saved model contains pandas-specific objects that are incompatible

## Why It Happens

- Pandas 2.0+ introduced a new `StringDtype` with different initialization
- When you save a model with pandas 2.0.3, it includes pandas objects
- If you load it with a different pandas version, those objects break
- This is a **serialization compatibility issue**

---

## ✅ Solution: Retrain with Current Pandas Version

The model needs to be trained with the **same pandas version** you're using to run the app.

### Step 1: Check Your Pandas Version

```bash
python check_versions.py
```

This will show:
- Your current pandas version
- Whether the model loads successfully
- Specific error details

### Step 2: Retrain the Model

Simply run the training script again with your current environment:

```bash
python train_and_save_model.py
```

This will:
- ✓ Use your current pandas version
- ✓ Save the model with compatible serialization
- ✓ Create new model files in `model_artifacts/`

### Step 3: Restart Streamlit

```bash
streamlit run app.py
```

The error should be gone! 🎉

---

## 🔍 Understanding the Issue

### What Gets Saved in the Model?

When you save the pipeline with `joblib.dump()`, it saves:
- ✓ The trained SVM model (sklearn)
- ✓ The preprocessing pipeline (sklearn)
- ✓ **Pandas DataFrame metadata** (column types, etc.)
- ✓ **Pandas-specific objects** (like StringDtype)

### Why Version Matters

```python
# Pandas 1.5.x
StringDtype()  # Takes 1 argument

# Pandas 2.0.x
StringDtype(storage="python")  # Takes 2 arguments

# Pandas 2.1.x
StringDtype(storage="python", na_value=pd.NA)  # Takes 3 arguments
```

When the saved model tries to recreate `StringDtype` objects, it uses the old signature, which fails with the new pandas version.

---

## 🛡️ Prevention: Lock Pandas Version

To avoid this in the future, update `requirements.txt` to lock the exact version:

```txt
pandas==2.0.3  # Lock to specific version
```

Or use version ranges:

```txt
pandas>=2.0.0,<2.1.0  # Allow minor updates only
```

---

## 🔄 Alternative Solutions

### Option 1: Downgrade Pandas (Not Recommended)

```bash
pip install pandas==2.0.3
```

Then restart the app without retraining.

**Cons:**
- May break other dependencies
- Not a long-term solution

### Option 2: Use Protocol 4 for Joblib (Experimental)

Modify `train_and_save_model.py`:

```python
# Instead of:
joblib.dump(pipeline, 'model_artifacts/hotel_booking_pipeline.pkl', compress=3)

# Use:
import pickle
joblib.dump(pipeline, 'model_artifacts/hotel_booking_pipeline.pkl', 
            compress=3, protocol=pickle.HIGHEST_PROTOCOL)
```

**Cons:**
- Still may have compatibility issues
- Not guaranteed to work

### Option 3: Save Model Without Pandas Objects (Best for Production)

Convert DataFrames to numpy arrays before training:

```python
# In train_and_save_model.py
X_train = X_train.values  # Convert to numpy
X_test = X_test.values
```

**Pros:**
- No pandas dependency in saved model
- Better cross-version compatibility

**Cons:**
- Requires code changes
- Loses column name information

---

## 📊 Quick Diagnosis

Run this to check your setup:

```bash
python check_versions.py
```

Expected output if working:
```
============================================================
VERSION CHECK
============================================================
Pandas version: 2.0.3
Joblib version: 1.3.2

Attempting to load model...
✓ Model loaded successfully!
```

Expected output if broken:
```
============================================================
VERSION CHECK
============================================================
Pandas version: 2.1.4
Joblib version: 1.3.2

Attempting to load model...
✗ Error loading model: StringDtype.__init__() takes from 1 to 2 positional arguments but 3 were given

Error type: TypeError

============================================================
DIAGNOSIS: Pandas Version Mismatch
============================================================

The model was saved with a different pandas version.
Solution: Retrain the model with your current pandas version.

Run: python train_and_save_model.py
```

---

## 🎯 Recommended Fix (3 Steps)

```bash
# 1. Check versions
python check_versions.py

# 2. Retrain model with current pandas
python train_and_save_model.py

# 3. Run app
streamlit run app.py
```

That's it! The model will now be compatible with your pandas version.

---

## 📝 For Deployment

When deploying to Streamlit Cloud:

1. **Lock pandas version** in `requirements.txt`:
   ```txt
   pandas==2.0.3
   ```

2. **Train model locally** with that version

3. **Commit model files** to git (or use Git LFS)

4. **Deploy** - Streamlit Cloud will use the same pandas version

This ensures consistency between training and deployment environments.

---

## 🆘 Still Not Working?

If retraining doesn't fix it:

1. **Delete old model files:**
   ```bash
   rm -rf model_artifacts/
   ```

2. **Clear Python cache:**
   ```bash
   find . -type d -name "__pycache__" -exec rm -rf {} +
   find . -type f -name "*.pyc" -delete
   ```

3. **Retrain:**
   ```bash
   python train_and_save_model.py
   ```

4. **Restart Streamlit:**
   ```bash
   streamlit run app.py
   ```

---

**Summary:** The error is caused by pandas version mismatch. Simply retrain the model with your current pandas version to fix it! 🚀