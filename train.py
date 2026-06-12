import os
import pickle
import pandas as pd
from pandas.api.types import is_string_dtype
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
df = pd.read_csv("data/student-mat.csv", sep=";")
for col in df.columns:
    if is_string_dtype(df[col]):
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
X = df[[
    "studytime",
    "absences",
    "G1",
    "G2"
]]
y = df["G3"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
models = {
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ),
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    )
}
results = {}
best_model = None
best_mae = float("inf")
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mae = mean_absolute_error(
        y_test,
        preds
    )
    results[name] = mae
    print(f"{name} MAE: {mae:.4f}")
    if mae < best_mae:
        best_mae = mae
        best_model = model
os.makedirs("models", exist_ok=True)
comparison_df = pd.DataFrame(
    results.items(),
    columns=["Model", "MAE"]
)
comparison_df.to_csv(
    "models/model_comparison.csv",
    index=False
)
pickle.dump(
    best_model,
    open("models/model.pkl", "wb")
)
print("\nBest Model Saved")
rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
rf_model.fit(X_train, y_train)
feature_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf_model.feature_importances_
})
feature_df.to_csv(
    "models/feature_importance.csv",
    index=False
)
print("Feature Importance Saved")
print("Training Completed Successfully")