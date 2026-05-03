"""
Train and Save Hotel Booking Cancellation Prediction Model
This script trains the SVM model and saves it for deployment
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import VarianceThreshold, mutual_info_classif


class FeatureSelector(BaseEstimator, TransformerMixin):
    """Custom feature selector combining variance threshold, correlation filter, and mutual information"""
    
    def __init__(self, vt_threshold=0.01, corr_threshold=0.9, mi_threshold=0.01):
        self.vt_threshold = vt_threshold
        self.corr_threshold = corr_threshold
        self.mi_threshold = mi_threshold

    def fit(self, X, y):
        # Convert to array safely
        X = np.array(X)

        # Variance threshold
        self.vt = VarianceThreshold(self.vt_threshold)
        X_vt = self.vt.fit_transform(X)

        # Correlation filter
        corr = np.corrcoef(X_vt, rowvar=False)
        
        self.to_drop = set()
        for i in range(corr.shape[0]):
            for j in range(i+1, corr.shape[1]):
                if abs(corr[i, j]) > self.corr_threshold:
                    self.to_drop.add(j)

        keep_mask = np.array([i not in self.to_drop for i in range(X_vt.shape[1])])
        X_corr = X_vt[:, keep_mask]

        # Mutual information
        mi = mutual_info_classif(X_corr, y, random_state=42)
        self.mi_mask = mi > self.mi_threshold
        self.keep_mask = keep_mask

        return self

    def transform(self, X):
        X = np.array(X)
        X_vt = self.vt.transform(X)
        X_corr = X_vt[:, self.keep_mask]
        X_final = X_corr[:, self.mi_mask]
        return X_final


def load_and_prepare_data(filepath='hotel_bookings.csv'):
    """Load and prepare the dataset"""
    print("Loading data...")
    df = pd.read_csv(filepath)
    
    # Remove rows with missing target
    df = df.dropna(subset=['is_canceled'])
    
    # Separate features and target
    X = df.drop(['is_canceled'], axis=1)
    y = df['is_canceled']
    
    # Remove non-predictive columns
    columns_to_drop = ['reservation_status', 'reservation_status_date']
    X = X.drop(columns=[col for col in columns_to_drop if col in X.columns], errors='ignore')
    
    return X, y


def create_pipeline(X_train):
    """Create the full preprocessing and modeling pipeline"""
    print("Creating pipeline...")
    
    # Identify numeric and categorical columns
    num_cols = X_train.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X_train.select_dtypes(include=["object"]).columns
    
    # Numeric pipeline
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    # Categorical pipeline
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    # Combine preprocessing
    preprocessor = ColumnTransformer([
        ("num", num_pipe, num_cols),
        ("cat", cat_pipe, cat_cols)
    ])
    
    # Full pipeline
    full_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("selector", FeatureSelector(
            vt_threshold=0.01,
            corr_threshold=0.9,
            mi_threshold=0.01
        )),
        ("pca", PCA(n_components=0.95, svd_solver="full")),
        ("svm", SVC(C=1, kernel="linear", class_weight="balanced", probability=True))
    ])
    
    return full_pipeline


def train_model(X_train, y_train, pipeline):
    """Train the model"""
    print("Training model...")
    pipeline.fit(X_train, y_train)
    print("Training completed!")
    return pipeline


def save_model_and_metadata(pipeline, X_train, filepath='model_artifacts'):
    """Save the trained model and necessary metadata using joblib for efficiency"""
    print("Saving model and metadata with joblib...")
    
    # Save the pipeline using joblib (more efficient for sklearn models)
    joblib.dump(pipeline, f'{filepath}/hotel_booking_pipeline.pkl', compress=3)
    
    # Save feature names for reference
    feature_info = {
        'numeric_features': list(X_train.select_dtypes(include=["int64", "float64"]).columns),
        'categorical_features': list(X_train.select_dtypes(include=["object"]).columns),
        'all_features': list(X_train.columns)
    }
    
    joblib.dump(feature_info, f'{filepath}/feature_info.pkl')
    
    print(f"✓ Model saved to {filepath}/hotel_booking_pipeline.pkl")
    print(f"✓ Feature info saved to {filepath}/feature_info.pkl")
    print(f"  (Using joblib with compression for optimal performance)")


def main():
    """Main execution function"""
    # Load data
    X, y = load_and_prepare_data('hotel_bookings.csv')
    
    # Split data
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Create pipeline
    pipeline = create_pipeline(X_train)
    
    # Train model
    trained_pipeline = train_model(X_train, y_train, pipeline)
    
    # Evaluate on test set
    print("\nEvaluating model...")
    test_score = trained_pipeline.score(X_test, y_test)
    print(f"Test Accuracy: {test_score:.4f}")
    
    # Save model
    import os
    os.makedirs('model_artifacts', exist_ok=True)
    save_model_and_metadata(trained_pipeline, X_train, 'model_artifacts')
    
    print("\n✓ Model training and saving completed successfully!")


if __name__ == "__main__":
    main()

