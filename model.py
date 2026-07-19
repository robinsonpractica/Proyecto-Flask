import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
import joblib

def train_model():
    df = pd.read_csv("adult-census-income.csv")
    df.replace("?", pd.NA, inplace=True)
    df.dropna(inplace=True)
    df['income'] = df['income'].str.strip()
    df['high_income'] = df['income'].apply(lambda x: 1 if x == '>50K' else 0)

    features = ['age', 'education', 'marital.status', 'occupation', 'hours.per.week', 'sex', 'native.country']
    X = df[features]
    y = df['high_income']

    numeric_features = ['age', 'hours.per.week']
    categorical_features = ['education', 'marital.status', 'occupation', 'sex', 'native.country']

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ]
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', KNeighborsClassifier(n_neighbors=40))
    ])

    model.fit(X, y)
    joblib.dump(model, 'model.pkl')
    print("Modelo entrenado y guardado como model.pkl")

if __name__ == "__main__":
    train_model()
