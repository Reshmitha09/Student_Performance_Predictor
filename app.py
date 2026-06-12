import streamlit as st
import pandas as pd
import pickle
import os
from datetime import datetime
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)
model = pickle.load(open("models/model.pkl", "rb"))
comparison_df = pd.read_csv("models/model_comparison.csv")
feature_df = pd.read_csv("models/feature_importance.csv")
df = pd.read_csv("data/student-mat.csv", sep=";")
history_file = "prediction_history.csv"
if not os.path.exists(history_file):
    pd.DataFrame(
        columns=[
            "timestamp",
            "studytime",
            "absences",
            "g1",
            "g2",
            "prediction"
        ]
    ).to_csv(history_file, index=False)
st.title("🎓 Student Performance Predictor Dashboard")
tab1, tab2, tab3 = st.tabs(
    ["Prediction", "Dataset Insights", "Model Performance"]
)
with tab1:
    st.header("Predict Student Final Grade")
    studytime = st.slider(
        "Study Time",
        1,
        4,
        2
    )
    absences = st.number_input(
        "Absences",
        min_value=0,
        max_value=100,
        value=5
    )
    g1 = st.number_input(
        "G1 Grade",
        min_value=0,
        max_value=20,
        value=10
    )
    g2 = st.number_input(
        "G2 Grade",
        min_value=0,
        max_value=20,
        value=10
    )
    if st.button("Predict Final Grade"):
        prediction = model.predict(
            [[studytime, absences, g1, g2]]
        )[0]
        if prediction <= 7:
            category = "Poor"
        elif prediction <= 11:
            category = "Average"
        elif prediction <= 15:
            category = "Good"
        else:
            category = "Excellent"
        st.success(
            f"Predicted Grade: {prediction:.2f}"
        )
        st.info(
            f"Category: {category}"
        )
        st.subheader("Suggestions")
        recommendations = []
        if studytime < 3:
            recommendations.append(
                "Increase study time"
            )
        if absences > 10:
            recommendations.append(
                "Reduce absences"
            )
        if g1 < 10:
            recommendations.append(
                "Improve G1 performance"
            )
        if g2 < 10:
            recommendations.append(
                "Improve G2 performance"
            )
        if recommendations:
            for rec in recommendations:
                st.write("✓", rec)
        else:
            st.write("✓ Keep up the good work!")
        new_row = pd.DataFrame([
            {
                "timestamp": datetime.now(),
                "studytime": studytime,
                "absences": absences,
                "g1": g1,
                "g2": g2,
                "prediction": round(prediction, 2)
            }
        ])
        history = pd.read_csv(history_file)
        history = pd.concat(
            [history, new_row],
            ignore_index=True
        )
        history.to_csv(
            history_file,
            index=False
        )
    st.subheader("Recent Predictions")
    history = pd.read_csv(history_file)
    st.dataframe(
        history.tail(10)
    )
with tab2:
    st.header("Dataset Insights")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Dataset Size",
        len(df)
    )
    rf_mae = comparison_df[
        comparison_df["Model"] == "Random Forest"
    ]["MAE"].values[0]
    col2.metric(
        "Random Forest MAE",
        round(rf_mae, 2)
    )
    col3.metric(
        "Features Used",
        4
    )
    st.subheader("Grade Distribution")
    st.bar_chart(
        df["G3"].value_counts().sort_index()
    )
    st.subheader("Study Time Distribution")
    st.bar_chart(
        df["studytime"].value_counts()
    )
    st.subheader("Absence Distribution")
    st.bar_chart(
        df["absences"]
    )
with tab3:
    st.header("Model Performance")
    st.subheader("Model Comparison")
    st.dataframe(
        comparison_df
    )
    st.bar_chart(
        comparison_df.set_index("Model")
    )
    st.subheader("Feature Importance")
    st.dataframe(
        feature_df
    )
    st.bar_chart(
        feature_df.set_index("Feature")
    )