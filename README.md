# 💰 Loan Approval Predictor — Web App

A polished, animated web app that predicts loan approval likelihood, built with **Flask** (backend) and a custom **HTML/CSS/JS** frontend.

This is the "full experience" version — a real web page with smooth animations — as opposed to a simpler Streamlit version.

## Model

- **Algorithm:** Logistic Regression (scikit-learn)
- **Test Accuracy:** 89.71%
- **Train Accuracy:** 89.64%
- **Preprocessing:** `ColumnTransformer` with one-hot encoding (gender, home ownership, loan intent), ordinal encoding (education), and standard scaling (income, loan amount, credit score)

## Project structure

```
loan-approval-webapp/
├── app.py                          # Flask backend (loads model + serves predictions)
├── templates/
│   └── index.html                  # Page markup
├── static/
│   ├── style.css                    # Styling + animations
│   └── script.js                     # Form handling, live ratio calc, animated result
├── transformer.pkl                  # ← ADD THIS: your fitted ColumnTransformer
├── loan_prediction_model.pkl        # ← ADD THIS: your trained Logistic Regression model
├── loan_prediction.ipynb            # EDA, charts, and visual analysis
├── loan_prediction_model.ipynb      # Preprocessing, encoding, and model training
├── requirements.txt
└── README.md
```

⚠️ **You must add your own `transformer.pkl` and `loan_prediction_model.pkl` into this folder** (same folder as `app.py`) before running — they're not included in the download.

The two notebooks aren't required for the app to run — they're included so anyone browsing the repo can see the full process: `loan_prediction.ipynb` covers the exploratory analysis (distributions, correlations, charts), and `loan_prediction_model.ipynb` covers preprocessing, encoding, and training the model that `app.py` serves.

## Run locally

```bash
cd loan-approval-webapp
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## How it works

1. The form on the page collects all 12 input features.
2. On submit, `script.js` sends them as JSON to the Flask `/predict` route.
3. `app.py` builds a one-row DataFrame with the exact column names/order used in training, runs it through your fitted `transformer.pkl` (same ColumnTransformer: one-hot + ordinal encoding + scaling), then calls `loan_prediction_model.pkl.predict()`.
4. The result (approved/rejected + probability) is sent back as JSON and animated into the result card — probability bar fills and the percentage counts up.

## Deploy for free (so you get a public link)

**Render** (recommended, free tier):
1. Push this folder to a GitHub repo (include the two `.pkl` files and both notebooks)
2. Go to render.com → **New → Web Service** → connect your GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy — Render gives you a public URL like `https://loan-predictor.onrender.com`

**Railway** is another good free option with a very similar flow.

## Notes

- `gunicorn` is included in `requirements.txt` for production deployment (Render/Railway use it instead of Flask's dev server).
- Free-tier services may "sleep" after inactivity — the first request after idling can take 10–20 seconds to wake up.
