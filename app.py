from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# -----------------------------
# Load trained model + preprocessing transformer
# -----------------------------
with open("transformer.pkl", "rb") as f:
    transformer = pickle.load(f)

with open("loan_prediction_model.pkl", "rb") as f:
    model = pickle.load(f)

# previous_loan_defaults_on_file is mapped to 0/1 manually BEFORE the
# ColumnTransformer in the notebook (it's not one of the transformer's
# columns), so we replicate that exact step here.
DEFAULT_MAP = {"No": 0, "Yes": 1}

# Realistic bounds based on the actual training data distribution.
# Values outside these ranges are far outside what the model ever saw during
# training, so predictions there are unreliable (linear extrapolation, not
# learned signal). We reject them here rather than silently returning a
# misleading prediction.
FIELD_RANGES = {
    "person_age": (18, 100),
    "person_income": (8000, 1000000),
    "person_emp_exp": (0, 60),
    "loan_amnt": (500, 35000),
    "loan_int_rate": (5, 20),
    "cb_person_cred_hist_length": (2, 30),
    "credit_score": (390, 850),
}


def validate_ranges(values):
    for field, (low, high) in FIELD_RANGES.items():
        val = values[field]
        if val < low or val > high:
            raise ValueError(
                f"{field} value {val} is outside the realistic range ({low}\u2013{high}) "
                f"seen in training data. Predictions outside this range aren't reliable."
            )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        person_age = float(data["person_age"])
        person_income = float(data["person_income"])
        person_emp_exp = int(data["person_emp_exp"])
        loan_amnt = float(data["loan_amnt"])
        loan_int_rate = float(data["loan_int_rate"])
        cb_person_cred_hist_length = float(data["cb_person_cred_hist_length"])
        credit_score = int(data["credit_score"])

        validate_ranges(
            {
                "person_age": person_age,
                "person_income": person_income,
                "person_emp_exp": person_emp_exp,
                "loan_amnt": loan_amnt,
                "loan_int_rate": loan_int_rate,
                "cb_person_cred_hist_length": cb_person_cred_hist_length,
                "credit_score": credit_score,
            }
        )

        loan_percent_income = round(loan_amnt / person_income, 4) if person_income > 0 else 0.0

        # IMPORTANT: column names/order below must match the X dataframe used
        # when transformer.fit() / fit_transform() was called in the notebook.
        # Categorical text values must be spelled EXACTLY as in the training CSV.
        input_df = pd.DataFrame(
            [
                {
                    "person_age": person_age,
                    "person_gender": data["person_gender"],
                    "person_education": data["person_education"],
                    "person_income": person_income,
                    "person_emp_exp": person_emp_exp,
                    "person_home_ownership": data["person_home_ownership"],
                    "loan_amnt": loan_amnt,
                    "loan_intent": data["loan_intent"],
                    "loan_int_rate": loan_int_rate,
                    "loan_percent_income": loan_percent_income,
                    "cb_person_cred_hist_length": cb_person_cred_hist_length,
                    "credit_score": credit_score,
                    "previous_loan_defaults_on_file": DEFAULT_MAP[data["previous_loan_defaults_on_file"]],
                }
            ]
        )

        transformed_input = transformer.transform(input_df)
        prediction = int(model.predict(transformed_input)[0])

        proba = None
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba(transformed_input)[0][1])

        return jsonify(
            {
                "approved": bool(prediction == 1),
                "probability": proba,
                "loan_percent_income": loan_percent_income,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
