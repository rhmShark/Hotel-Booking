"""
Quick fix script to bypass venv issues and run with system Python
This script will:
1. Check if required packages are installed in system Python
2. Install missing packages if needed
3. Run the training script
"""

import subprocess
import sys

def check_and_install_package(package_name, import_name=None):
    """Check if package is installed, install if not"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f" {package_name} is already installed")
        return True
    except ImportError:
        print(f"  {package_name} not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package_name}")
            return False

def main():
    print("=" * 60)
    print("CHECKING AND INSTALLING REQUIRED PACKAGES")
    print("=" * 60)
    
    # List of required packages
    packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("joblib", "joblib"),
        ("streamlit", "streamlit"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("Pillow", "PIL"),
    ]
    
    all_installed = True
    for package_name, import_name in packages:
        if not check_and_install_package(package_name, import_name):
            all_installed = False
    
    print("\n" + "=" * 60)
    if all_installed:
        print("✓ ALL PACKAGES INSTALLED SUCCESSFULLY")
        print("=" * 60)
        print("\nNow running train_and_save_model.py...")
        print("-" * 60)
        
        # Run the training script
        try:
            subprocess.check_call([sys.executable, "train_and_save_model.py"])
            print("\n" + "=" * 60)
            print("✓ MODEL TRAINING COMPLETED!")
            print("=" * 60)
            print("\nNext step: Run the Streamlit app")
            print("Command: streamlit run app.py")
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Error running training script: {e}")
            sys.exit(1)
    else:
        print("✗ SOME PACKAGES FAILED TO INSTALL")
        print("=" * 60)
        print("\nPlease install them manually:")
        print("pip install pandas numpy scikit-learn joblib streamlit matplotlib seaborn Pillow")
        sys.exit(1)

if __name__ == "__main__":
    main()

