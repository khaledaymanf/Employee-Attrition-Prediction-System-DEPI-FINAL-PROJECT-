import streamlit as st
import pickle
import numpy as np
from joblib import load


st.set_page_config(page_title="Employee Attrition Predictor", layout="wide")
st.title("💼 Employee Attrition Prediction")
st.markdown("Provide the following key features:")

model = load("employee_attrition_model.pkl")

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

    # نسخ القيم الافتراضية للخصائص اللي مش موجودة
    default_features = {
        'Education': 3,
        'EnvironmentSatisfaction': 3,
        'MonthlyIncome': 6500,
        'MonthlyRate': 14000,
        'NumCompaniesWorked': 2,
        'PercentSalaryHike': 12,
        'PerformanceRating': 3,
        'RelationshipSatisfaction': 3,
        'StockOptionLevel': 1,
        'TrainingTimesLastYear': 3,
        'WorkLifeBalance': 3,
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
        'JobRole_Sales Representative': 0,
        'MaritalStatus_Single': 0,
        'OverTime_Yes': payload["OverTime_Yes"],
        'TenureRatio': 0.5,
        'YearsSincePromotionRatio': 0.15,
        'IncomePerYear': 6000,
        'IncomeToAge': 200,
        'WorkLifeScore': 3.0
    }

    # دمج بيانات المستخدم مع الافتراضية
    for k,v in payload.items():
        default_features[k] = v

    vector = np.array([default_features[k] for k in default_features]).reshape(1, -1)
    proba = model.predict_proba(vector)[0][1]
    prediction = "Yes" if proba >= 0.5 else "No"

    st.subheader("📊 Result")
    st.metric("Prediction", prediction)
    st.metric("Confidence", f"{proba*100:.2f}%")

    if prediction == "Yes":
        st.error("⚠️ High Risk: Employee likely to leave.")
    else:
        st.success("✅ Low Risk: Employee likely to stay.")

