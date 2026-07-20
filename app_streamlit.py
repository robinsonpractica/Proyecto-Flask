import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier

@st.cache_resource
def load_model():
    df = pd.read_csv("adult-census-income.csv")
    df.replace("?", pd.NA, inplace=True)
    df.dropna(inplace=True)
    df['income'] = df['income'].str.strip()
    df['high_income'] = df['income'].apply(lambda x: 1 if x == '>50K' else 0)

    features = ['age', 'education', 'marital.status', 'occupation', 'hours.per.week', 'sex', 'native.country']
    X = df[features]
    y = df['high_income']

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ['age', 'hours.per.week']),
            ("cat", OneHotEncoder(handle_unknown='ignore'), ['education', 'marital.status', 'occupation', 'sex', 'native.country']),
        ]
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', KNeighborsClassifier(n_neighbors=40))
    ])
    model.fit(X, y)
    return model

model = load_model()

st.title("Predictor de Ingresos Anuales")
st.markdown("Basado en datos del Censo de EE.UU. - Modelo KNN")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Edad", min_value=17, max_value=90, value=25)
    education = st.selectbox("Educacion", [
        "Bachelors", "Some-college", "HS-grad", "Masters", "Doctorate",
        "Prof-school", "Assoc-voc", "Assoc-acdm", "11th", "10th", "9th",
        "12th", "7th-8th", "5th-6th", "1st-4th", "Preschool"
    ])
    marital_status = st.selectbox("Estado Civil", [
        "Never-married", "Married-civ-spouse", "Divorced",
        "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"
    ])

with col2:
    occupation = st.selectbox("Ocupacion", [
        "Prof-specialty", "Craft-repair", "Exec-managerial",
        "Adm-clerical", "Sales", "Other-service", "Machine-op-inspct",
        "Transport-moving", "Handlers-cleaners", "Farming-fishing",
        "Tech-support", "Protective-serv", "Priv-house-serv", "Armed-Forces"
    ])
    hours_per_week = st.number_input("Horas por semana", min_value=1, max_value=99, value=40)
    sex = st.selectbox("Sexo", ["Male", "Female"])
    native_country = st.selectbox("Pais de origen", [
        "United-States", "Mexico", "Philippines", "Germany", "Canada",
        "Puerto-Rico", "El-Salvador", "Cuba", "Jamaica", "Italy",
        "India", "Japan", "China", "South", "England", "Colombia",
        "Dominican-Republic", "Haiti", "Guatemala", "Poland", "Taiwan",
        "Iran", "Peru", "France", "Ecuador", "Nicaragua", "Vietnam",
        "Honduras", "Thailand", "Greece", "Trinadad&Tobago", "Portugal",
        "Ireland", "Cambodia", "Hungary", "Scotland", "Holand-Netherlands"
    ])

if st.button("Predecir Ingreso"):
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
        st.success(f"Con este perfil, tu probabilidad de ganar mas de 50K es del {probability*100:.1f}%.")
    else:
        st.error(f"Con este perfil, tu probabilidad de superar los 50K es del {probability*100:.1f}%. Considera mejorar tu educacion o cambiar de ocupacion.")
