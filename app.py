import os
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['age'])
    education = request.form['education']
    marital_status = request.form['marital_status']
    occupation = request.form['occupation']
    hours_per_week = int(request.form['hours_per_week'])
    sex = request.form['sex']
    native_country = request.form['native_country']

    import pandas as pd
    user_data = pd.DataFrame([{
        'age': age,
        'education': education,
        'marital.status': marital_status,
        'occupation': occupation,
        'hours.per.week': hours_per_week,
        'sex': sex,
        'native.country': native_country
    }])

    prediction = model.predict(user_data)[0]
    probability = model.predict_proba(user_data)[0][1]

    if prediction == 1:
        result = f"Con este perfil, tu probabilidad de ganar mas de 50K es del {probability*100:.1f}%."
        status = "high"
    else:
        result = f"Con este perfil, tu probabilidad de superar los 50K es del {probability*100:.1f}%. Considera mejorar tu educacion o cambiar de ocupacion."
        status = "low"

    return render_template('index.html', result=result, status=status,
                         age=age, education=education, marital_status=marital_status,
                         occupation=occupation, hours_per_week=hours_per_week,
                         sex=sex, native_country=native_country)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
