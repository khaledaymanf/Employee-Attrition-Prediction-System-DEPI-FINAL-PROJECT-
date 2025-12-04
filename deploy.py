# app.py
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

MODEL_PATH = "employee_attrition_model.pkl"

#EXACT 51 FEATURES EXPECTED BY THE MODEL
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

    # One-hot Encoding
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

    # Engineered Features
    'TenureRatio': 0.5,
    'YearsSincePromotionRatio': 0.15,
    'IncomePerYear': 6000,
    'IncomeToAge': 200,
    'WorkLifeScore': 3.0
}

# Ensure the order matches training data
ORDERED_KEYS = list(DEFAULT_FEATURES.keys())

app = Flask(__name__)
CORS(app)

# Load model
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except:
    model = None
    print("ERROR: Could not load model.")

@app.route("/predict", methods=["POST"])
def predict_attrition():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json(silent=True) or {}

    inputs = DEFAULT_FEATURES.copy()

    # Overwrite only provided fields
    for k, v in data.items():
        if k in inputs:
            inputs[k] = v

    # Convert to numpy vector in the correct order
    vector = np.array([inputs[k] for k in ORDERED_KEYS]).reshape(1, -1)

    # Predict
    proba = model.predict_proba(vector)[0][1]
    prediction = "Yes" if proba >= 0.5 else "No"

    return jsonify({
        "prediction": prediction,
        "probability": float(proba)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
