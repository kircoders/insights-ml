from analyze_insights import validate_dataset, clean_dataset, train_model, describe_dataset_columns

def generate_gpt_prompt(model_info, df):
    problem_type = model_info["problem_type"]
    target = model_info["target_column"]
    model_name = model_info["model_used"]
    score = model_info["score"]
    features = model_info["feature_importance"]

    sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)
    feature_text = "\n".join(
        [f"- {feat}: {imp}" for feat, imp in sorted_features]
    )

    # Dataset column summary
    dataset_description = describe_dataset_columns(df)

    if problem_type == "classification":
        summary = f"The model predicts whether `{target}` is True or False."
        metric = f"Accuracy score on test data: **{score}**"
    else:
        summary = f"The model predicts the value of `{target}` (a numeric outcome)."
        metric = f"R² score on test data: **{score}**"

    prompt = f"""
You are analyzing a machine learning model trained using a Random Forest.

{summary}

**Model type:** {problem_type.capitalize()}
**Model used:** {model_name}
{metric}

### Dataset Columns: Some of the values include (these are not all the values! Just the top 5)
{dataset_description}

### Feature Importances:
{feature_text}

Based on this, summarize how this model works and what it's likely using to make predictions. Be clear, concise, and focus on what features matter most and why.
""".strip()

    return prompt
