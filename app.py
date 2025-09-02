from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os
import joblib
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

app = Flask(__name__)

# Paths
data_path = "student_performance_dataset.csv"
model_path = "student_model_keras.h5"
scaler_path = "scaler_keras.pkl"
encoders_path = "encoders_keras.pkl"
log_file = "predictions.h"

# Load dataset
df = pd.read_csv(data_path)
df.drop(columns=["Student_ID"], inplace=True)

# Load preprocessors
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(encoders_path)
# Load dataset
df = pd.read_csv(data_path)
df.drop(columns=["Student_ID"], inplace=True)

# Apply label encoders to dataset (MISSING STEP FIXED HERE)
categorical_columns = ["Gender", "Parental_Education_Level", "Internet_Access_at_Home", "Extracurricular_Activities"]
for col in categorical_columns:
    df[col] = label_encoders[col].transform(df[col])

# Encode target separately
df["Pass_Fail"] = label_encoders["Pass_Fail"].transform(df["Pass_Fail"])

# Features and target
X = df.drop(columns=["Pass_Fail", "Final_Exam_Score"])
y = df["Pass_Fail"]

# Scale features
X_scaled = scaler.transform(X)


# Load model
model = load_model(model_path)

# Predict on all for evaluation
y_pred_prob = model.predict(X_scaled).flatten()
y_pred = (y_pred_prob >= 0.5).astype(int)

# Evaluation
accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred)
recall = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)

# Write header to log file if not exists
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("// Prediction Log Header File\n")
        f.write("#ifndef PREDICTIONS_H\n#define PREDICTIONS_H\n\n")

# Log prediction
def log_prediction(data, result):
    from datetime import datetime
    with open(log_file, "a") as f:
        f.write("// New Prediction\n")
        f.write(f"// Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"// Gender: {data['gender']}, Study Hours: {data['study_hours']}, Attendance: {data['attendance']}, ")
        f.write(f"Past Scores: {data['past_exam_scores']}, Parental Education: {data['parental_education']}, ")
        f.write(f"Internet: {data['internet_access']}, Extracurricular: {data['extracurricular']}\n")
        f.write(f"#define PREDICTION_{str(hash(str(data)))[:8]} \"{result}\"\n\n")

@app.route('/')
def index():
    try:
        acc = round(accuracy, 2)
        prec = round(precision, 2)
        rec = round(recall, 2)
        f1s = round(f1, 2)
    except Exception as e:
        acc = prec = rec = f1s = "N/A"
        print(f"Error displaying metrics: {e}")

    return render_template('index.html', accuracy=acc, precision=prec, recall=rec, f1=f1s)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        input_array = np.array([[ 
            label_encoders["Gender"].transform([data['gender']])[0],
            int(data['study_hours']),
            float(data['attendance']),
            int(data['past_exam_scores']),
            label_encoders["Parental_Education_Level"].transform([data['parental_education']])[0],
            label_encoders["Internet_Access_at_Home"].transform([data['internet_access']])[0],
            label_encoders["Extracurricular_Activities"].transform([data['extracurricular']])[0]
        ]])
        input_scaled = scaler.transform(input_array)
        prediction_prob = model.predict(input_scaled)[0][0]
        prediction = int(prediction_prob >= 0.5)
        result = "Pass" if prediction == 1 else "Fail"

        log_prediction(data, result)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

