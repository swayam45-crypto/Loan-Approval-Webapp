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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    try:
        person_income = float(data["person_income"])
        loan_amnt = float(data["loan_amnt"])
        loan_percent_income = round(loan_amnt / person_income, 4) if person_income > 0 else 0.0

        # IMPORTANT: column names/order below must match the X dataframe used
        # when transformer.fit() / fit_transform() was called in the notebook.
        # Categorical text values must be spelled EXACTLY as in the training CSV.
        input_df = pd.DataFrame(
            [
                {
                    "person_age": float(data["person_age"]),
                    "person_gender": data["person_gender"],
                    "person_education": data["person_education"],
                    "person_income": person_income,
                    "person_emp_exp": int(data["person_emp_exp"]),
                    "person_home_ownership": data["person_home_ownership"],
                    "loan_amnt": loan_amnt,
                    "loan_intent": data["loan_intent"],
                    "loan_int_rate": float(data["loan_int_rate"]),
                    "loan_percent_income": loan_percent_income,
                    "cb_person_cred_hist_length": float(data["cb_person_cred_hist_length"]),
                    "credit_score": int(data["credit_score"]),
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
