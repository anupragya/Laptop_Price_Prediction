import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# =====================================================================
# MACHINE LEARNING MODEL PLACEHOLDER
# =====================================================================
# Load your actual pipeline or pickle file here when ready.
# import pickle
# with open('your_model.pkl', 'rb') as f:
#     model = pickle.load(f)

def fallback_prediction(features):
    """
    Sarcastic dummy model weights to calculate a price because 
    real math is exhausting in this economy.
    """
    # Features sequence: [Company, Inches, ScreenResolution, Cpu, Ram, Memory, Gpu, OpSys]
    base_price = 150.0
    price = (
        base_price + 
        (features[0] * 12.5) +  # Company
        (features[1] * 35.0) +  # Inches
        (features[2] * 45.0) +  # ScreenResolution
        (features[3] * 8.5)  +  # Cpu
        (features[4] * 55.0) +  # Ram
        (features[5] * 15.0) +  # Memory (safely handled if missing)
        (features[6] * 7.0)  +  # Gpu
        (features[7] * 22.0)    # OpSys
    )
    return round(float(price), 2)


# =====================================================================
# SERVER ROUTES
# =====================================================================

@app.route('/')
def index():
    """Boots up the glorious laptop OS desktop simulation."""
    return render_template('index.html')


@app.route('/project', methods=['GET', 'POST'])
def project():
    """
    Processes the laptop specs directly from your HTML form mapping.
    Matches the exact layout seen in your screenshot.
    """
    prediction = None
    error_msg = None
    user_inputs = {}

    if request.method == 'POST':
        try:
            # Helper to securely convert form strings into numerical dataset values
            def extract_field(field_name, default=np.nan):
                val = request.form.get(field_name)
                return float(val) if val and val.strip() != '' else default

            # Parse inputs matching CleanedData.csv structure & your form fields
            company    = extract_field('Company')
            inches     = extract_field('Inches')
            screen_res = extract_field('ScreenResolution')
            cpu        = extract_field('Cpu')
            ram        = extract_field('Ram')
            memory     = extract_field('Memory', default=15.0) # Median fallback for missing data
            gpu        = extract_field('Gpu')
            opsys      = extract_field('OpSys')

            # Keep values alive in the inputs context to re-populate the form layout
            user_inputs = {
                'Company': company, 'Inches': inches, 'ScreenResolution': screen_res,
                'Cpu': cpu, 'Ram': ram, 'Memory': memory, 'Gpu': gpu, 'OpSys': opsys
            }

            # Array sequence alignment: Company, Inches, ScreenResolution, Cpu, Ram, Memory, Gpu, OpSys
            feature_array = [company, inches, screen_res, cpu, ram, memory, gpu, opsys]

            # Enforce validation so the user doesn't pass empty values to the matrix array
            if np.isnan(company) or np.isnan(cpu) or np.isnan(ram):
                raise ValueError("You skipped core components. Even our cynical code needs a Brand, CPU, and RAM to spit out a number.")

            # --- RUN THROUGH DISCRIMINATORY ESTIMATOR ---
            # if 'model' in globals():
            #     input_df = pd.DataFrame([feature_array], columns=['Company', 'Inches', 'ScreenResolution', 'Cpu', 'Ram', 'Memory', 'Gpu', 'OpSys'])
            #     prediction = round(float(model.predict(input_df)[0]), 2)
            # else:
            #     prediction = fallback_prediction(feature_array)

            prediction = fallback_prediction(feature_array)

        except Exception as e:
            error_msg = f"Crash Report: {str(e)}"

    return render_template('project.html', prediction=prediction, error=error_msg, inputs=user_inputs)


@app.route('/about')
def about():
    """Opens up the 'System Manifesto' settings log."""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Simulates the standard interactive mail server endpoint."""
    message_sent = False
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Local pipeline testing output
        print(f"\n[📥 Message Routed to Black Hole]\nSender: {email}\nRegarding: {subject}\nPayload: {message}\n")
        message_sent = True

    return render_template('contact.html', success=message_sent)


if __name__ == '__main__':
    # Debug active so changes to your vibrant styles show immediately without server resets
    app.run(debug=True, port=5000)