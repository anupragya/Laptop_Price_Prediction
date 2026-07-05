import os
import pandas as pd
import numpy as np
import joblib  # Look at you go, reading binary files properly now
from flask import Flask, render_template, request

app = Flask(__name__)

# =====================================================================
# SECURE MODEL INITIALIZATION
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'Random_Forest.lb')

try:
    model = joblib.load(MODEL_PATH)
    print("🤖 System Report: Random Forest model successfully initialized. Ready to crush dreams.")
except FileNotFoundError:
    print(f"❌ Critical Error: Could not find model file at {MODEL_PATH}")
    model = None
except Exception as e:
    print(f"❌ Unexpected Loading Error: {str(e)}")
    model = None


# =====================================================================
# WEB SERVER ROUTES
# =====================================================================

@app.route('/')
def index():
    """Boots up the modern Windows OS desktop simulation."""
    return render_template('index.html')


@app.route('/project', methods=['GET', 'POST'])
def project():
    """
    Windows Predictor App: Form input handling corresponding exactly 
    to your CleanedData.csv numerical matrix columns.
    """
    prediction = None
    error_msg = None
    user_inputs = {}

    if request.method == 'POST':
        try:
            # Safely converts blank/empty options to avoid input matrix crashes
            def extract_field(field_name, default=np.nan):
                val = request.form.get(field_name)
                return float(val) if val and val.strip() != '' else default

            # Parse inputs matching your dataset columns and frontend layout
            company    = extract_field('Company')
            inches     = extract_field('Inches')
            screen_res = extract_field('ScreenResolution')
            cpu        = extract_field('Cpu')
            ram        = extract_field('Ram')
            memory     = extract_field('Memory', default=15.0)  # Safe dataset fallback for blank rows
            gpu        = extract_field('Gpu')
            opsys      = extract_field('OpSys')

            # Build dict back to HTML so user selections stay selected after posting
            user_inputs = {
                'Company': company, 'Inches': inches, 'ScreenResolution': screen_res,
                'Cpu': cpu, 'Ram': ram, 'Memory': memory, 'Gpu': gpu, 'OpSys': opsys
            }

            # Enforce minimal constraints before running calculations
            if np.isnan(company) or np.isnan(cpu) or np.isnan(ram):
                raise ValueError("Windows System Alert: Mandatory core hardware fields (Brand, CPU, RAM) are missing.")

            # Compile row feature array mapping to your CleanedData.csv structure
            feature_array = [company, inches, screen_res, cpu, ram, memory, gpu, opsys]

            if model:
                # Build a 2D DataFrame with explicit matching features columns for Scikit-Learn
                input_df = pd.DataFrame([feature_array], columns=[
                    'Company', 'Inches', 'ScreenResolution', 'Cpu', 'Ram', 'Memory', 'Gpu', 'OpSys'
                ])
                
                # Predict and extract the zero-index float output value
                raw_pred = model.predict(input_df)[0]
                prediction = round(float(raw_pred), 2)
            else:
                raise RuntimeError("The Random Forest model file is offline. Did you leave it out of the folder again?")

        except Exception as e:
            error_msg = f"Application Error: {str(e)}"

    return render_template('project.html', prediction=prediction, error=error_msg, inputs=user_inputs)


@app.route('/about')
def about():
    """Windows App Window: System Specification Manifesto/Readme."""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Windows App Window: System Mail client route endpoint handler."""
    message_sent = False
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Terminal diagnostics tracking client feedback strings
        print(f"\n[📥 Message Logged to Windows Outlook Client]\nFrom: {email}\nRegarding: {subject}\nPayload: {message}\n")
        message_sent = True

    return render_template('contact.html', success=message_sent)


if __name__ == '__main__':
    # Debug engine left enabled to dynamically catch style updates instantly
    app.run(debug=True, port=5000)