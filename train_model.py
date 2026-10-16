
from pathlib import Path
import sys

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA_FILE = Path("patient_waiting_data.csv")
TARGET = "waiting_time"

NUMERIC_FEATURES = [
    "arrival_hour",
    "queue_length",
    "staff_count",
    "bed_count",
    "daily_capacity",
]
CATEGORICAL_FEATURES = ["department"]


def main():
    if not DATA_FILE.exists():
        sys.exit(
            f"Training data not found: {DATA_FILE}\n"
            "Provide a patient-level CSV with actual waiting-time labels. "
            "The aggregated demoData.json is not suitable for this script."
        )

    df = pd.read_csv(DATA_FILE)

    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    required = features + [TARGET]
    missing = [col for col in required if col not in df.columns]

    if missing:
        sys.exit(f"Missing CSV columns: {', '.join(missing)}")

    df = df[required].copy()
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df.dropna(subset=[TARGET])

    if len(df) < 10:
        sys.exit("At least 10 labelled rows are required for this demo.")

    if (df[TARGET] < 0).any():
        sys.exit("Waiting times must be non-negative.")

    X = df[features]
    y = df[TARGET]

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessing = ColumnTransformer([
        ("numeric", numeric_pipeline, NUMERIC_FEATURES),
        ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
    ])

    model = Pipeline([
        ("preprocessing", preprocessing),
        ("regressor", RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            min_samples_leaf=2,
        )),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")
    print(f"Mean absolute error: {mean_absolute_error(y_test, predictions):.2f} minutes")
    print(f"R² score: {r2_score(y_test, predictions):.3f}")

    joblib.dump(model, "waiting_time_model.joblib")
    print("Saved trained model: waiting_time_model.joblib")


if __name__ == "__main__":
    main()
