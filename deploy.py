# deploy.py
import requests


URL = "https://employee-attritionprediction.streamlit.app/"


data = {
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

try:
    response = requests.post(URL, json=data)

    print("Status code:", response.status_code)
    print("Response text:", response.text)

    result = response.json()
    print("\nPrediction Result:", result)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)

except ValueError:
    print("Error: Response is not valid JSON")
