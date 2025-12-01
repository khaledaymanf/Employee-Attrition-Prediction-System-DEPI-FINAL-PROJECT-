# streamlit_app.py - Streamlit Frontend showing only 10 key features

import streamlit as st
import requests
import json
import time

# --- Configuration ---
API_URL = "http://localhost:5000/predict" 

st.set_page_config(page_title="Employee Attrition Predictor (Simplified)", layout="wide")
st.title("💼 Simplified Attrition Prediction System")
st.markdown("Please input the **10 most important** employee features. Other features will be automatically imputed.")

# Use a form structure for better organization
with st.form(key='attrition_form'):
    st.subheader("Key Employee Metrics (10 Inputs)")
    
    # --- Input Widgets (10 Selected Features) ---
    col1, col2, col3 = st.columns(3)
    
    # Column 1 (Numerical)
    with col1:
        age = st.slider("Age", 18, 60, 30)
        daily_rate = st.number_input("Daily Rate", min_value=100, max_value=2000, value=800)
        distance = st.number_input("Distance From Home (km)", min_value=1, max_value=30, value=9)
        
    # Column 2 (Ordinal / Numerical)
    with col2:
        hourly_rate = st.number_input("Hourly Rate", min_value=30, max_value=100, value=66)
        job_involvement = st.selectbox("Job Involvement (1=Low, 4=High)", options=[1, 2, 3, 4], index=2)
        job_satisfaction = st.selectbox("Job Satisfaction (1=Low, 4=High)", options=[1, 2, 3, 4], index=2)
        
    # Column 3 (Categorical / Numerical)
    with col3:
        years_at_company = st.number_input("Years At Company", min_value=0, max_value=40, value=7)
        overtime_options = st.radio("Over Time?", ["No", "Yes"], horizontal=True)
        job_role = st.selectbox("Job Role", options=['Sales Executive', 'Research Scientist', 'Other'], index=0) 
        marital_status = st.radio("Marital Status", ['Single', 'Married', 'Divorced'], index=1)
        
    submitted = st.form_submit_button("Predict Attrition Likelihood", type="primary")

if submitted:
    # 1. Prepare Payload (ONLY the user-provided values, converted to API's OHE keys)
    # The key names here MUST match the keys in the DEFAULT_FEATURES dictionary in app.py
    payload = {
        'Age': int(age),
        'DailyRate': int(daily_rate),
        'DistanceFromHome': float(distance),
        'HourlyRate': float(hourly_rate),
        'JobInvolvement': int(job_involvement),
        'JobSatisfaction': int(job_satisfaction),
        'YearsAtCompany': int(years_at_company),
        
        # OHE Keys - Only the 'Yes' category is sent if selected
        'OverTime_Yes': 1 if overtime_options == "Yes" else 0,
        
        # OHE Key for JobRole: Only Sales Executive is handled as a key input
        'JobRole_Sales Executive': 1 if job_role == 'Sales Executive' else 0,
        
        # OHE Key for Marital Status: Only Married is handled as a key input
        'MaritalStatus_Married': 1 if marital_status == 'Married' else 0,
    }

    # 2. Send request to API
    with st.spinner('Contacting API and generating prediction...'):
        time.sleep(1) 
        
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status() 
            result = response.json()
            
            # 3. Display Result
            prediction = result.get('prediction', 'N/A')
            probability = result.get('probability', 0) * 100
            
            st.subheader("📊 Prediction Result")
            st.metric("Attrition Prediction", prediction)
            st.metric("Confidence (%)", f"{probability:.2f}%")

            if prediction == "Yes":
                st.error("⚠️ High Risk: Predicted to leave.")
            elif prediction == "No":
                st.success("✅ Low Risk: Predicted to stay.")

        except requests.exceptions.ConnectionError:
            st.error(f"❌ Connection Error: Could not connect to the API at {API_URL}. Ensure 'app.py' is running.")
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API Error: The server returned an error. Check the Flask terminal.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")