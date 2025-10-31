import pandas as pd 
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

def validate_dataset(df, target_column):
    errors = []

    # Check if target exists
    if target_column not in df.columns:
        errors.append(f"Target column '{target_column}' not found in dataset.")
        return errors

    # Check if we can actually analyze the dataset! If it has less than 5 rows, there's not
    # much to go off of 
    if df.empty or df.shape[0] < 5:
        errors.append("Dataset is empty or has too few rows to analyze.")

    # Check if target has only one value.
    # If the target has ONLY ONE VALUE, then there's nothing we can learn from
    if df[target_column].nunique() <= 1:
        errors.append("Target column must have at least 2 unique values.")

    # Check if there are any actual columns we can use. We want to ensure that 
    # at least one column has actual variation that we can explain. If not, 
    usable_features = df.drop(columns=[target_column])
    has_variation = False
    for col in usable_features.columns:
        if usable_features[col].nunique() > 1:
            has_variation = True
            break

    if not has_variation:
        errors.append("No usable features with variation in dataset.")

    return errors  # return list of problems (or empty list)

def clean_dataset(df, target_column):
    X = df.drop(columns=[target_column])  # all features
    y = df[target_column]  # target

    drop_cols = []
    for col in X.columns:
        if X[col].nunique() <= 1:
            drop_cols.append(col)

    X_clean = X.drop(columns=drop_cols)

    # Optional: Drop high-cardinality IDs (one value per row)
    for col in X_clean.columns:
        if (
            X_clean[col].nunique() == len(X_clean)
            and (
                not pd.api.types.is_numeric_dtype(X_clean[col])  # e.g. strings
                or "id" in col.lower()                            # or looks like an ID
            )
        ):
            X_clean = X_clean.drop(columns=[col])


    # Return cleaned features + target
    X_clean = pd.get_dummies(X_clean, drop_first=True)
    return X_clean, y

# for each dataset, the following will be generated in this function.
'''
{
  "model_type": "classification",
  "target_column": "has_disease",
  "model_used": "RandomForestClassifier",
  "score": 0.93,  # accuracy
  "feature_importance": {
    "blood_pressure": 0.58,
    "age": 0.32,
    "gender_M": 0.10
  },
  "dropped_columns": ["patient_id"],
  "highly_correlated_pairs": [
    "blood_pressure vs has_disease: 0.76"
  ],
  "notes": [
    "Binary classification detected"
  ]
}
'''
from sklearn.model_selection import train_test_split

def train_model(X_clean, y, target_column):
    # Determine if this is classification or regression
    unique_values = y.unique()
    if len(unique_values) == 2:
        problem_type = "classification"
        model = RandomForestClassifier()
    else:
        problem_type = "regression"
        model = RandomForestRegressor()

    # Split into train and test sets (30% test)
    X_train, X_test, y_train, y_test = train_test_split(X_clean, y, test_size=0.3, random_state=42)

    # Train model
    model.fit(X_train, y_train)

    # Score on the test set
    score = model.score(X_test, y_test)

    # Get feature importances
    importances = model.feature_importances_
    feature_names = X_clean.columns
    feature_importance_dict = dict(zip(feature_names, importances))

    return {
        "problem_type": problem_type,
        "target_column": target_column,
        "model_used": model.__class__.__name__,
        "score": score,
        "feature_importance": feature_importance_dict
    }

def describe_dataset_columns(df):
    column_descriptions = []
    for col in df.columns:
        sample_values = df[col].dropna().unique()[:5]  # get up to 5 unique non-null values
        sample_values = [str(v) for v in sample_values]
        column_descriptions.append(f"- {col}: sample values → {', '.join(sample_values)}")
    return "\n".join(column_descriptions)



