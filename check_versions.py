"""Check pandas versions to diagnose the StringDtype error"""
import pandas as pd
import joblib
import sys
import os

# Import the FeatureSelector class from train_and_save_model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from train_and_save_model import FeatureSelector

print("=" * 60)
print("VERSION CHECK")
print("=" * 60)
print(f"Pandas version: {pd.__version__}")
print(f"Joblib version: {joblib.__version__}")

# Try to load the model and see the exact error
try:
    print("\nAttempting to load model...")
    pipeline = joblib.load('model_artifacts/hotel_booking_pipeline.pkl')
    print("✓ Model loaded successfully!")
    print(f"\nModel type: {type(pipeline)}")
    print(f"Pipeline steps: {pipeline.named_steps.keys()}")
except FileNotFoundError:
    print("✗ Model file not found!")
    print("\nThe model hasn't been trained yet.")
    print("Solution: Train the model first.")
    print("\nRun: python train_and_save_model.py")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    print(f"\nError type: {type(e).__name__}")
    
    # Check if it's the StringDtype issue
    if "StringDtype" in str(e):
        print("\n" + "=" * 60)
        print("DIAGNOSIS: Pandas Version Mismatch")
        print("=" * 60)
        print("\nThe model was saved with a different pandas version.")
        print("Solution: Retrain the model with your current pandas version.")
        print("\nRun: python train_and_save_model.py")
    elif "FeatureSelector" in str(e):
        print("\n" + "=" * 60)
        print("DIAGNOSIS: Custom Class Import Issue")
        print("=" * 60)
        print("\nThe model contains a custom FeatureSelector class.")
        print("This should be fixed now. If error persists, retrain the model.")
        print("\nRun: python train_and_save_model.py")

# Made with Bob
