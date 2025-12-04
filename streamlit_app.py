import streamlit as st
import pickle
import numpy as np
import time

MODEL_PATH = "employee_attrition_model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

DEFAULT_FEATURES = {
    'Age': 37,
    'DailyRate': 800,
    'DistanceFromHome': 9,
    'Education': 3,
    'EnvironmentSatisfaction': 3,
    'HourlyRate': 66,
    'JobInvolvement': 3,
    'JobLevel': 2,
    'JobSatisfaction': 3,
    'MonthlyIncome': 6500,
    'MonthlyRate': 14000,
    'NumCompaniesWorked': 2,
    'PercentSalaryHike': 12,
    'PerformanceRating': 3,
    'RelationshipSatisfaction': 3,
    'StockOptionLevel': 1,
    'TotalWorkingYears': 11,
    'TrainingTimesLastYear': 3,
    'WorkLifeBalance': 3,
    'YearsAtCompany': 7,
    'YearsInCurrentRole': 4,
    'YearsSinceLastPromotion': 2,
    'YearsWithCurrManager': 4,
    'IncomePerYearExperience': 500,
    'BusinessTravel_Travel_Frequently': 0,
    'BusinessTravel_Travel_Rarely': 1,
    'Department_Research & Development': 1,
    'Department_Sales': 0,
    'EducationField_Life Sciences': 1,
    'EducationField_Marketing': 0,
    'EducationField_Medical': 0,
    'EducationField_Other': 0,
    'EducationField_Technical Degree': 0,
    'Gender_Male': 1,
    'JobRole_Human Resources': 0,
    'JobRole_Laboratory Technician': 0,
    'JobRole_Manager': 0,
    'JobRole_Manufacturing Director': 0,
    'JobRole_Research Director': 0,
    'JobRole_Research Scientist': 0,
    'JobRole_Sales Executive': 0,
    'JobRole_Sales Representative': 0,
    'MaritalStatus_Married': 0,
    'MaritalStatus_Single': 0,
    'OverTime_Yes': 0,
    'TenureRatio': 0.5,
    'YearsSincePromotionRatio': 0.15,
    'IncomePerYear': 6000,
    'IncomeToAge': 200,
    'WorkLifeScore': 3.0
}

ORDERED_KEYS = list(DEFAULT_FEATURES.keys())

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
    payload = DEFAULT_FEATURES.copy()

    payload["Age"] = age
    payload["DailyRate"] = daily_rate
    payload["DistanceFromHome"] = distance
    payload["HourlyRate"] = hourly_rate
    payload["JobInvolvement"] = job_involvement
    payload["JobSatisfaction"] = job_satisfaction
    payload["YearsAtCompany"] = years_at_company
    payload["OverTime_Yes"] = 1 if overtime == "Yes" else 0
    payload["JobRole_Sales Executive"] = 1 if job_role == "Sales Executive" else 0
    payload["MaritalStatus_Married"] = 1 if marital_status == "Married" else 0
    payload["MaritalStatus_Single"] = 1 if marital_status == "Single" else 0

    vector = np.array([payload[k] for k in ORDERED_KEYS]).reshape(1, -1)

    with st.spinner("Predicting..."):
        time.sleep(0.5)
        proba = model.predict_proba(vector)[0][1]
        pred = "Yes" if proba >= 0.5 else "No"

    st.subheader("📊 Result")
    st.metric("Prediction", pred)
    st.metric("Confidence", f"{proba*100:.2f}%")

    if pred == "Yes":
        st.error("⚠️ High Risk: Employee likely to leave.")
    else:
        st.success("✅ Low Risk: Employee likely to stay.")
