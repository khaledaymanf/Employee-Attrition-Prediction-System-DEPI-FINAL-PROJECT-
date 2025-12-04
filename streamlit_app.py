# streamlit_app.py
import streamlit as st
import requests
import time

API_URL = "https://employee-attritionprediction.streamlit.app/"

st.set_page_config(page_title="Employee Attrition Predictor", layout="wide")
st.title("💼 Employee Attrition Prediction")
st.markdown("Provide the following key features:")

with st.form("form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 18, 60, 30)
        daily_rate = st.number_input("Daily Rate", 100, 2000, 800)
        distance = st.number_input("Distance From Home", 1, 30, 9)

    with col2:
        hourly_rate = st.number_input("Hourly Rate", 30, 100, 66)
        job_involvement = st.selectbox("Job Involvement (1–4)", [1,2,3,4], 2)
        job_satisfaction = st.selectbox("Job Satisfaction (1–4)", [1,2,3,4], 2)

    with col3:
        years_at_company = st.number_input("Years At Company", 0, 40, 7)
        overtime = st.radio("OverTime", ["No", "Yes"])
        job_role = st.selectbox("Job Role", ["Sales Executive", "Other"])
        marital_status = st.radio("Marital Status", ["Single", "Married"])

    submitted = st.form_submit_button("Predict", type="primary")

if submitted:
    payload = {
        "Age": age,
        "DailyRate": daily_rate,
        "DistanceFromHome": distance,
        "HourlyRate": hourly_rate,
        "JobInvolvement": job_involvement,
        "JobSatisfaction": job_satisfaction,
        "YearsAtCompany": years_at_company,

        "OverTime_Yes": 1 if overtime == "Yes" else 0,
        "JobRole_Sales Executive": 1 if job_role == "Sales Executive" else 0,
        "MaritalStatus_Married": 1 if marital_status == "Married" else 0,
    }

    with st.spinner("Contacting server..."):
        time.sleep(0.7)
        try:
            r = requests.post(API_URL, json=payload)
            res = r.json()

            pred = res["prediction"]
            prob = res["probability"] * 100

            st.subheader("📊 Result")
            st.metric("Prediction", pred)
            st.metric("Confidence", f"{prob:.2f}%")

            if pred == "Yes":
                st.error("⚠️ High Risk: Employee likely to leave.")
            else:
                st.success("✅ Low Risk: Employee likely to stay.")

        except Exception as e:
            st.error(f"Error: {e}")


