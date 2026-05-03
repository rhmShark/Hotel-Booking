"""
Hotel Booking Cancellation Prediction - Streamlit App
A web-based interface for predicting hotel booking cancellations using SVM
"""

import streamlit as st
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Hotel Booking Cancellation Predictor",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_model():
    """Load the trained model pipeline using joblib for efficient loading"""
    try:
        pipeline = joblib.load('model_artifacts/hotel_booking_pipeline.pkl')
        feature_info = joblib.load('model_artifacts/feature_info.pkl')
        return pipeline, feature_info
    except FileNotFoundError:
        st.error("⚠️ Model files not found! Please run 'train_and_save_model.py' first.")
        st.stop()


def create_input_features():
    """Create input form for user to enter booking details"""
    
    st.sidebar.header("📋 Booking Information")
    
    # Hotel Type
    hotel = st.sidebar.selectbox(
        "Hotel Type",
        options=["City Hotel", "Resort Hotel"],
        help="Type of hotel"
    )
    
    # Lead Time
    lead_time = st.sidebar.number_input(
        "Lead Time (days)",
        min_value=0,
        max_value=737,
        value=50,
        help="Number of days between booking and arrival"
    )
    
    # Arrival Date
    st.sidebar.subheader("Arrival Date")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        arrival_year = st.selectbox("Year", options=[2015, 2016, 2017])
    
    with col2:
        arrival_month = st.selectbox(
            "Month",
            options=["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
        )
    
    arrival_week = st.sidebar.slider("Week Number", 1, 53, 27)
    arrival_day = st.sidebar.slider("Day of Month", 1, 31, 15)
    
    # Stay Duration
    st.sidebar.subheader("Stay Duration")
    weekend_nights = st.sidebar.number_input("Weekend Nights", 0, 10, 1)
    week_nights = st.sidebar.number_input("Week Nights", 0, 20, 2)
    
    # Guests
    st.sidebar.subheader("Guest Information")
    adults = st.sidebar.number_input("Adults", 1, 10, 2)
    children = st.sidebar.number_input("Children", 0, 10, 0)
    babies = st.sidebar.number_input("Babies", 0, 10, 0)
    
    # Meal Plan
    meal = st.sidebar.selectbox(
        "Meal Plan",
        options=["BB", "HB", "FB", "SC", "Undefined"],
        help="BB=Bed & Breakfast, HB=Half Board, FB=Full Board, SC=Self Catering"
    )
    
    # Country
    country = st.sidebar.text_input("Country Code", "PRT", help="3-letter country code")
    
    # Market Segment
    market_segment = st.sidebar.selectbox(
        "Market Segment",
        options=["Direct", "Corporate", "Online TA", "Offline TA/TO", "Complementary", "Groups", "Aviation"]
    )
    
    # Distribution Channel
    distribution_channel = st.sidebar.selectbox(
        "Distribution Channel",
        options=["Direct", "Corporate", "TA/TO", "GDS"]
    )
    
    # Previous History
    st.sidebar.subheader("Booking History")
    is_repeated_guest = st.sidebar.checkbox("Repeated Guest")
    previous_cancellations = st.sidebar.number_input("Previous Cancellations", 0, 20, 0)
    previous_bookings = st.sidebar.number_input("Previous Bookings (Not Canceled)", 0, 50, 0)
    
    # Room Information
    st.sidebar.subheader("Room Details")
    reserved_room_type = st.sidebar.selectbox(
        "Reserved Room Type",
        options=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    )
    
    assigned_room_type = st.sidebar.selectbox(
        "Assigned Room Type",
        options=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
        index=0
    )
    
    booking_changes = st.sidebar.number_input("Booking Changes", 0, 20, 0)
    
    # Deposit and Payment
    deposit_type = st.sidebar.selectbox(
        "Deposit Type",
        options=["No Deposit", "Refundable", "Non Refund"]
    )
    
    # Agent and Company (optional)
    agent = st.sidebar.number_input("Agent ID (0 if none)", 0, 500, 0)
    company = st.sidebar.number_input("Company ID (0 if none)", 0, 500, 0)
    
    # Additional Information
    st.sidebar.subheader("Additional Details")
    days_in_waiting_list = st.sidebar.number_input("Days in Waiting List", 0, 400, 0)
    
    customer_type = st.sidebar.selectbox(
        "Customer Type",
        options=["Transient", "Contract", "Transient-Party", "Group"]
    )
    
    adr = st.sidebar.number_input(
        "Average Daily Rate (ADR)",
        min_value=0.0,
        max_value=1000.0,
        value=100.0,
        help="Average daily rate in the currency of the hotel"
    )
    
    parking_spaces = st.sidebar.number_input("Required Parking Spaces", 0, 10, 0)
    special_requests = st.sidebar.number_input("Total Special Requests", 0, 10, 0)
    
    # Create feature dictionary
    features = {
        'hotel': hotel,
        'lead_time': lead_time,
        'arrival_date_year': arrival_year,
        'arrival_date_month': arrival_month,
        'arrival_date_week_number': arrival_week,
        'arrival_date_day_of_month': arrival_day,
        'stays_in_weekend_nights': weekend_nights,
        'stays_in_week_nights': week_nights,
        'adults': adults,
        'children': float(children),
        'babies': babies,
        'meal': meal,
        'country': country,
        'market_segment': market_segment,
        'distribution_channel': distribution_channel,
        'is_repeated_guest': int(is_repeated_guest),
        'previous_cancellations': previous_cancellations,
        'previous_bookings_not_canceled': previous_bookings,
        'reserved_room_type': reserved_room_type,
        'assigned_room_type': assigned_room_type,
        'booking_changes': booking_changes,
        'deposit_type': deposit_type,
        'agent': float(agent) if agent > 0 else np.nan,
        'company': float(company) if company > 0 else np.nan,
        'days_in_waiting_list': days_in_waiting_list,
        'customer_type': customer_type,
        'adr': adr,
        'required_car_parking_spaces': parking_spaces,
        'total_of_special_requests': special_requests
    }
    
    return features


def make_prediction(pipeline, features):
    """Make prediction using the trained pipeline"""
    # Convert features to DataFrame
    df = pd.DataFrame([features])
    
    # Make prediction
    prediction = pipeline.predict(df)[0]
    prediction_proba = pipeline.predict_proba(df)[0]
    
    return prediction, prediction_proba


def display_prediction_results(prediction, prediction_proba):
    """Display prediction results with styling"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if prediction == 1:
            st.error("🚨 **HIGH RISK OF CANCELLATION**")
            st.markdown(f"**Cancellation Probability: {prediction_proba[1]:.2%}**")
        else:
            st.success("✅ **LOW RISK OF CANCELLATION**")
            st.markdown(f"**Cancellation Probability: {prediction_proba[1]:.2%}**")
    
    # Probability breakdown
    st.subheader("📊 Prediction Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Will NOT Cancel",
            value=f"{prediction_proba[0]:.2%}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Will Cancel",
            value=f"{prediction_proba[1]:.2%}",
            delta=None
        )
    
    # Risk level indicator
    risk_level = prediction_proba[1]
    if risk_level < 0.3:
        risk_text = "🟢 Low Risk"
        risk_color = "green"
    elif risk_level < 0.7:
        risk_text = "🟡 Medium Risk"
        risk_color = "orange"
    else:
        risk_text = "🔴 High Risk"
        risk_color = "red"
    
    st.markdown(f"**Risk Level: <span style='color:{risk_color}'>{risk_text}</span>**", 
                unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Title and description
    st.title("🏨 Hotel Booking Cancellation Predictor")
    st.markdown("""
    This application uses a **Support Vector Machine (SVM)** model to predict the likelihood 
    of hotel booking cancellations based on various booking characteristics.
    
    **How to use:**
    1. Fill in the booking details in the sidebar
    2. Click 'Predict Cancellation Risk' to get the prediction
    3. Review the results and risk assessment
    """)
    
    # Load model
    try:
        pipeline, feature_info = load_model()
        st.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return
    
    # Create input form
    features = create_input_features()
    
    # Prediction button
    if st.sidebar.button("🔮 Predict Cancellation Risk", type="primary"):
        try:
            with st.spinner("Making prediction..."):
                prediction, prediction_proba = make_prediction(pipeline, features)
            
            display_prediction_results(prediction, prediction_proba)
            
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")
    
    # Model information
    with st.expander("ℹ️ About the Model"):
        st.markdown("""
        **Model Details:**
        - **Algorithm:** Support Vector Machine (SVM) with Linear Kernel
        - **Features:** 29 booking characteristics
        - **Preprocessing:** StandardScaler, OneHotEncoder, PCA
        - **Performance:** ~71.6% accuracy on test data
        
        **Key Features Considered:**
        - Lead time (days between booking and arrival)
        - Hotel type and room details
        - Guest information and history
        - Deposit type and payment details
        - Market segment and distribution channel
        - Special requests and booking changes
        """)
    
    # Sample data section
    with st.expander("📋 Sample Booking Data"):
        sample_data = {
            'Hotel Type': 'City Hotel',
            'Lead Time': 85,
            'Adults': 2,
            'Children': 0,
            'Weekend Nights': 1,
            'Week Nights': 2,
            'Meal Plan': 'BB',
            'Market Segment': 'Online TA',
            'Deposit Type': 'No Deposit',
            'ADR': 120.0
        }
        
        st.json(sample_data)
        st.caption("This is an example of typical booking data that can be used for prediction.")


if __name__ == "__main__":
    main()

# Made with Bob
