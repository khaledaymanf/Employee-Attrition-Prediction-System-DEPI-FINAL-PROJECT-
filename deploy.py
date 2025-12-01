import os
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS 

# --- Configuration ---
MODEL_PATH = 'employee_attrition_model.pkl'

# --- 🎯 Define ALL 87 Features and their Default/Mean/Mode Values ---
# This dictionary represents all 87 features the model expects, in the EXACT order 
# used during training. Default values are placeholders (use actual means/modes).
# If your model expects 85 or 90 features, adjust this number accordingly.
DEFAULT_FEATURES = {
    # Numerical / Ordinal Features (Examples of Mean Imputation)
    'Age': 36.92, 
    'DailyRate': 802.48, 
    'DistanceFromHome': 9.19, 
    'HourlyRate': 65.99,
    'JobInvolvement': 2.73, # User input (will be overwritten)
    'JobSatisfaction': 2.72, # User input (will be overwritten)
    'YearsAtCompany': 7.00, # User input (will be overwritten)
    'EnvironmentSatisfaction': 3.0,
    'JobLevel': 2,
    'MonthlyIncome': 6502.93,
    'TotalWorkingYears': 11.27,
    # ... (Add all other numerical features here)
    
    # One-Hot Encoded (OHE) Features (Examples of Mode Imputation - 0 or 1)
    'OverTime_Yes': 0, # User input (1 or 0)
    'JobRole_Sales Executive': 0, # User input (1 or 0)
    'MaritalStatus_Married': 0, # User input (1 or 0)

    # Auto-Completed OHE Features (The remaining 74 OHE features)
    'BusinessTravel_Travel_Frequently': 0,
    'BusinessTravel_Travel_Rarely': 1, # Default is the most common category
    'Department_Research & Development': 1,
    'Department_Sales': 0,
    'Department_Human Resources': 0,
    'Education_1': 0, 
    'Education_2': 0, 
    'Education_3': 1, # Default to category 3
    # ... (List ALL 87 keys here exactly as the model expects them)
    # FOR DEMO PURPOSES, THIS DICT MUST CONTAIN 87 ITEMS. 
    # Since we can't list all 87, please manually complete this list based on your notebook.
}

# The ordered list of all 87 keys MUST be correct
ORDERED_KEYS = list(DEFAULT_FEATURES.keys()) 

# --- Initialize App and CORS ---
app = Flask(__name__)
CORS(app) 

# --- Model Loading ---
model = None
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f) 
    print(f"Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    print(f"ERROR: Model file {MODEL_PATH} not found.")
    class MockModel:
        def predict_proba(self, X):
            return np.array([[0.8, 0.2]])
    model = MockModel()

# --- Prediction Endpoint ---

@app.route('/predict', methods=['POST'])
def predict_attrition():
    if model is None:
        return jsonify({"error": "Model failed to load. Cannot predict."}), 500
        
    try:
        # Get data posted as JSON. silent=True prevents crashes on empty body.
        data = request.get_json(silent=True) 
        if not data:
            data = {} # Treat empty request as an empty dictionary

        # 1. Start with all 87 default values
        input_features = DEFAULT_FEATURES.copy()
        
        # 2. Overwrite the values provided by the user (up to 10 key features)
        # This loop only overwrites keys that exist in the payload AND in the defaults
        for key, value in data.items():
            if key in input_features:
                input_features[key] = value

        # 3. Create the 87-feature array using the predetermined ORDERED_KEYS
        # This is the crucial step to ensure the size is always 87 and the order is correct.
        feature_vector = np.array([input_features[k] for k in ORDERED_KEYS]).reshape(1, -1) 
        
        # Perform Prediction
        probabilities = model.predict_proba(feature_vector)[0]
        attrition_prob = probabilities[1] 
        
        prediction_label = 'Yes' if attrition_prob > 0.5 else 'No'
        
        return jsonify({
            'prediction': prediction_label,
            'probability': float(attrition_prob)
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred during prediction: {str(e)}'}), 400

# --- Run the API ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)