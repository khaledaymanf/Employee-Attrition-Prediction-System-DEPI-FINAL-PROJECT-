💼 Project Overview
This project delivers a full-stack solution for predicting employee attrition. It encompasses data analysis, machine learning model development (using the provided dataset), and a deployment system consisting of a Flask API backend and an interactive Streamlit frontend.

The goal is to provide HR departments with a tool to proactively identify employees at high risk of leaving the company, enabling timely intervention and retention strategies.

🚀 Features
Data Analysis (EDA): Comprehensive analysis of the provided HR dataset to uncover key factors and correlations influencing attrition.

Machine Learning Model: A robust classification model (trained in employee_attrition.ipynb) for predicting the binary outcome of attrition (Yes/No).

RESTful API: A lightweight Flask API that exposes the model's prediction capabilities via a standard /predict endpoint.

Interactive Frontend: A user-friendly Streamlit web application that allows HR personnel to input key employee metrics and instantly receive an attrition risk assessment.

Simplified Input: The frontend focuses on the 10 most impactful features, while the backend handles the imputation and encoding of the remaining necessary features for the model.

🛠️ Technologies & Libraries
Core Language: Python 3.x

Data Science: Pandas, NumPy, Scikit-learn

Visualization: Matplotlib, Seaborn, Plotly (used in the Notebook)

Backend API: Flask, Flask-CORS

Frontend UI: Streamlit, Requests
