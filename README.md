🎓 Student Performance Prediction
📌 Overview

This project predicts student academic performance based on various input features such as study habits, attendance, socio-economic factors, and past scores. It leverages Machine Learning models to assist educators, parents, and institutions in identifying at-risk students and improving learning outcomes.

🚀 Features

📊 Data preprocessing and cleaning

🤖 Machine Learning model training & evaluation

📈 Performance metrics (Accuracy, Precision, Recall, F1-score)

🌐 Flask-based web interface for predictions

💾 Option to save prediction results

🏗️ Tech Stack

Frontend: HTML, CSS, Bootstrap (for UI)

Backend: Flask (Python)

Machine Learning: Scikit-learn, Pandas, NumPy

Visualization: Matplotlib, Seaborn

Database (optional): SQLite / CSV

📂 Project Structure
Student-Performance-Prediction/
│-- dataset/               # Contains dataset (CSV file)
│-- models/                # Saved ML models (.pkl files)
│-- static/                # CSS, JS, Images
│-- templates/             # HTML files for Flask app
│-- app.py                 # Flask application
│-- student_performance.ipynb  # Jupyter notebook for ML model building
│-- requirements.txt       # Required Python packages
│-- README.md              # Project documentation

⚙️ Installation

Clone this repository:

git clone https://github.com/your-username/student-performance-prediction.git
cd student-performance-prediction


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate     # For Linux/Mac
venv\Scripts\activate        # For Windows


Install dependencies:

pip install -r requirements.txt

▶️ Usage

Run the Flask app:

python app.py


Open in your browser:

http://127.0.0.1:5000/


Enter student details in the form and get the predicted performance.

📊 Model Training

Data is preprocessed (handling missing values, encoding categorical data, scaling).

Various ML models are tested:

Logistic Regression

Random Forest

Decision Tree

XGBoost (optional)

Best performing model is saved using joblib.

📈 Results

Model Accuracy: ~0.90 (depending on dataset)

Insights:

Attendance, study hours, and past grades strongly affect performance.

Socio-economic factors have moderate influence.

🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
