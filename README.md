# 🏨 Hotel Booking Cancellation Prediction System

A machine learning-powered web application that predicts the likelihood of hotel booking cancellations using Support Vector Machine (SVM) algorithm.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Model Architecture](#model-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model Performance](#model-performance)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🎯 Overview

This application helps hotels predict booking cancellations by analyzing various booking characteristics such as:
- Lead time (days between booking and arrival)
- Guest information and history
- Room details and preferences
- Deposit type and payment information
- Market segment and distribution channel

## ✨ Features

- **Interactive Web Interface**: User-friendly Streamlit interface for easy data input
- **Real-time Predictions**: Instant cancellation risk assessment
- **Probability Scores**: Detailed breakdown of cancellation likelihood
- **Risk Level Indicators**: Visual representation of risk (Low/Medium/High)
- **Model Transparency**: Information about model architecture and performance

## 🧠 Model Architecture

### Pipeline Components:

1. **Data Preprocessing**
   - Missing value imputation (median for numeric, most frequent for categorical)
   - Standard scaling for numerical features
   - One-hot encoding for categorical features

2. **Feature Engineering**
   - Variance threshold filtering (removes low-variance features)
   - Correlation filtering (removes highly correlated features > 0.9)
   - Mutual information feature selection

3. **Dimensionality Reduction**
   - PCA (Principal Component Analysis) retaining 95% variance

4. **Classification Model**
   - Support Vector Machine (SVM) with linear kernel
   - Balanced class weights for handling imbalanced data
   - Probability estimates enabled

### Model Performance:
- **Accuracy**: ~71.6%
- **Training Data**: 87,396 hotel bookings
- **Features**: 29 booking characteristics

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Hotel-Booking
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## 📊 Usage

### Training the Model

Before running the application, you need to train and save the model:

```bash
python train_and_save_model.py
```

This will:
- Load the hotel bookings dataset
- Train the SVM model with the full pipeline
- Save the trained model to `model_artifacts/hotel_booking_pipeline.pkl`
- Save feature information to `model_artifacts/feature_info.pkl`

**Note**: Make sure you have the `hotel_bookings.csv` file in the project directory.

### Running the Web Application

Once the model is trained, launch the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Fill in Booking Details**: Use the sidebar to enter all booking information
   - Hotel type and arrival date
   - Guest information (adults, children, babies)
   - Stay duration (weekend and week nights)
   - Room preferences and special requests
   - Payment and deposit information

2. **Make Prediction**: Click the "🔮 Predict Cancellation Risk" button

3. **Review Results**: 
   - View the cancellation probability
   - Check the risk level (Low/Medium/High)
   - See the confidence breakdown

## 📁 Project Structure

```
Hotel-Booking/
│
├── app.py                          # Streamlit web application
├── train_and_save_model.py         # Model training script
├── practice_compute_final.ipynb    # Original analysis notebook
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── model_artifacts/                # Saved model files (created after training)
│   ├── hotel_booking_pipeline.pkl  # Trained model pipeline
│   └── feature_info.pkl            # Feature metadata
│
└── hotel_bookings.csv              # Dataset (not included in repo)
```

## 📈 Model Performance

### Classification Report (Test Set):
```
              precision    recall  f1-score   support

           0       0.89      0.70      0.78     12644
           1       0.49      0.77      0.60      4802

    accuracy                           0.72     17446
   macro avg       0.69      0.73      0.69     17446
weighted avg       0.78      0.72      0.73     17446
```

### Key Insights:
- The model performs better at identifying non-cancellations (class 0)
- Recall for cancellations (class 1) is 77%, meaning it catches most cancellations
- Balanced class weights help handle the imbalanced dataset

## 🌐 Deployment

### Local Deployment
Follow the [Usage](#usage) instructions above.

### Cloud Deployment Options

#### 1. Streamlit Cloud (Recommended for Streamlit apps)
```bash
# Push your code to GitHub
# Visit https://streamlit.io/cloud
# Connect your GitHub repository
# Deploy with one click
```

#### 2. Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### 3. Docker
```dockerfile
# Create Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🔧 Customization

### Modifying Model Parameters

Edit `train_and_save_model.py` to adjust:
- SVM hyperparameters (C, kernel, class_weight)
- Feature selection thresholds
- PCA variance retention
- Train/test split ratio

### Customizing the UI

Edit `app.py` to:
- Change color schemes and styling
- Add/remove input fields
- Modify prediction display format
- Add additional visualizations

## 📝 Input Features

The model uses the following 29 features:

**Booking Information:**
- hotel, lead_time, arrival_date_year, arrival_date_month
- arrival_date_week_number, arrival_date_day_of_month

**Stay Details:**
- stays_in_weekend_nights, stays_in_week_nights
- adults, children, babies

**Service Information:**
- meal, market_segment, distribution_channel
- reserved_room_type, assigned_room_type

**Guest History:**
- is_repeated_guest, previous_cancellations
- previous_bookings_not_canceled

**Booking Details:**
- booking_changes, deposit_type, days_in_waiting_list
- customer_type, adr (average daily rate)
- required_car_parking_spaces, total_of_special_requests

**Optional:**
- agent, company, country

## 🐛 Troubleshooting

### Common Issues:

1. **Model files not found**
   - Solution: Run `python train_and_save_model.py` first

2. **Import errors**
   - Solution: Ensure all dependencies are installed: `pip install -r requirements.txt`

3. **Dataset not found**
   - Solution: Download the hotel_bookings.csv dataset and place it in the project root

4. **Port already in use**
   - Solution: Run Streamlit on a different port: `streamlit run app.py --server.port 8502`

## 📚 Dataset

The model is trained on the **Hotel Booking Demand** dataset, which contains:
- 119,390 hotel bookings
- 32 features
- Data from two hotels (City Hotel and Resort Hotel)
- Bookings from 2015-2017

**Dataset Source**: [Hotel Booking Demand Dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Dataset provided by the Hotel Booking Demand dataset on Kaggle
- Scikit-learn for machine learning tools
- Streamlit for the web framework

## 📞 Support

For questions or issues, please open an issue on GitHub or contact [your-email@example.com]

---

**Made with ❤️ using Python, Scikit-learn, and Streamlit**
