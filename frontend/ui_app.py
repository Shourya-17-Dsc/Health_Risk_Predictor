import streamlit as st
import requests

# Page Config
st.set_page_config(page_title="Global Health Risk Predictor", page_icon="🩺", layout="centered")

# API URL - replace with your actual backend URL
API_URL = "https://health-risk-predictor-etp3.onrender.com/predict"

st.title("🩺 Global Health Risk Predictor")
st.markdown("Predict Diabetes and Hypertension risk using recent health metrics. Works across all users worldwide!")

with st.form("risk_form"):
    st.subheader("👤 Employee & Demographic Info")

    col1, col2 = st.columns(2)
    with col1:
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        year = st.selectbox("Checkup Year", [2021, 2022, 2023, 2024, 2025])
        plant = st.selectbox("Plant", ["NPC", "RAS", "BCP", "GRGM1", "SMP"])
        department = st.selectbox("Department", ["IT", "HR", "Finance", "Operations", "Admin", "Others"])
    with col2:
        age = st.slider("Age", 18, 100, 30)
        sex = st.selectbox("Sex", ["Male", "Female"])
        bmi = st.number_input("BMI", 10.0, 50.0, 23.5)
        bp = st.number_input("Blood Pressure (Systolic)", min_value=80.0, max_value=200.0, value=120.0)
        hdl = st.number_input("HDlCholestrol", min_value=10.0, max_value=100.0, value=50.0)

    st.subheader("🧪 Lab Test Values")
    col3, col4, col5 = st.columns(3)
    with col3:
        sugar_r = st.number_input("Random Blood Sugar", 50.0, 400.0, 110.0)
    with col4:
        chol = st.number_input("Cholesterol", 100.0, 400.0, 180.0)
    with col5:
        tg = st.number_input("Triglycerides", 50.0, 400.0, 150.0)

    col6, col7 = st.columns(2)
    with col6:
        ldl = st.number_input("LDL", 10.0, 200.0, 100.0)
    with col7:
        vldl = st.number_input("VLDL", 5.0, 100.0, 30.0)

    submit = st.form_submit_button("🔍 Predict Now")

# On Submit
if submit:
    st.info("⏳ Sending data to backend...")

    payload = {
        "blood_group": blood_group,
        "year": year,
        "plant": plant,
        "department": department,
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "bp": bp,
        "sugar_r": sugar_r,
        "chol": chol,
        "tg": tg,
        "LDL": ldl,
        "VLDL": vldl,
        "HDlCholestrol": hdl
    }

    try:
        res = requests.post(API_URL, json=payload)

        if res.status_code == 200:
            result = res.json()
            st.success(f"🩸 Diabetes Status: **{result['diabetes_status']}**")
            st.success(f"💓 Blood Pressure Status: **{result['bp_status']}**")

            if result.get("health_tips"):
                st.subheader("💡 Health Tips")
                for tip in result["health_tips"]:
                    st.markdown(f"- ✅ {tip}")
            else:
                st.info("✅ No tips required — you're healthy!")

        else:
            st.error("🚨 Server responded with an error.")
            st.code(res.text)

    except Exception as e:
        st.error("❌ Failed to connect to the backend.")
        st.code(str(e))

# Footer
st.markdown("---")
st.caption("🌐 Created by Shourya | Streamlit + Flask | 2025")
