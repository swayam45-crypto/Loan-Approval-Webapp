# 💰 Loan Approval Predictor

A machine learning web app that predicts loan approval likelihood in real time, built with **scikit-learn**, **Flask**, and a custom animated frontend.

🔗 **Live demo:** [loan-approval-webapp.onrender.com](https://loan-approval-webapp.onrender.com)
📓 **Notebooks:** [`loan_prediction.ipynb`](./loan_prediction.ipynb) (EDA & visualizations) · [`loan_prediction_model.ipynb`](./loan_prediction_model.ipynb) (preprocessing & training)

---

## Overview

This project trains a classification model on 45,000 historical loan applications to predict whether a new application is likely to be approved, and serves that model through a Flask API and a polished, animated web interface — complete with a light/dark theme toggle.

## Features

- **Real-time predictions** — submit applicant and loan details, get an instant approval likelihood with a confidence score
- **Live auto-calculated fields** — loan-to-income ratio updates as you type
- **Light/dark theme toggle** with a custom animated gradient background
- **Clean separation of concerns** — Flask backend handles inference; frontend is plain HTML/CSS/JS with no build step

## Model

- **Algorithm:** Logistic Regression (scikit-learn)
- **Test Accuracy:** 89.71%
- **Train Accuracy:** 89.64%
- **Preprocessing:** a single fitted `ColumnTransformer` handling:
  - One-hot encoding — `person_gender`, `person_home_ownership`, `loan_intent`
  - Ordinal encoding — `person_education` (High School → Doctorate)
  - Standard scaling — `person_income`, `loan_amnt`, `credit_score`
  - Remaining features pass through unchanged

### A note on model behavior

This dataset is **synthetic** (sourced from Kaggle's Loan Approval Classification dataset). During evaluation, I found the model's decision boundary doesn't always track real-world lending intuition — for example, prior loan defaults are an almost deterministic rejection signal, while income and credit score have a much weaker and occasionally counterintuitive relationship with approval in this particular dataset. This is a property of the synthetic data generation, not a bug in the pipeline — I verified the app's predictions match the training notebook's output exactly on real rows from the dataset. Worth keeping in mind if you extend this project with real-world data.

## Project structure

```
loan-approval-webapp/
├── app.py                          # Flask backend — loads model, serves predictions
├── templates/
│   └── index.html                  # Frontend markup, styling (Tailwind CDN), and theme logic
├── static/
│   └── script.js                   # Form handling, live ratio calc, animated result rendering
├── transformer.pkl                 # Fitted ColumnTransformer (encoding + scaling)
├── loan_prediction_model.pkl       # Trained Logistic Regression model
├── loan_prediction.ipynb           # EDA, charts, and visual analysis
├── loan_prediction_model.ipynb     # Preprocessing, encoding, and model training
├── requirements.txt
└── README.md
```

## How it works

1. The form collects 12 applicant and loan features (a 13th, `loan_percent_income`, is auto-calculated).
2. On submit, the frontend sends the raw values as JSON to the Flask `/predict` endpoint.
3. The backend builds a single-row DataFrame with the exact column names used in training, runs it through the fitted `transformer.pkl`, then calls `loan_prediction_model.pkl.predict()`.
4. The result — approved/rejected plus a probability score — is returned as JSON and rendered with an animated result card.

## Tech stack

`Python` · `scikit-learn` · `pandas` · `Flask` · `gunicorn` · `HTML/CSS/JS` · `Tailwind CSS`

## Limitations

- Trained on a single synthetic dataset — not validated against real-world lending data or regulations
- For educational and portfolio purposes only — not a real lending or financial decision tool

## Future improvements

- Add SHAP-based explainability for individual predictions
- Compare against additional models (Random Forest, XGBoost, Gradient Boosting)
- Validate against a real-world credit dataset to check for generalization

---

*AI-powered loan eligibility insights · Built by Swayam Bhoir*
