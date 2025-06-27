from flask import Flask,render_template,request
import joblib
import numpy as np
from config.paths_config import *


app = Flask(__name__)

model_path = MODEL_PATH
scaler_path = SCALER_PATH

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@app.route('/')
def home():
    return render_template("index.html", predictions=None)

@app.route('/predict', methods=["POST"])
def predict():
    try:
        healthcare_cost = float(request.form["healthcare_costs"])
        treatment_type = int(request.form["treatment_type"])
        age = int(request.form['age'])
        alcohol_consumption = int(request.form['alcohol_consumption'])
        inflammatory = int(request.form['inflammatory_bowel_disease'])

        input = np.array([[healthcare_cost, treatment_type, age, alcohol_consumption, inflammatory]])

        scaled_input = scaler.transform(input)

        prediction = model.predict(scaled_input)[0]

        return render_template("index.html", prediction=prediction)
    
    except Exception as e:
        return str(e)
    
if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    





