from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load model & preprocessors
model_diabetes = joblib.load("model_diabetes.pkl")
model_bp = joblib.load("model_bp.pkl")
imputer = joblib.load("imputer.pkl")
label_encoders = joblib.load("label_encoders.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# Health tips
diabetes_tips = [
    "Control sugar intake. Eat low-glycemic foods.",
    "Exercise regularly and maintain a healthy weight."
]

bp_tips = [
    "Reduce salt and manage stress.",
    "Monitor blood pressure and avoid smoking."
]

@app.route('/')
def home():
    return "✅ Health Risk Predictor API is live."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        df = pd.DataFrame([data])

        # Label encoding
        for col, le in label_encoders.items():
            if col in df.columns:
                df[col] = df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

        # Ensure required columns
        missing = set(feature_columns) - set(df.columns)
        if missing:
            return jsonify({"error": f"Missing features: {list(missing)}"}), 400

        df = df[feature_columns]
        df = pd.DataFrame(imputer.transform(df), columns=feature_columns)

        diabetes_pred = model_diabetes.predict(df)[0]
        bp_pred = model_bp.predict(df)[0]

        diabetes_status = ["Normal", "Pre-Diabetic", "Diabetic"][int(diabetes_pred)]
        bp_status = ["Normal", "Pre-Hypertensive", "Hypertensive"][int(bp_pred)]

        tips = []
        if diabetes_pred > 0:
            tips += diabetes_tips
        if bp_pred > 0:
            tips += bp_tips

        return jsonify({
            "diabetes_status": diabetes_status,
            "bp_status": bp_status,
            "health_tips": tips
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host="0.0.0.0", port=port)
